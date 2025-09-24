'''
Provides a basic frontend
'''

#pylint: disable=C0201

import sys
import logging
from datetime import date
import main
import pandas_chunks as pc
import mongo_connect as mc

the_date = date.today()
date_items = str(the_date).split('-')
yr = date_items[0]
month = date_items[1]
day = date_items[2]

LOG_F = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_F)
file_handle = logging.FileHandler(f"log_{month}_{day}_{yr}.log")
file_handle.setLevel(logging.INFO)
file_handle.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handle)

def get_file_name():
    '''Gets name of file in string form '''
    filename = input("Enter filename:\t")
    return filename

def get_file_count():
    ''' Gets the amount of files '''
    amount = input("How many files do you want to upload?\t")
    number = int(amount)
    return number

def begin_upload(some_list=None):
    ''' Kicks off data upload process '''
    if some_list is None:
        ##not sure yet - raise exception?
        print(some_list, "is none")
    elif not some_list:
        print("list is empty")
    else:
        amt = len(some_list)
        for file in some_list:
            uploader = main.get_file(file)
            pc.import_csv_in_chunks(uploader, amt)

def load_users():
    '''
    Loads user accounts from a file
    '''
    the_file = get_file_name()
    pc.import_csv_in_chunks(the_file)

def load_csvs():
    ''' Gets the amount of files to add
        as well as their names
    '''
    files_to_upload = []
    files = get_file_count()

    while files > 0:
        name = get_file_name()
        files_to_upload.append(name)
        files = files-1
    begin_upload(files_to_upload)

def load_status_updates():
    '''
    Loads status updates from a file
    '''
    print("""****NOTE****\nUsers must be added prior
          to status uploads.""")
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)

def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")

def update_user():
    '''
    Updates information for an existing user
    '''
    print("""\t\t*** Warning ***\n\t\tYou are allowed to update
        \teverything but the users ID. Please supply
        \tyour updates to the respective fields.\n
        We will use the user ID provided to find the user.""")
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name,
                            user_last_name,
                            user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")

def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if not result['User ID']:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['User ID']}")
        print(f"Email: {result['User Email']}")
        print(f"Name: {result['User Name']}")
        print(f"Last name: {result['User Last Name']}")

def delete_user():
    '''
    Deletes user from the database
    '''
    print("""\t****WARNING****\n
        This action will delete the user and all
        related statuses.""")
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")

def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")

def update_status():
    '''
    Updates information for an existing status
    '''
    print("""\t\t*** Warning ***\n\t\tYou are allowed to update
        \teverything but the users ID. Please supply
        \tyour updates to the respective fields.\n
        We will use the user ID provided to find the user.""")
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")

def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result['Status ID']:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result['User ID']}")
        print(f"Status ID: {result['Status ID']}")
        print(f"Status Tesxt: {result['Status Text']}")

def delete_status():
    '''
    Deletes status from the database
    '''
    print("""\t****WARNING****\n
        This action will delete all
        related statuses.""")
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")

def quit_program():
    '''
    Quits program
    '''
    sys.exit()

if __name__ == '__main__':
    user_collection = mc.db
    status_collection = mc.db
    menu_options = {
        'A': load_csvs,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load csvs
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            Q: Quit

                            Please enter your choice: """)
        selection = user_selection.lower()
        lowers = [key.lower() for key in menu_options.keys()]
        if user_selection.upper() in menu_options or selection in lowers:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
