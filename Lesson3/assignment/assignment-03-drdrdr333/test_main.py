'''
    Unit testing for first assignment
'''

# pylint:  disable=W0611
import unittest
from mock import Mock, MagicMock, patch
import main
from exceptions import NonFileExtension, InvalidEmailException
import users
import user_status
import io
from contextlib import redirect_stdout


# Tests for main/integrations
class TestMain(unittest.TestCase):
    ''' Unit test of main functionality
        of the first assignment
    '''
    def test_init_usr_collect(self):
        '''UserCollection object created from main proper'''
        expected = main.init_user_collection()
        self.assertEqual({}, expected.database)
        with self.assertRaises(TypeError):
            main.init_user_collection(111)

    def test_init_sts_collect(self):
        ''' StatusCollection object created from main proper'''
        expected = main.init_status_collection()
        self.assertEqual({}, expected.database)

    def test_file_find(self):
        ''' Test of file search '''
        with self.assertRaises(TypeError):
            main.get_file(111111)
        with self.assertRaises(FileNotFoundError):
            main.get_file('hello.txt')
        with self.assertRaises(NonFileExtension):
            main.get_file('hello')
        expected = main.get_file('accounts.csv')
        self.assertEqual(expected, 'accounts.csv')

    def test_load_users(self):
        ''' Test of loading users '''
        ex = main.load_users('accounts.csv', main.init_user_collection())
        self.assertTrue(ex)
        ex_f = main.load_users('t.csv', main.init_user_collection())
        self.assertFalse(ex_f)
        added = users.UserCollection()
        added.add_user('evmiles97', 'test', 'test', 'test')
        self.assertFalse(main.load_users('accounts.csv', added))

    def test_save_users(self):
        ''' Test to save users '''
        collect = main.init_user_collection()
        collect.add_user = {1,'test@', 'eee', 'fff'}
        expected = main.save_users('new_accounts.csv', collect)
        self.assertTrue(expected)
        ex_f = main.save_users('nnnn', collect)
        self.assertFalse(ex_f)
        ex_f_ = main.save_users(111, collect)
        self.assertFalse(ex_f_)
        ex_f__ = main.save_users('nnnn.txt', collect)
        self.assertFalse(ex_f__)

