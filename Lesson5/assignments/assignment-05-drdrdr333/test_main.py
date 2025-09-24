'''
    Integration testing from main
'''

# pylint:  disable=W0611
import unittest
from mock import Mock, MagicMock, patch
import main
import mongo_connect as mc
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
        ex = main.load_users('accounts.csv')
        self.assertTrue(ex)
        added = users.UserCollection()
        added.add_user('evmiles97', 'test', 'test', 'test', mc.db)
        self.assertTrue(main.load_users('test_users.csv', added))

# # Part unit part integration test for main
# # to practice mocking, patching
class TestMainMock(unittest.TestCase):
    ''' For mocking '''
    def setUp(self):
        ''' For mocking objects '''
        self.st_collection = user_status.UserStatusCollection()
        self.user_collection = users.UserCollection()

    def test_load_status(self):
        ''' Proper status load to status collection '''
        self.assertEqual(main.load_status_updates('test_status.csv', self.st_collection), True)
        self.assertEqual(main.load_status_updates('t.csv', self.st_collection), False)

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
        ex_true = coll.add_user(1,1,1,1, mc.db)
        self.assertEqual(main.add_user("2","testtest@test.com",2,2, mc.db), ex_true)
        with self.assertRaises(TypeError):
            main.add_user(1, 'hello@h.com', 't', 't', coll)
        with self.assertRaises(InvalidEmailException):
            main.add_user("string", "1111", "t", "t", coll)

    def test_update_user(self):
        '''Test of main.update_user - leverage UserCollection '''
        res = (True, False)
        expected = [True, False]
        coll = self.user_collection
        coll.add_user(1,1,1,1, mc.db)
        with patch("users.UserCollection.modify_user") as mu:
            mu.return_value = res[0]
            self.assertEqual(main.update_user('1', 'update@up.com', 2, 2, mc.db), expected[0])
            mu.return_value = res[1]
            self.assertEqual(main.update_user('3', 'test@test.com', 4, 4, mc.db), expected[1])
            mu.assert_called_with('3', 'test@test.com', 4, 4, mc.db)
        with self.assertRaises(TypeError):
            main.update_user(3, 'test@test.com', 4, 4, coll)
        with self.assertRaises(InvalidEmailException):
            main.update_user('3', 'testtest.com', 4, 4, coll)
            main.update_user('3', 'test@test.com', 4, 4, "today")

    def test_main_delete_users(self):
        ''' Test of main.delete_user - leverage UserCollection'''
        res = (True, False)
        expected = (True, False)
        coll = self.user_collection
        coll.add_user('1', 1, 1, 1, mc.db)
        with patch("users.UserCollection.delete_user") as du:
            du.return_value = res[0]
            self.assertEqual(main.delete_user('1', mc.db), expected[0])
            du.return_value = res[1]
            self.assertEqual(main.delete_user('2', mc.db), expected[1])
            du.assert_called_with('2', mc.db)
        with self.assertRaises(TypeError):
            main.delete_user(1, mc.db)

    def test_main_search_users(self):
        ''' Test of main.search_user - leverage UserCollection '''
        res = ('test1', 'test2')
        expected = (users.Users('test1', 'test@test.com', 12, 12), users.Users(None, None, None, None))
        coll = self.user_collection
        coll.add_user('test1', 'test@test.com', 12, 12, mc.db)
        with patch('users.UserCollection.search_user') as su:
            su.return_value = expected[0]
            self.assertEqual(main.search_user(res[0], mc.db), expected[0])
            su.return_value = expected[1]
            self.assertEqual(main.search_user(res[1], mc.db), expected[1])
        with self.assertRaises(TypeError):
            main.search_user(1, coll)

    def test_main_add_status(self):
        ''' Test of main.add_status - leverage UserStatusCollection '''
        coll = self.st_collection
        ex_true = coll.add_status('1','1','1', mc.db)
        self.assertEqual(main.add_status("2","test", "test", mc.db), ex_true)
        with self.assertRaises(TypeError):
            main.add_status(1, 'hello@h.com', 't', mc.db)

    def test_main_mod_status(self):
        ''' Test of main.update_stats - leverage UserStatusCollection '''
        res = (True, False)
        expected = (True, False)
        coll = self.st_collection
        ex_true = coll.add_status('1','1','1', mc.db)
        with patch("user_status.UserStatusCollection.modify_status") as ms:
            ms.return_value = res[0]
            self.assertEqual(main.update_status('1', '1', '1', mc.db), expected[0])
            ms.return_value = res[1]
            self.assertEqual(main.update_status('2', '1', '1', mc.db), expected[1])
        with self.assertRaises(TypeError):
            main.update_status('hello@h.com', 1, 't', mc.db)

    def test_main_delete_status(self):
        ''' Test main.delete_status - leverage UserStatusCollection '''
        res = (True, False)
        expected = (True, False)
        coll = self.st_collection
        ex_true = coll.add_status('1','1','1', mc.db)
        with patch('user_status.UserStatusCollection.delete_status') as ds:
            ds.return_value = res[0]
            self.assertEqual(main.delete_status('1', mc.db), expected[0])
            ds.return_value = res[1]
            self.assertEqual(main.delete_status('33', mc.db), expected[1])
        with self.assertRaises(TypeError):
            main.delete_status(1, coll)

    def test_main_search_user(self):
        ''' Test of main.search_user - leverage UserStatusCollection '''
        expected = (user_status.UserStatus('statid1', 'usid1', 'test1'), user_status.UserStatus(None, None, None) )
        coll = self.st_collection
        ex_true = coll.add_status('statid1', 'usid1', 'test1', mc.db)
        with patch('user_status.UserStatusCollection.search_status') as ss:
            ss.return_value = expected[0]
            self.assertEqual(main.search_status('statid1', mc.db), expected[0])
            ss.return_value = expected[1]
            self.assertEqual(main.search_status('statid22', mc.db), expected[1])
            ss.assert_called_with('statid22', mc.db)
        with self.assertRaises(TypeError):
            main.search_status(22, mc.db)
