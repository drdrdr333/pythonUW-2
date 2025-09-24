'''
    Unit testing - status - for first assignment
'''

# pylint:  disable=W0611
import unittest
from mock import Mock, MagicMock
import user_status
import socialnetwork_model as sndb

# Unittest for User Status
class TestUserStatus(unittest.TestCase):
    ''' Test class for user status in
        assignment 1
    '''
    def test_user_status_create(self):
        ''' Proper creation of user status
            different referential object
            same attributes
        '''
        user_stats = []
        new_stats = []

        for i in range(10):
            user_stats.append([user_status.UserStatus(
                i,
                i,
                f'test {i}')]
            )
            new_stats.append(user_status.UserStatus(
                user_stats[i][i-i].status_id,
                            user_stats[i][i-i].user_id,
                            user_stats[i][i-i].status_text))
            self.assertEqual(new_stats[i].status_id,
                            user_stats[i][i-i].status_id)
            self.assertEqual(new_stats[i].user_id,
                            user_stats[i][i-i].user_id)
            self.assertEqual(new_stats[i].status_text,
                            user_stats[i][i-i].status_text)

    def setUp(self):
        ''' Setup for mock user status objects
            and collection object
        '''
        self.status_id = int()
        self.user_id = int()
        self.status_text = str()
        self.statuses = [user_status.UserStatus(i,
                                i, f'status{i}') for i in range(10)]
        self.collection = user_status.UserStatusCollection()

    def test_add_status_t_f(self):
        ''' Proper True False if status exists'''
        self.statuses[0].status_id = Mock(return_value=1)
        self.statuses[0].user_id = Mock(return_value=1)
        self.statuses[0].status_text = Mock(return_value='some txt')
        sndb.add_st_to_table = Mock(return_value=True)
        ex_true = self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text,
                                            'test')
        self.assertTrue(ex_true)
        sndb.add_st_to_table = Mock(return_value=False)
        ex_false = self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text,
                                            'test')
        self.assertFalse(ex_false)

    def test_modify_t_f(self):
        ''' Test True False if status in db '''
        sndb.add_st_to_table = Mock(return_value=True)
        sndb.modify_status = Mock(return_value=True)
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text,
                                            'test')
        ex_true = self.collection.modify_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            'new text test',
                                            'test')
        sndb.add_st_to_table = Mock(return_value=False)
        sndb.modify_status = Mock(return_value=False)
        ex_false = self.collection.modify_status(11, 11, 'the text', 'test')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_modify(self):
        ''' Test modify functionality '''
        sndb.add_st_to_table = Mock(return_value=True)
        sndb.modify_status = Mock(return_value=True)
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text,
                                            'test')
        self.collection.modify_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            'new text test',
                                            'test')
        self.collection.modify_status = MagicMock(('doesnt matter'))
        self.collection.modify_status(self.statuses[1].status_id,
                                            self.statuses[1].user_id,
                                            'new text test 2')
        self.collection.modify_status.assert_called_with(1, 1,
                                                        'new text test 2')

    def test_delete_t_f(self):
        ''' Tests True False of user status delete '''
        sndb.add_st_to_table = Mock(return_value=True)
        sndb.delete_status_from_table = Mock(return_value=True)
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text,
                                            'test')
        ex_true = self.collection.delete_status(self.statuses[0].status_id, 'test')
        sndb.delete_status_from_table.assert_called_with('test', self.statuses[0].status_id)
        sndb.delete_status_from_table = Mock(return_value=False)
        ex_false = self.collection.delete_status(16, 'test')
        sndb.delete_status_from_table.assert_called_with('test', 16)
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_search_t_f(self):
        ''' Tests True False of user status delete '''
        sndb.add_st_to_table = Mock(return_value=True)
        sndb.search_status_in_table = Mock(return_value=True)
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text,
                                            'test')
        ex_true = self.collection.search_status(self.statuses[0].status_id, 'test')
        sndb.search_status_in_table.assert_called_with('test', self.statuses[0].status_id)
        sndb.search_status_in_table = Mock(return_value=False)
        ex_false = self.collection.search_status(16, 'test')
        sndb.search_status_in_table.assert_called_with('test', 16)
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)
