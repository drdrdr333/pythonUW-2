'''
Classes for user information for the social network project
'''
# pylint: disable=R0903
import logging

LOGGER = logging.getLogger(__name__)

class Users():
    '''
    Contains user information
    '''

    def __init__(self, user_id, email, user_name, user_last_name):
        self.user_id = user_id
        self.email = email
        self.user_name = user_name
        self.user_last_name = user_last_name


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self):
        self.database = {}
        logging.info("SUCCESS: User collection created.")

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        if user_id in self.database:
            # Rejects new status if status_id already exists
            logging.warning("%s already in database bad add_user attempt.", user_id)
            return False
        new_user = Users(user_id, email, user_name, user_last_name)
        self.database[user_id] = new_user
        logging.info("SUCCESS: User id: %s added", user_id)
        return True

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        if user_id not in self.database:
            logging.warning("%s not in database bad modify_user attempt.", user_id)
            return False
        self.database[user_id].email = email
        self.database[user_id].user_name = user_name
        self.database[user_id].user_last_name = user_last_name
        logging.info("""SUCCESS: User id: %s modified. EMAIL: %s,
                     U_NAME: %s, LASTNAME: %s""",
                     user_id, email, user_name, user_last_name)
        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        if user_id not in self.database:
            logging.warning("%s not in database bad delete attempt.", user_id)
            return False
        del self.database[user_id]
        logging.info("SUCCESS: User id: %s deleted", user_id)
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        if user_id not in self.database:
            logging.warning("%s not in database bad search attempt.", user_id)
            return Users(None, None, None, None)
        logging.info("SUCCESS: User id: %s searched for and found.", user_id)
        return self.database[user_id]
