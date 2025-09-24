""" Implements databse functionality 
    for assignment 03
"""
# pylint: disable=W0611,W1514,E0401,E1120,R0903,E0602,C0103,E1205,W1203,W0150,W0311,W0621,W0718
import os
from datetime import date
import logging
import peewee as pw
import users
import user_status

the_date = date.today()
date_items = str(the_date).split('-')
yr = date_items[0]
month = date_items[1]
day = date_items[2]
LOG_F = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_F)
file_handle = logging.FileHandler(f"log_{month}_{day}_{yr}_DATABASE.log")
file_handle.setLevel(logging.INFO)
file_handle.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handle)

_FILE = 'social.db'
# if os.path.exists(_FILE):
#     os.remove(_FILE)
#     logging.info('Existing databse removed, fresh database created')

db = pw.SqliteDatabase(_FILE)

class BaseModel(pw.Model):
    ''' Base Model for database '''
    class Meta:
        ''' Allows db to be edited in 1 place '''
        database = db

class User(BaseModel):
    ''' Representing Users for the database '''
    t_user_id = pw.CharField(primary_key = True, max_length = 30, null = False)
    t_user_email = pw.CharField()
    t_user_name = pw.CharField(max_length = 30)
    t_user_last_name = pw.CharField(max_length = 100)

class Status(BaseModel):
    ''' Representing statuses for the database '''
    st_status_id = pw.CharField(primary_key = True)
    st_user_id = pw.ForeignKeyField(User, related_name='posted_by',
                                    null = False,
                                    on_delete='CASCADE')
    st_status_text = pw.CharField()

def check_email(email, user_obj):
    ''' Checks email for users.User object
        updates if email != None
    '''
    if email:
        user_obj.email = email
    return user_obj.email

def check_user_name(new_user_name, user_obj):
    ''' Checks new_user_name for users.User object
        updates if new_user_name != None
    '''
    if new_user_name:
        user_obj.user_name = new_user_name
    return user_obj.user_name

def check_last_name(new_last_name, user_obj):
    ''' Checks new_last_name for users.User object
        updates if new_last_name != None
    '''
    if new_last_name:
        user_obj.user_last_name = new_last_name
    return user_obj.user_last_name

def check_user_id(new_user_id, status_obj):
    ''' Checks new_user_id for status_obj
        (UserStatus object), if new_user_id
        != None the user_id attribute of
        status_obj is updated
    '''
    if new_user_id:
        status_obj.user_id = new_user_id
    return status_obj.user_id

def check_status_text(new_status, status_obj):
    ''' Checks new_status for status obj
        (UserStatus object), if new_status
        != None, status_obj attribute status_text
        is updated
    '''
    if new_status:
        status_obj.status_text = new_status
    return status_obj.status_text

def create_tables():
    '''Creates our tables '''
    MODELS = [BaseModel, User, Status]
    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    for model in MODELS:
        db.create_tables([
            model
        ])
    db.close()
    return db

def add_user_to_table(db, user_obj):
    """
        Adds user to User Model
        *t is prepending to signify table
    Keyword arguments:
        user_obj -> User
    Return: 
        Logs message/warning
        None
    """
    change = None
    try:
        db.connect()
        with db.transaction():
            new_user = User.create(
                t_user_id = user_obj.user_id,
                t_user_email = user_obj.email,
                t_user_name = user_obj.user_name,
                t_user_last_name = user_obj.user_last_name
            )
            new_user.save()
            change = True
    except Exception as e:
        logger.warning(f"Error creating user: {user_obj.user_id}")
        logger.warning("Details: ", e)
        change = False
    finally:
        db.close()
        return change

def modify_user(db, user_obj, new_email=None, new_u_name=None, new_l_name=None):
    """
        Modifies the selected user in the 
         User table of the database
    Keyword arguments:
        db -> Sqlitedatabase
            The database we want to update
        user_obj -> users.User
            The user object, tying to the record
            in the database
        **kwargs -> dict
            Will check for certain params,
            can only accept attributes of 
            the User Model within the 
            User Model class
    Return:
        Logs message/warning
        True if updated
        False otherwise
        None if not assigned
    """
    u_to_modify = user_obj.user_id
    f_email = check_email(new_email, user_obj)
    f_u_name = check_user_name(new_u_name, user_obj)
    f_l_name = check_last_name(new_l_name, user_obj)
    change = None
    try:
        db.connect()
        with db.transaction():
            check = User.select().where(User.t_user_id == f"{u_to_modify}")
            if check.exists():
                query = (User.update({User.t_user_email: f"{f_email}",
                            User.t_user_name: f"{f_u_name}",
                            User.t_user_last_name: f"{f_l_name}"})
                            .where(User.t_user_id.contains(f'{u_to_modify}')))
                query.execute()
                change = True
            else:
                change = False
    except Exception as e:
        logger.warning(f"Error modifying user: {user_obj.user_id}")
        logger.warning("Details: ", e)
    finally:
        db.close()
        return change

def delete_user_from_table(db, user_obj_id):
    """
        Deletes user from database table
    Keyword arguments:
        db -> Sqlitedatabse
            database containing table for
                user data
        user_obj -> str()
            user object containing attributes
                see imported users
    Return:
        if user exists in the db
        and is deleted -> return True
        else -> return False
        closes connection
    """
    change = None
    try:
        db.connect()
        with db.transaction():
            check = User.select().where(User.t_user_id == f"{user_obj_id}")
            if check.exists():
                query = User.delete().where(User.t_user_id == f"{user_obj_id}")
                query.execute()
                change = True
    except Exception as e:
        logger.warning(f"Error deleting user: {user_obj_id}")
        logger.warning("Details: ", e)
        change = False
    finally:
        db.close()
        return change