# Part unit part integration test for main
# to practice mocking, patching
class TestMainMock(unittest.TestCase):
    ''' For mocking '''
    def setUp(self):
        ''' For mocking objects '''
        self.st_collection = main.init_status_collection()
        self.user_collection = main.init_user_collection()

    def test_save_users_writer(self):
        ''' assist to test_save_users line 53 '''
        coll = self.user_collection
        coll.add_user(1, 1, 1, 1)
        o = io.StringIO()
        with redirect_stdout(o):
            main.save_users('l.csv', self.user_collection)
        output = o.getvalue()
        self.assertEqual(output, 'Row added to l.csv.\n')

    def test_load_status(self):
        ''' Proper status load to status collection '''
        self.assertEqual(main.load_status_updates('status_updates.csv', self.st_collection), True)
        self.assertEqual(main.load_status_updates('t.csv', self.st_collection), False)

    def test_save_status_updates(self):
        ''' Test of save status into a csv '''
        coll = self.st_collection
        coll.add_status(1,1,'testtesttest')
        self.assertFalse(main.save_status_updates(111, coll))
        self.assertFalse(main.save_status_updates('t.txt', coll))
        self.assertFalse(main.save_status_updates('tttttttt', coll))
        #testing with patch, this could
        #have leveraged self above as well
        with patch('main.init_status_collection') as st:
            st.return_value={}
            self.assertTrue(main.save_status_updates('tst_status_up.csv', st))

    def test_csv_writer_status(self):
        '''Test writerow - needed on coverage '''
        coll = self.st_collection
        coll.add_status(1, 1, 'testtesttest')
        f = io.StringIO()
        with redirect_stdout(f):
            main.save_status_updates('tst_status_up.csv', self.st_collection)
        out = f.getvalue()
        self.assertEqual(out, 'Row added to tst_status_up.csv.\n')

    def test_main_add_user(self):
        ''' Test of main add user - leverage UserCollection '''
        coll = self.user_collection
        ex_true = coll.add_user(1,1,1,1)
        self.assertEqual(main.add_user("2","testtest@test.com",2,2, coll), ex_true)
        with self.assertRaises(TypeError):
            main.add_user(1, 'hello@h.com', 't', 't', coll)
        with self.assertRaisesRegex(TypeError, "Invalid collection. Please supply a user collection as the final argument."):
            main.add_user("1", 'hello@h.com', 't', 't', "today")
        with self.assertRaises(InvalidEmailException):
            main.add_user("string", "1111", "t", "t", coll)

    def test_update_user(self):
        '''Test of main.update_user - leverage UserCollection '''
        res = (True, False)
        expected = [True, False]
        coll = self.user_collection
        coll.add_user(1,1,1,1)
        with patch("users.UserCollection.modify_user") as mu:
            mu.return_value = res[0]
            self.assertEqual(main.update_user('1', 'update@up.com', 2, 2, coll), expected[0])
            mu.return_value = res[1]
            self.assertEqual(main.update_user('3', 'test@test.com', 4, 4, coll), expected[1])
            mu.assert_called_with('3', 'test@test.com', 4, 4)
        with self.assertRaises(TypeError):
            main.update_user(3, 'test@test.com', 4, 4, coll)
        with self.assertRaises(InvalidEmailException):
            main.update_user('3', 'testtest.com', 4, 4, coll)
        with self.assertRaisesRegex(TypeError, "Invalid collection. Please supply a user collection as the final argument."):
            main.update_user('3', 'test@test.com', 4, 4, "today")

    def test_main_delete_users(self):
        ''' Test of main.delete_user - leverage UserCollection'''
        res = (True, False)
        expected = (True, False)
        coll = self.user_collection
        coll.add_user('1', 1, 1, 1)
        with patch("users.UserCollection.delete_user") as du:
            du.return_value = res[0]
            self.assertEqual(main.delete_user('1', coll), expected[0])
            du.return_value = res[1]
            self.assertEqual(main.delete_user('2', coll), expected[1])
            du.assert_called_with('2')
        with self.assertRaises(TypeError):
            main.delete_user(1, coll)

    def test_main_search_users(self):
        ''' Test of main.search_user - leverage UserCollection '''
        res = ('test1', 'test2')
        expected = (users.Users('test1', 'test@test.com', 12, 12), users.Users(None, None, None, None))
        coll = self.user_collection
        coll.add_user('test1', 'test@test.com', 12, 12)
        with patch('users.UserCollection.search_user') as su:
            su.return_value = expected[0]
            self.assertEqual(main.search_user(res[0], coll), expected[0])
            su.return_value = expected[1]
            self.assertEqual(main.search_user(res[1], coll), expected[1])
        with self.assertRaises(TypeError):
            main.search_user(1, coll)

    def test_main_add_status(self):
        ''' Test of main.add_status - leverage UserStatusCollection '''
        coll = self.st_collection
        ex_true = coll.add_status('1','1','1')
        self.assertEqual(main.add_status("2","test", "test", coll), ex_true)
        with self.assertRaises(TypeError):
            main.add_status(1, 'hello@h.com', 't', coll)
        with self.assertRaisesRegex(TypeError, "Invalid collection. Please supply a status collection as the final argument."):
            main.add_status("1", 'hello@h.com', 't', "today")

    def test_main_mod_status(self):
        ''' Test of main.update_stats - leverage UserStatusCollection '''
        res = (True, False)
        expected = (True, False)
        coll = self.st_collection
        ex_true = coll.add_status('1','1','1')
        with patch("user_status.UserStatusCollection.modify_status") as ms:
            ms.return_value = res[0]
            self.assertEqual(main.update_status('1', '1', '1', coll), expected[0])
            ms.return_value = res[1]
            self.assertEqual(main.update_status('2', '1', '1', coll), expected[1])
        with self.assertRaises(TypeError):
            main.update_status('hello@h.com', 1, 't', coll)
        with self.assertRaisesRegex(TypeError, "Invalid collection. Please supply a status collection as the final argument."):
            main.update_status("1", 'hello@h.com', 't', "today")

    def test_main_delete_status(self):
        ''' Test main.delete_status - leverage UserStatusCollection '''
        res = (True, False)
        expected = (True, False)
        coll = self.st_collection
        ex_true = coll.add_status('1','1','1')
        with patch('user_status.UserStatusCollection.delete_status') as ds:
            ds.return_value = res[0]
            self.assertEqual(main.delete_status('1', coll), expected[0])
            ds.return_value = res[1]
            self.assertEqual(main.delete_status('33', coll), expected[1])
        with self.assertRaises(TypeError):
            main.delete_status(1, coll)
        with self.assertRaisesRegex(TypeError, "Invalid collection. Please supply a status collection as the final argument."):
            main.delete_status("1", "today")

    def test_main_search_user(self):
        ''' Test of main.search_user - leverage UserStatusCollection '''
        expected = (user_status.UserStatus('statid1', 'usid1', 'test1'), user_status.UserStatus(None, None, None) )
        coll = self.st_collection
        ex_true = coll.add_status('statid1', 'usid1', 'test1')
        with patch('user_status.UserStatusCollection.search_status') as ss:
            ss.return_value = expected[0]
            self.assertEqual(main.search_status('statid1', coll), expected[0])
            ss.return_value = expected[1]
            self.assertEqual(main.search_status('statid22', coll), expected[1])
            ss.assert_called_with('statid22')
        with self.assertRaises(TypeError):
            main.search_status(22, coll)
        with self.assertRaisesRegex(TypeError, "Invalid collection. Please supply a status collection as the final argument."):
            main.search_status("1", "today")

# Unit test for Users
class TestUnitUsuers(unittest.TestCase):
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

# Unit test for User Status
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
