'''
    Unit testing - status - for first assignment
'''

# pylint:  disable=W0611
import unittest
from mock import Mock, MagicMock
import user_status
# Unit

 test for User Status
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
        ex_true = self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        ex_false = self.collection.add_status(self.statuses[0].status_id,
                                              self.statuses[0].user_id,
                                              'false!!!')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_add_status(self):
        ''' Proper add status functionality '''
        trues = []
        for i in range(10):
            ex_true = self.collection.add_status(self.statuses[i].status_id,
            self.statuses[i].user_id, self.statuses[i].status_text)
            trues.append(ex_true)
        expected = [True]*10
        self.assertSequenceEqual(trues, expected)

    def test_modify_t_f(self):
        ''' Test True False if status in db '''
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        ex_true = self.collection.modify_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            'new text test')
        ex_false = self.collection.modify_status(11, 11, 'test')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_modify(self):
        ''' Test modify functionality '''
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        self.collection.modify_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            'new text test')
        self.assertEqual(self.collection.database[0].status_text,
                        'new text test')
        self.collection.modify_status = MagicMock(('doesnt matter'))
        self.collection.modify_status(self.statuses[1].status_id,
                                            self.statuses[1].user_id,
                                            'new text test 2')
        self.collection.modify_status.assert_called_with(1, 1,
                                                        'new text test 2')

    def test_delete_t_f(self):
        ''' Tests True False of user status delete '''
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        ex_true = self.collection.delete_status(self.statuses[0].status_id)
        ex_false = self.collection.delete_status(16)
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_delete(self):
        ''' Tests user collect delete functionality '''
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        self.collection.delete_status(self.statuses[0].status_id)
        self.assertEqual(self.collection.database, {})
        self.collection.delete_status = MagicMock('delete')
        self.collection.delete_status((65))
        self.collection.delete_status.assert_called_with(65)

    def test_search_t_f(self):
        ''' Tests True False of user status delete '''
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        ex_true = self.collection.search_status(self.statuses[0].status_id)
        ex_false = self.collection.search_status(16)
        self.assertTrue(ex_true)
        self.assertEqual(None, ex_false.status_id)
        self.assertEqual(None, ex_false.user_id)
        self.assertEqual(None, ex_false.status_text)

    def test_search(self):
        ''' Tests user collect delete functionality '''
        self.collection.add_status(self.statuses[0].status_id,
                                            self.statuses[0].user_id,
                                            self.statuses[0].status_text)
        expected = self.collection.search_status(self.statuses[0].status_id)
        self.assertEqual(self.collection.database[0].status_id,
                        expected.status_id)
        self.assertEqual(self.collection.database[0].user_id,
                        expected.user_id)
        self.assertEqual(self.collection.database[0].status_text,
                        expected.status_text)
        self.collection.search_status = MagicMock('delete')
        self.collection.search_status((65))
        self.collection.search_status.assert_called_with(65)
