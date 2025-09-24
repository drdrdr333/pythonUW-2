'''
main driver for a simple social network project
'''

import os
import csv
import re
import users
import user_status
from exceptions import NonFileExtension, InvalidEmailException

# pylint:  disable=W0707,W0612,R1702,R1710,C2801,W1514
_PATH = os.getcwd()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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

def init_user_collection():
    '''
    Creates and returns a new instance of UserCollection
    '''
    usr_collection = users.UserCollection()
    return usr_collection

def init_status_collection():
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    stat_collection = user_status.UserStatusCollection()
    return stat_collection

def load_users(filename, user_collection):
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
            if row['USER_ID'] in user_collection.database:
                return False
            user_collection.add_user(
                row['USER_ID'],
                row['EMAIL'],
                row['NAME'],
                row['LASTNAME']
            )
    return True


def save_users(filename, user_collection):
    '''
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such as an invalid filename).
    - Otherwise, it returns True.
    '''
    try:
        if isinstance(filename, int):
            return False
        check = filename.split('.')
        if check[1] != 'csv':
            return False
        if isinstance(filename, str):
            with open(filename, 'w+', newline='') as _f:
                writer = csv.DictWriter(_f, fieldnames=['USER_ID',
                                                    'EMAIL',
                                                    'NAME',
                                                    'LASTNAME'])
                writer.writeheader()
                for key,val in user_collection.database.items():
                    writer.writerow({'USER_ID': val.user_id,
                                    'EMAIL': val.email,
                                    'NAME': val.user_name,
                                    'LASTNAME': val.user_last_name})
                    print(f"Row added to {filename}.")
            return True
    except IndexError as i:
        return False


def load_status_updates(filename, status_collection):
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
            if row_num == 0:
                pass
            else:
                status_collection.add_status(
                    row['STATUS_ID'],
                    row['USER_ID'],
                    row['STATUS_TEXT']
                )
    return True


def save_status_updates(filename, status_collection):
    '''
    Saves all statuses in status_collection into a CSV file

    Requirements:
    - If there is an existing file, it will overwrite it.
    - Returns False if there are any errors(such an invalid filename).
    - Otherwise, it returns True.
    '''
    try:
        if isinstance(filename, int):
            return False
        check = filename.split('.')
        if check[1] != 'csv':
            return False
        if isinstance(filename, str):
            with open(filename, 'w+', newline='') as _f:
                writer = csv.DictWriter(_f, fieldnames=['STATUS_ID',
                                                       'USER_ID',
                                                       'STATUS_TEXT'])
                writer.writeheader()
                for key,val in status_collection.database.items():
                    writer.writerow({'STATUS_ID': val.status_id,'USER_ID': val.user_id,
                                    'STATUS_TEXT': val.status_text})
                    print(f"Row added to {filename}.")
            return True
    except IndexError:
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
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
    if not isinstance(user_collection, users.UserCollection):
        raise TypeError("Invalid collection. Please supply a user collection.")
    the_add = user_collection.add_user(user_id, email, user_name, user_last_name)
    return the_add


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    if not EMAIL_REGEX.match(email):
        raise InvalidEmailException('''Email does not match standard email format.
                                    (___@__.com) Please retry.''')
    if not isinstance(user_collection, users.UserCollection):
        raise TypeError("Invalid collection. Please supply a user collection.")
    updated = user_collection.modify_user(user_id, email, user_name, user_last_name)
    return updated


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    deleted = user_collection.delete_user(user_id)
    return deleted


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    the_user = user_collection.search_user(user_id)
    return the_user


def add_status(user_id, status_id, status_text, status_collection):
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
    if isinstance(status_collection, user_status.UserStatusCollection):
        raise TypeError("Invalid collection. Please supply a status collection as final arg.")
    stats = status_collection.add_status(user_id, status_id, status_text)
    return stats


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    if not isinstance(user_id, str):
        raise TypeError('User id field should be a string.')
    if isinstance(status_collection, user_status.UserStatusCollection):
        raise TypeError("Invalid collection. Please supply a status collection as final arg.")
    updated_stats = status_collection.modify_status(status_id, user_id, status_text)
    return updated_stats


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    if not isinstance(status_id, str):
        raise TypeError('Status id field should be a string.')
    if isinstance(status_collection, user_status.UserStatusCollection):
        raise TypeError("Invalid collection. Please supply a status collection as final arg.")
    deleted = status_collection.delete_status(status_id)
    return deleted


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    if not isinstance(status_id, str):
        raise TypeError('Status id field should be a string.')
    if isinstance(status_collection, user_status.UserStatusCollection):
        raise TypeError("Invalid collection. Please supply a status collection as final arg.")
    searched_user = status_collection.search_status(status_id)
    return searched_user
