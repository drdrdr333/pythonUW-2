''' Unit testing - users - for first assignment '''

# pylint:  disable=W0611
import unittest
import users


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
        ex_true = self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name)
        ex_false = self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name)
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_user_collect_db_data(self):
        ''' Test if database saves exact user
            referential memory will be different
            so we que off attributes
        '''
        self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name)
        self.assertEqual(self.database.database[1].user_id,
                        self.user.user_id)
        self.assertEqual(self.database.database[1].user_last_name,
                        self.user.user_last_name)

    def test_user_collect_modify_t_f(self):
        ''' Test true false function of modify '''
        self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name)
        ex_true = self.database.modify_user(self.user.user_id,
                                            self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name)
        ex_false = self.database.modify_user(2, 'test', 'name', 'name')
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_user_collect_modify_update(self):
        ''' Proper modification of attributes '''
        self.database.add_user(self.user.user_id, self.user.email,
                                        self.user.user_name,
                                        self.user.user_last_name)
        self.database.modify_user(self.user.user_id, 'test_update_email',
                                'up_u_name', 'up_l_name')
        self.assertEqual(self.database.database[1].email,
                        'test_update_email')
        self.assertEqual(self.database.database[1].user_name, 'up_u_name')
        self.assertEqual(self.database.database[1].user_last_name, 'up_l_name')

    def test_user_collect_delete_t_f(self):
        ''' True False functionality of the existence of a user'''
        self.database.add_user(self.user.user_id, self.user.email,
                               self.user.user_name,
                               self.user.user_last_name)
        ex_true = self.database.delete_user(self.database.database[1].user_id)
        ex_false = self.database.delete_user(3)
        self.assertTrue(ex_true)
        self.assertFalse(ex_false)

    def test_user_collect_delete(self):
        ''' Delete functionality works proper '''
        trues = []
        for i in range(10):
            self.database.add_user(self.user.user_id+i,
                                   f'{self.user.email}{i}',
                                   f'{self.user.user_name}{i}',
                                   f'{self.user.user_last_name}{i}')
        for i in range(10):
            ex = self.database.delete_user(self.database.database[i+1].user_id)
            trues.append(ex)
        compare = [True]*10
        self.assertSequenceEqual(trues, compare)

    def test_user_collect_search_fault(self):
        ''' If user collect search returns a None/null user '''
        self.database.add_user(self.user.user_id, self.user.email,
                               self.user.user_name,
                               self.user.user_last_name)
        expected = self.database.search_user(2)
        self.assertEqual(self.database.search_user(3).user_id,
                         expected.user_id)
        self.assertEqual(self.database.search_user(3).email,
                         expected.email)
        self.assertEqual(self.database.search_user(3).user_name,
                         expected.user_name)
        self.assertEqual(self.database.search_user(3).user_last_name,
                         expected.user_last_name)

    def test_user_collect_search(self):
        ''' If user collect search returns 1-1 our user
            even the reference of the object
        '''
        self.database.add_user(self.user.user_id, self.user.email,
                               self.user.user_name,
                               self.user.user_last_name)
        expected = self.database.search_user(self.database.database[1].user_id)
        self.assertEqual(self.database.database[1].email, expected.email)
        self.assertEqual(self.database.database[1], expected)
