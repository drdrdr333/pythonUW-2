'''
classes to manage the user status messages
'''
# pylint: disable=R0903
import logging

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
        logging.info("SUCCESS: User status collection created.")

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        if status_id in self.database:
            # Rejects new status if status_id already exists
            logging.warning("Status id: %s already exists in database", user_id)
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        logging.info("SUCCESS: Status id: %s added", status_id)
        self.database[status_id] = new_status
        return True

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        if status_id not in self.database:
            # Rejects update is the status_id does not exist
            logging.warning("Status id: %s not found in database", user_id)
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        logging.info("SUCCESS: Status id: %s modified", status_id)
        return True

    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        if status_id not in self.database:
            # Fails if status does not exist
            logging.warning("Status id: %s not found in database", status_id)
            return False
        del self.database[status_id]
        logging.info("SUCCESS: Status id: %s deleted", status_id)
        return True

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        if status_id not in self.database:
            # Fails if the status does not exist
            logging.warning("Status id: %s not found in database", status_id)
            return UserStatus(None, None, None)
        logging.info("SUCCESS: Status id: %s searched & found", status_id)
        return self.database[status_id]
