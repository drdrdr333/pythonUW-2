'''
Classes for user information for the social network project
'''
# pylint: disable=R0903,R0913
import logging
import socialnetwork_model as sndb

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

    def add_user(self, user_id, email, user_name, user_last_name, the_db):
        '''
        Adds a new user to the collection
        '''
        new_user = Users(user_id, email, user_name, user_last_name)
        added = sndb.add_user_to_table(the_db, new_user)
        return added

    def modify_user(self, user_id, email, user_name, user_last_name, the_db):
        '''
        Modifies an existing user
        '''
        the_user = Users(user_id, email, user_name, user_last_name)
        updated = sndb.modify_user(the_db, the_user, new_email=email,
                                   new_u_name=user_name, new_l_name=user_last_name)
        return updated

    def delete_user(self, user_id, the_db):
        '''
        Deletes an existing user
        '''
        deleted = sndb.delete_user_from_table(the_db, user_id)
        logging.info("SUCCESS: User id: %s deleted", user_id)
        return deleted

    def search_user(self, user_id, the_db):
        '''
        Searches for user data
        '''
        found = sndb.search_user_in_table(the_db, user_id)
        return found
