'''
Classes for user information for the social network project
'''
# pylint: disable=R0903,R0913,W0613
import logging
import mongo_connect as mc

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
        added = mc.insert_to_db(new_user)
        return added

    def modify_user(self, user_id, new_email, new_user_name,
                    new_user_last_name, the_db):
        '''
        Modifies an existing user
        '''
        the_user = Users(user_id, email=new_email,
                         user_name=new_user_name,
                         user_last_name=new_user_last_name)
        updated = mc.modify_object_in_db(the_user)
        return updated

    def delete_user(self, user_id, the_db):
        '''
        Deletes an existing user
        '''
        deleted = mc.delete_user_in_db(user_id)
        return deleted

    def search_user(self, user_id, the_db):
        '''
        Searches for user data
        '''
        found = mc.search_user_in_db(user_id)
        return found
