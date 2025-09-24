'''
Provides a basic frontend
'''

#pylint: disable=C0201,W0612

import sys
import logging
from datetime import date
import main

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


def generator_for_statuses(the_length, the_data):
    '''
        generator for all of a users
        statuses
    '''
    start = 0
    while start < the_length:
        yield the_data[start]['st_status_text']
        start += 1

def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename)


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename)


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
                         user_last_name):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    print("""\t\t*** Warning ***\n\t\tYou are allowed to update
\teverything but the users ID. Please supply
\tyour updates to the respective fields.""")
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name,
                            user_last_name):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id)
    if not result:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['t_user_id']}")
        print(f"Email: {result['t_user_email']}")
        print(f"Name: {result['t_user_name']}")
        print(f"Last name: {result['t_user_last_name']}")


def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id):
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
    if not main.add_status(user_id, status_id, status_text):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id)
    if not result['st_status_id']:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result['st_user_id']}")
        print(f"Status ID: {result['st_status_id']}")
        print(f"Status text: {result['st_status_text']}")


def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")

def search_all_status_updates():
    '''
    Dependant upon other modules - 
    if a user has a single or multiple statuses
    a generator is created and iterated over for every
    status
    '''
    user_id = input("Enter user id to search:\t")
    result = main.search_status_updates_by_user(user_id)
    if result:
        print(f"There are {len(result)} statuses for {user_id}")
        gen = generator_for_statuses(len(result), result)
        for i in range(len(result)):
            try:
                question = input("Would you like to see the next update?(Y/N):\t")
                if question.lower() == 'y':
                    print(next(gen))
                elif question.lower() == 'n':
                    break
            except StopIteration:
                logger.info("Last update for the user...")
        print("Last update for the user...returning to menu.")
        return True
    return False

def filter_status_by_string():
    '''
    Dependant upon other modules -
    if the text supplied in the execution
    of this function has stautes that match
    it, this function iterates thru them,
    else returns false
    '''
    search_txt = input("Enter the string to search for:\t")
    result = main.filter_status_by_string(search_txt)
    if result:
        try:
            res = iter(result)
            for i in res:
                question = input("Review the next status? (Y/N):\t")
                if question.lower() == 'y':
                    print(f"{i['st_status_text']}")
                    to_delete = input("Delete this status? (Y/N):\t")
                    if to_delete.lower() == 'y':
                        main.delete_status(i['st_status_id'])
                    else:
                        continue
                elif question.lower() == 'n':
                    break
        except StopIteration:
            logger.info("Last status that meets your search...")
        print("Exit...returning to menu.")
        return True
    return print("No items returned...")

def show_flagged_statuses():
    '''
    Same as above
    Prints all statuses matching the text
    in a single container
    '''
    search_txt = input("Enter the string to search for:\t")
    result = main.filter_status_by_string(search_txt)
    final = [(row['st_user_id'], row['st_status_text']) for row in result]
    for row in final:
        print(row)

def quit_program():
    '''
    Quits program
    '''
    sys.exit()

if __name__ == '__main__':
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': search_all_status_updates,
        'M': filter_status_by_string,
        'N': show_flagged_statuses,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user from file
                            B: Load status from file
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            L: Search all statuses for a user
                            M: Search all statuses matching a string
                            N: Show all flagged statuses
                            Q: Quit

                            Please enter your choice: """)
        selection = user_selection.lower()
        lowers = [key.lower() for key in menu_options.keys()]
        if user_selection.upper() in menu_options or selection in lowers:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
