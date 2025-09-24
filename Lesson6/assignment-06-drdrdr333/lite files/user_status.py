'''
classes to manage the user status messages
'''
# pylint: disable=R0903,W1203
import logging
import socialnetwork_model as sndb

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
        added = sndb.add_st_to_table(the_db, new_status)
        return added

    def modify_status(self, status_id, user_id, status_text, the_db):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        to_update = UserStatus(status_id, user_id, status_text)
        updated = sndb.modify_status(the_db, to_update, new_status_txt=status_text)
        return updated

    def delete_status(self, status_id, the_db):
        '''
        deletes the status message with id, status_id
        '''
        deleted = sndb.delete_status_from_table(the_db, status_id)
        logging.info("SUCCESS: Status id: %s deleted", status_id)
        return deleted

    def search_status(self, status_id, the_db):
        '''
        Find and return a status message by its status_id
        '''
        searched = sndb.search_status_in_table(the_db, status_id)
        return searched

    def search_all_status_updates(self, user_id, the_db):
        '''
        Find and return all the statuses
        created by a user
        '''
        the_statuses = sndb.search_all_status_updates(the_db, user_id)
        if the_statuses:
            return the_statuses
        logging.info(f"No statuses found for user {user_id}...")
        return False

    def filter_status_by_string(self, text, the_db):
        '''
        Find and return all status text
        within the database that matches
        the supplied 'text' parameter
        '''
        statuses = sndb.filter_status_by_string(the_db, text)
        if statuses:
            return statuses
        logging.info(f"No matching statuses found for text: {text}...")
        return False
