'''
main driver for a simple social network project
'''

import os
import csv
import logging
import re
import users
import user_status
import socialnetwork_model as sn
from exceptions import NonFileExtension, InvalidEmailException

# pylint:  disable=W0707,W0612,R1702,R1710,C2801,W1514
_PATH = os.getcwd()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LOGGER = logging.getLogger(__name__)

def create_data_tables():
    '''
    Creates our social database - alleviates the 
        necessity of above two functions
    '''
    the_db = sn.create_tables()
    return the_db

DB = create_data_tables()

def get_file(filename):
    """
        Add-in to get a file
        return a file object
        via the csv module
        & context mgr
        handles exceptions
    Keyword arguments:
        filename -> str()
    Purpose:
        find a filename, return file object
    Return:
        if file exists - file
        else exception
    """
    if isinstance(filename, int):
        raise TypeError('''Please supply a
                        proper string for a
                        file name.''')
    if isinstance(filename, str):
        try:
            f_name = filename.split('.')
            first = f_name[0][::]
            last = f_name[1][-3:]
            for the_dir, subdir, file in os.walk(_PATH):
                for the_file in file:
                    if the_file.endswith(last):
                        first_ = the_file.split('.')[0]
                        if first_ == first:
                            file_match = the_file
                            return file_match
                raise FileNotFoundError
        except IndexError:
            raise NonFileExtension("Invalid extension. Please retry.")
        except FileNotFoundError as _f:
            raise FileNotFoundError('File does not exist in the repository.') from _f

def load_users(filename, the_db=DB):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    file = get_file(filename) #may meet reqs. raises exceptions instead of False
    with open(file, newline='') as _f:
        reader = csv.DictReader(_f)
        for row in reader:
            if row.keys().__contains__(None):
                return False
            users.UserCollection().add_user(
                row['USER_ID'],
                row['EMAIL'],
                row['NAME'],
                row['LASTNAME'],
                the_db
            )
    return True

def load_status_updates(filename, the_db=DB):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    '''
    file = get_file(filename)
    with open(file, newline='') as _f:
        reader = csv.DictReader(_f)
        for row_num, row in enumerate(reader):
            if list(row.values()).__contains__(None) or row.keys().__contains__(None):
                return False
            user_status.UserStatusCollection().add_status(
                row['STATUS_ID'],
                row['USER_ID'],
                row['STATUS_TEXT'],
                the_db
            )
    return True

def add_user(user_id, email, user_name, user_last_name, the_db=DB):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    if not EMAIL_REGEX.match(email):
        raise InvalidEmailException('''Email does not match standard email format.
                                    (___@__.com) Please retry.''')
    the_add = users.UserCollection().add_user(user_id, email, user_name, user_last_name, the_db)
    return the_add

def update_user(user_id, email, user_name, user_last_name, the_db=DB):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    if not EMAIL_REGEX.match(email):
        logging.warning("App crash due to invalid email sent. Raising exception.")
        raise InvalidEmailException('''Email does not match standard email format.
                                    (___@__.com) Please retry.''')
    updated = users.UserCollection().modify_user(user_id, email, user_name,
                                                 user_last_name, the_db)
    return updated

def delete_user(user_id, the_db=DB):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    deleted = users.UserCollection().delete_user(user_id, the_db)
    return deleted

def search_user(user_id, the_db=DB):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    found = users.UserCollection().search_user(user_id, the_db)
    if found is False:
        print(f"No user found for user id: {user_id}...")
    return found

def add_status(user_id, status_id, status_text, the_db=DB):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    stats = user_status.UserStatusCollection().add_status(status_id, user_id, status_text, the_db)
    return stats

def update_status(status_id, user_id, status_text, the_db=DB):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    updated_stats = user_status.UserStatusCollection().modify_status(status_id,
                                                                     user_id,
                                                                     status_text,
                                                                     the_db)
    return updated_stats

def delete_status(status_id, the_db=DB):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    if not isinstance(status_id, str):
        raise TypeError('Status id field should be a string.')
    deleted = user_status.UserStatusCollection().delete_status(status_id, the_db)
    return deleted

def search_status(status_id, the_db=DB):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    if not isinstance(status_id, str):
        raise TypeError('Status id field should be a string.')
    found = user_status.UserStatusCollection().search_status(status_id, the_db)
    if found is False:
        print(f"Search for status: {status_id} not found...")
    return found

def search_status_updates_by_user(user_id, the_db=DB):
    """
     Relies on the database model
     in 'social network model' to 
     return a list of rows,
     each row being a status by 
     a unique user
    
    Keyword arguments:
        user_id -> str()
            User id to search for
        
        the_db -> Sqlitedatabase
            database to use for searching
    Return:
        if a status for the user exists,
            it will return all statuses, inclusive
            of a singular status
        else
            False
    """
    the_statuses = user_status.UserStatusCollection().search_all_status_updates(user_id, the_db)
    if the_statuses:
        return the_statuses
    return False

def filter_status_by_string(text, the_db=DB):
    """
      Calls user_status method w/ same name
      to return an iterator of all statuses
      matching a supplied 'text' 
    Keyword arguments:
        the_db -> Sqlitedatabase
            the database to search
        text -> str()
            text to search the db for
    Return:
        if there are statuses
            returns them all in an iterator
            object, inclusive of 1 status
        else
            returns False
    """
    statuses = user_status.UserStatusCollection().filter_status_by_string(text, the_db)
    if statuses:
        return statuses
    return False
