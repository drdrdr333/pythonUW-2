'''
classes to manage the user status messages
'''
# pylint: disable=R0903,W0613
import logging
import mongo_connect as mc

LOGGER = logging.getLogger(__name__)

class UserStatus():
    '''
    class to hold status message data
    '''
    def __init__(self, status_id, user_id, status_text):
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''
    def __init__(self):
        self.database = {}

    def add_status(self, status_id, user_id, status_text, the_db):
        '''
        add a new status message to the collection
        '''
        new_status = UserStatus(status_id, user_id, status_text)
        added = mc.insert_to_db(new_status)
        return added

    def modify_status(self, status_id, user_id, status_text, the_db):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        to_update = UserStatus(status_id, user_id, status_text)
        updated = mc.modify_object_in_db(to_update)
        return updated

    def delete_status(self, status_id, the_db):
        '''
        deletes the status message with id, status_id
        '''
        deleted = mc.delete_status_in_db(status_id)
        return deleted

    def search_status(self, status_id, the_db):
        '''
        Find and return a status message by its status_id
        '''
        searched = mc.search_status_in_db(status_id)
        return searched