def search_user_in_table(db, user_obj_id):
    """
        Searches for user in database
    Keyword arguments:
        db -> Sqlitedatabase
            Database the search is enforced
                upon
        user_obj_id -> str()
            User id to search for
    Return: 
        if user id exists:
            return the full row
            of the User model object
        else:
            return False
    """
    row = None
    try:
        db.connect()
        with db.transaction():
            check = User.select().where(User.t_user_id == f"{user_obj_id}")
            if check.exists():
                row = [u.__data__ for u in check]
    except Exception as e:
        logger.warning(f"Error searching user: {user_obj_id}")
        logger.warning("Details: ", e)
    finally:
        db.close()
        if isinstance(row, list):
            return row[0]
        logger.info(f"Search user id: {user_obj_id} not found...")
        return False

######### BEGINNING OF STATUS ###############
def add_st_to_table(db, st_obj):
    """
        Add status to Status model
        *t prepended to signify table
    Keyword arguments:
        st_obj -> UserStatus
    Return: 
        Logs message/warning
        None
    """
    change = None
    try:
        db.connect()
        with db.transaction():
            new_status = Status.create(
                st_status_id = st_obj.status_id,
                st_user_id = st_obj.user_id,
                st_status_text = st_obj.status_text,
            )
            new_status.save()
            change = True
    except Exception as e:
        logger.warning(f"Error creating status: {st_obj.status_id}")
        logger.warning("Details: ", e)
        change = False
    finally:
        db.close()
        return change

def modify_status(db, status_obj, new_status_txt=None):
    """
        Updates status attributes of
        an existing status in the Model
        so long as the foreign key
        constraint is met
    Keyword arguments:
        db -> Sqlitedatabase
            The database to update
        status_obj -> UserStatus
            UserStatus object to update
        new_status_text -> str() or None
            The text for the status, if None,
                status posted is a direct copy
                from previous status
                ie. The status WILL post
    Return:
        If foreign key constraint is met:
            status posted, return True
        Else:
            return False
    """
    change = None
    try:
        db.connect()
        status_uid = status_obj.user_id
        text = check_status_text(new_status_txt, status_obj)
        with db.transaction():
            check = Status.select().join(User).where(User.t_user_id.contains(f"{status_uid}"))
            if check.exists():
                for item in check:
                    stat_id = item.st_status_id
                query = (Status.update({Status.st_status_text: f"{text}"})
                        .where(Status.st_status_id.contains(f'{stat_id}')))
                query.execute()
                change = True
            else:
                change = False
    except Exception as e:
            logger.warning(f"Error modifying status: {st_obj.status_id}")
            logger.warning("Details: ", e)
    finally:
        db.close()
        return change

def delete_status_from_table(db, status_obj_id):
    """
        Deletes a status from the
        database
    Keyword arguments:
        db -> Sqlitedatabase
            Database holding data
        status_obj -> str()
            status id to be deleted
    Return:
        if the status exists
            delete status, return true
        else
            return false
    """
    change = None
    try:
        db.connect()
        with db.transaction():
            check = Status.select().where(Status.st_status_id == f"{status_obj_id}")
            if check.exists():
                query = Status.delete().where(Status.st_status_id == f"{status_obj_id}")
                query.execute()
                change = True
    except Exception as e:
            logger.warning(f"Error deleting status: {st_obj.status_id}")
            logger.warning("Details: ", e)
            change = False
    finally:
        db.close()
        return change

def search_status_in_table(db, status_obj_id):
    """
        Searches for status in db
    Keyword arguments:
        db -> Sqlitedatabase
            database to search within
                leverage Status table
        status_obj_id -> str()
            Status id to search for
    Return:
        if status id exists:
            return the row for that Status
            including all attributes
        else:
            return False
    """
    row = None
    try:
        db.connect()
        with db.transaction():
            check = Status.select().where(Status.st_status_id == f"{status_obj_id}")
            if check.exists():
                row = [st.__data__ for st in check]
    except Exception as e:
            logger.warning(f"Error searching status: {st_obj.status_id}")
            logger.warning("Details: ", e)
    finally:
        db.close()
        if isinstance(row, list):
            return row[0]
        return False

def search_all_status_updates(db, user_id):
    """
        Searches for all statuses created by a unique user
        id
    Keyword arguments:
        db -> Sqlitedatabase
            database to search within
                leverage Status table
        user_id -> str()
            User id to search for
    Return:
        if we have statuses for a user_id
            add them to a collection
            where each row is unique
        else:
            return False
    """
    rows = None
    try:
        db.connect()
        with db.transaction():
            check = Status.select().where(Status.st_user_id.contains(f"{user_id}"))
            if check.exists():
                rows = [st.__data__ for st in check]
    except Exception as e:
            logger.warning(f"Error searching status: {st_obj.status_id}")
            logger.warning("Details: ", e)
    finally:
        db.close()
        if rows:
            return rows
        return False

def filter_status_by_string(db, text):
    """
     Searches db for any statuses
     containing a particular bit of text

    Keyword arguments:
        db -> Sqlitedatabase
            the database to use
        text -> str()
            text to search for within the
            status text section of all the
            statuses
    Return:
        if there are matching texts
            returns an iterable object
            containing all the matching statuses
        else
            False
    """
    rows = None
    try:
        db.connect()
        with db.transaction():
            check = Status.select().where(Status.st_status_text.contains(f"{text}"))
            if check.exists():
                rows = [st.__data__ for st in check]
    except Exception as e:
            logger.warning(f"Error searching status: {st_obj.status_id}")
            logger.warning("Details: ", e)
    finally:
        db.close()
        if rows:
            return rows
        return False
