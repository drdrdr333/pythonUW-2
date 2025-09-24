''' Unit testing - users - for first assignment '''

# pylint:  disable=W0611
import unittest
from mock import Mock
import users
import socialnetwork_model as sndb


# Unit test for Users/UserCollection
class TestUsers(unittest.TestCase):
    ''' Test class for users in
        assignment1
    '''
    def test_multiple_user_create(self):
        ''' Tests multiple creation of users '''
        user_list = []
        new_users = []

        for i in range(10):
            user_list.append(
                [i, f'test{i}@.com', f'u{i}', f'{i}_lastname']
            )
            new_user = users.Users(user_list[i][i-i], user_list[i][i-i+1],
                                user_list[i][i-i+2], user_list[i][i-i+3])
            new_users.append(new_user)
            self.assertEqual(new_users[i].user_id, i)
            self.assertEqual(new_users[i].email, f'test{i}@.com')
            self.assertEqual(new_users[i].user_name, f'u{i}')
            self.assertEqual(new_users[i].user_last_name, f'{i}_lastname')

    def test_user_collection_creation(self):
        ''' Tests creation of user collection db '''
        _uc = users.UserCollection()
        self.assertEqual({}, _uc.database)

    def setUp(self):
        ''' Setup for usercollection simulations:
            we leverage to test the usercollection
            methods
        '''
        self.database = users.UserCollection()
        self.user = users.Users(1, 'test@.com', 't1', 'last1')

    def test_usercollect_add(self):
        ''' Test adding of user,
            attempt to re-add same user
        '''
        sndb.add_user_to_table = Mock(return_value=True)
        ex_true = self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name,
                                        'test')
        sndb.add_user_to_table = Mock(return_value=False)
        ex_false = self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name,
                                        'test')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_user_collect_modify_t_f(self):
        ''' Test true false function of modify '''
        sndb.add_user_to_table = Mock(return_value=True)
        self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name,
                                        'test')
        sndb.modify_user = Mock(return_value=True)
        ex_true = self.database.modify_user(self.user.user_id,
                                            self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name,
                                        'test')
        sndb.modify_user = Mock(return_value=False)
        ex_false = self.database.modify_user(2, 'test', 'name', 'name', 'test')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_user_collect_delete_t_f(self):
        ''' True False functionality of the existence of a user'''
        sndb.add_user_to_table = Mock(return_value=True)
        self.database.add_user(self.user.user_id, self.user.email,
                               self.user.user_name,
                               self.user.user_last_name,
                               'test')
        sndb.delete_user_from_table = Mock(return_value=True)
        ex_true = self.database.delete_user(5, 'test')
        sndb.delete_user_from_table = Mock(return_value=False)
        ex_false = self.database.delete_user(3, 'test')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_user_collect_search_fault(self):
        ''' If user collect search returns a None/null user '''
        sndb.add_user_to_table = Mock(return_value=True)
        self.database.add_user(self.user.user_id, self.user.email,
                               self.user.user_name,
                               self.user.user_last_name,
                               'test')
        sndb.search_user_in_table = Mock(return_value=True)
        expected = self.database.search_user(2, 'test')
        self.assertTrue(expected)
