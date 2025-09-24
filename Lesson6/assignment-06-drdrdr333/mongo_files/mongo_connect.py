'''
    Connection and database
    for MongoDB
    leverages pymongo
'''

#pylint: disable=W0311,W1203,R1710
import logging
from datetime import date
from pymongo import MongoClient
import users
import user_status

the_date = date.today()
date_items = str(the_date).split('-')
yr = date_items[0]
month = date_items[1]
day = date_items[2]

LOG_F = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_F)
file_handle = logging.FileHandler(f"log_{month}_{day}_{yr}_MONGO_db.log")
file_handle.setFormatter(formatter)
file_handle.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handle)

class MongoConnection():
    '''
        Connection object for
        data tunnel to/from
        MongoDB
    '''
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        ''' 
            For context manager to handle 
            external resource
        '''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
            Context manager to close
            connection to external resource
        '''
        self.connection.close()

# Database for the app
db = MongoConnection()

def create_collection(collection_name, the_db=db):
    """
        Create a collection within the database
        Leverage pre-defined library methods
        for pymongo - dependant upon if the 
        database exists
    
    Keyword arguments:
        the_db -> MongoClient
            the database for the app
        collection_name -> str()
            the name to assign to the collection

    Return:
        returns 
            True if the collection is created
        else
            False
    """
    if isinstance(collection_name, str):
        with the_db:
            new_db = the_db.connection.social_network
            new_collection = new_db.create_collection(collection_name)
            logger.info(f"Collection: {new_collection} created.")
        return True
    logger.warning(f"Error creating collection {collection_name}...")
    return False

def insert_to_db(_obj, the_db=db):
    """
        Insert user into Mongo DB
        Leverage pre-built method
    Keyword arguments:
        _obj -> users.User or user_status.UserStatus
            object to add
        the_db -> MongoClient
            database for app
    Return:
        bool
        True if object is modified
        False otherwise
        Logs both
    """
    if isinstance(_obj, users.Users):
        user = {
            "User ID": f"{_obj.user_id}",
            "User Email": f"{_obj.email}",
            "User Name": f"{_obj.user_name}",
            "User Last Name": f"{_obj.user_last_name}"
        }
        with the_db:
            check = the_db.connection.social_network.UserAccounts.find_one({
                "User ID": f"{_obj.user_id}"
            })
            if check is None:
                add_to = the_db.connection.social_network.UserAccounts
                add_to.insert_one(user)
                logger.info(f"User added: {_obj.user_id}, {_obj.user_name}")
                return True
            if check.keys():
                logger.warning(f"Prevent re-add of user id {_obj.user_id}")
                return False
    if isinstance(_obj, user_status.UserStatus):
        stat = {
            "Status ID": f"{_obj.status_id}",
            "User ID": f"{_obj.user_id}",
            "Status Text": f"{_obj.status_text}",
        }
        with the_db:
            check = the_db.connection.social_network.UserAccounts.find_one({
                "User ID": f"{_obj.user_id}"
            })
            if check is None:
                logger.warning(f"No matching user for status: {_obj.status_id}...closing")
                the_db.connection.close()
                return False
            if check.keys():
                check_two = the_db.connection.social_network.StatusUpdates.find_one({
                    "Status ID": f"{_obj.status_id}"
                })
                if check_two is None:
                    add_to = the_db.connection.social_network.StatusUpdates
                    add_to.insert_one(stat)
                    logger.info(f"Status id added: {_obj.status_id} for user id: {_obj.user_id}")
                else:
                    logger.info(f"Prevent duplicate stautus for {_obj.status_id}")
        return True

def modify_object_in_db(_obj, the_db=db):
    """
        Checks and verifies existence of object
        Modifies if object exists
        Null if it doesnt
    Keyword arguments:
        _obj -> users.User or user_status.UserStatus
            object to modify
        the_db -> MongoClient
            database for app
    Return:
        True if _obj is updated
        False if _obj does not exist or is not updated
    """
    if isinstance(_obj, users.Users):
        with the_db:
            check = the_db.connection.social_network.UserAccounts.find_one({
                "User ID": f"{_obj.user_id}"
            })
            if check is None:
                logger.warning(f"No matching user found for modify: {_obj.user_id}...closing")
                the_db.connection.close()
                return False
            if check.keys():
                the_db.connection.social_network.UserAccounts.update_one(
                    {"User ID": f"{_obj.user_id}"},
                    {
                        "$set": {
                            "User ID": f"{_obj.user_id}",
                            "User Email": f"{_obj.email}",
                            "User Name": f"{_obj.user_name}",
                            "User Last Name": f"{_obj.user_last_name}"
                        }
                    })
                return True
    if isinstance(_obj, user_status.UserStatus):
        with the_db:
            check = the_db.connection.social_network.UserAccounts.find_one({
                "User ID": f"{_obj.user_id}"
            })
            if check is None:
                logger.warning(f"""No matching user found for
                               modify of status: {_obj.user_id}...closing""")
                the_db.connection.close()
                return False
            if check.keys():
                the_db.connection.social_network.StatusUpdates.update_one(
                    {"User ID": f"{_obj.user_id}"},
                    {
                        '$set': {
                            "Status ID": f"{_obj.status_id}",
                            "User ID": f"{_obj.user_id}",
                            "Status Text": f"{_obj.status_text}",
                        }
                    })
                return True
    return False

def delete_user_in_db(_obj,  the_db=db):
    """
        checks if an _obj exists in MongoDB
        deletes if so
    Keyword arguments:
        _obj -> int() or str()
            id of user object to be deleted from collection
        the_db -> MongoClient()
            the database
    Return:
        bool
        True if object exists
        False if not
    """
    with the_db:
        check = the_db.connection.social_network.UserAccounts.find_one({
            "User ID": f"{_obj}"
        })
        if check is None:
            logger.warning(f"No matching user id found for {_obj} delete...closing")
            the_db.connection.close()
            return False
        if check.keys():
                the_db.connection.social_network.UserAccounts.delete_one({
                    "User ID": f"{_obj}"
                })
                logger.info(f"User: {_obj} deleted")
                the_db.connection.social_network.StatusUpdates.delete_many({
                    "User ID": f"{_obj}"
                })
                logger.info(f"All statuses for user {_obj} deleted")
    return True

def delete_status_in_db(_obj, the_db=db):
    ''' Same as above for statuses '''
    with the_db:
        check = the_db.connection.social_network.StatusUpdates.find_one({
            "Status ID": f"{_obj}"
        })
        if check is None:
            logger.warning(f"No matching user found for id {_obj} on delete...closing")
            the_db.connection.close()
            return False
        if check.keys():
            the_db.connection.social_network.StatusUpdates.delete_one({
                    "Status ID": f"{_obj}"
                })
            logger.info(f"Status id {_obj} deleted")
    return True

def search_user_in_db(_obj, the_db=db):
    """
       Searches for a user by user id
    Keyword arguments:
        _obj -> int() or str()
            user id to search for
        the_db -> MongoClient()
            database for app
    Return:

    """
    with the_db:
        res = the_db.connection.social_network.UserAccounts.find_one({
            "User ID": f"{_obj}"
        })
        if res is None:
            logger.info(f"No user found for id: {_obj}...closing db")
            the_db.connection.close()
            return False
        if res.keys():
            logger.info(f"User id: {_obj} found")
            the_db.connection.close()
            return dict(res)

def search_status_in_db(_obj, the_db=db):
    ''' Same as above for status, search 
        by status id
    '''
    with the_db:
        res = the_db.connection.social_network.StatusUpdates.find_one({
            "Status ID": f"{_obj}"
        })
        if res is None:
            logger.info(f"No status found for id: {_obj}...closing db")
            the_db.connection.close()
            return False
        if res.keys():
            logger.info(f"Status id: {_obj} found")
            the_db.connection.close()
            return dict(res)
