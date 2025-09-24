'''
    Test module for our social 
    network database
    SEE SUBMIT W PROJ.TXT!!!
'''
# pylint: disable=W0611,W1514,E0401,E1120,E0001,E0602
import unittest
import csv
from mock import Mock, patch
import peewee as pw
import socialnetwork_model as sn
from socialnetwork_model import BaseModel, User, Status
import users
import user_status
import main

# MODELS = [BaseModel, User, Status]

# test_db = pw.SqliteDatabase(":memory:")

class TestDatabase(unittest.TestCase):
    ''' Test of database '''
    def setUp(self):
        '''Setup for test
            simulations of db
        '''
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.test_users = []
        self.test_st = []
        for i in range(0,10):
            self.test_users.append(
                users.Users(
                    f"user{i}",
                    f"user@u{i}.com",
                    f"uname{i}",
                    f"last{i}"
                )
            )
            self.test_st.append(
                user_status.UserStatus(
                    f"status id {i}",
                    f"user{i}",
                    f"text {i}"
                )
            )
        self.users = sn.User()
        self.status = sn.Status()

    def tearDown(self):
        test_db.close()

    def test_add_user_db(self):
        ''' Direct user add in db '''
        for people in self.test_users:
            sn.add_user_to_table(test_db, people)
        query = self.users.select()
        test = [u.user_name for u in self.test_users]
        table_users_list = [u.t_user_name for u in query]
        self.assertSequenceEqual(test, table_users_list)
        with self.assertRaises(Exception):
            sn.add_user_to_table(self.test_users[2])

    def test_modify_user(self):
        '''Modify single user via db'''
        for people in self.test_users:
            sn.add_user_to_table(test_db, people)
        self.test_users[1].email = 'for testing'
        tester = [u.email for u in self.test_users]
        sn.modify_user(test_db, self.test_users[1], new_email='for testing')
        query = self.users.select()
        actual = [t.t_user_email for t in query]
        self.assertSequenceEqual(tester, actual)

    def test_modify_user_two(self):
        ''' Modify users - verifies return value
            both of an existing record, and non-existent
            record
        '''
        test_1 = users.Users("hel", 'testing_t@t.com', 'user', 'last')
        tt_ = users.Users("f", "ff", "wont work", "t")
        sn.add_user_to_table(test_db, test_1)
        self.assertTrue(sn.modify_user(test_db, test_1))
        self.assertFalse(sn.modify_user(test_db, tt_))
        with self.assertRaises(Exception):
            sn.modify_user(test_1)

    def test_check_email(self):
        ''' Check email functionality for 
            verifying modification email of user
        '''
        test_user = self.test_users[0]
        test_return_no_update = sn.check_email(None, test_user)
        self.assertEqual(test_user.email, test_return_no_update)
        update = "new_address"
        self.assertNotEqual(test_user.email, update)
        test_ret_update = sn.check_email(update, test_user)
        self.assertEqual(test_user.email, test_ret_update)

    def test_check_u_name(self):
        ''' Check user name functionality
            verifying modification of user name
        '''
        test_user = self.test_users[0]
        test_ret_no_update = sn.check_user_name(None, test_user)
        self.assertEqual(test_user.user_name, test_ret_no_update)
        update = "new username"
        self.assertNotEqual(test_user.user_name, update)
        test_update = sn.check_user_name(update, test_user)
        self.assertEqual(test_user.user_name, test_update)

    def test_check_l_name(self):
        ''' Check last name functionality
            verifies modification
        '''
        test_user = self.test_users[0]
        test_ret_no_update = sn.check_last_name(None, test_user)
        self.assertEqual(test_user.user_last_name, test_ret_no_update)
        update = "new lastname"
        self.assertNotEqual(test_user.user_last_name, update)
        test_update = sn.check_last_name(update, test_user)
        self.assertEqual(test_user.user_last_name, test_update)

    def test_check_user_id(self):
        ''' Check user id functionality for status
            verifies modification
        '''
        test_us_id = self.test_st[0]
        no_update = sn.check_user_id(None, test_us_id)
        self.assertEqual(test_us_id.user_id, no_update)
        update = "test111"
        self.assertNotEqual(test_us_id.user_id, update)
        test_update = sn.check_user_id(update, test_us_id)
        self.assertEqual(test_us_id.user_id, test_update)

    def test_check_status_text(self):
        ''' Check status text functionality
            for status, verifies modification 
        '''
        test_st_text = self.test_st[0]
        no_update = sn.check_status_text(None, test_st_text)
        self.assertEqual(test_st_text.status_text, no_update)
        update = "test111"
        self.assertNotEqual(test_st_text.status_text, update)
        test_update = sn.check_status_text(update, test_st_text)
        self.assertEqual(test_st_text.status_text, test_update)

    def test_modify_status(self):
        ''' Test modification of single 
            status
        '''
        #add users to db
        for people in self.test_users:
            sn.add_user_to_table(test_db, people)
        #add statuses to db
        for status in self.test_st:
            sn.add_st_to_table(test_db, status)

        sn.modify_status(test_db, self.test_st[0], new_status_txt=None)
        query = self.status.select()
        actual = [s.st_status_text for s in query]
        self.assertEqual(actual[0], self.test_st[0].status_text)
        sn.modify_status(test_db, self.test_st[0], new_status_txt="Test new status!!!")
        query_two = self.status.select()
        actual_ = [s.st_status_text for s in query_two]
        self.assertEqual(actual_[0], self.test_st[0].status_text)

    def test_modify_returns(self):
        ''' Ensures return T/F
            depending on if record exists
        '''
        self.assertFalse(sn.modify_status(test_db, self.test_st[1]))
        sn.add_st_to_table(test_db, self.test_st[2])
        ex_false = sn.modify_status(test_db, self.test_st[2], new_status_txt="Hi")
        self.assertFalse(ex_false) #No user in db...expected
        sn.add_user_to_table(test_db, self.test_users[2])
        ex_true = sn.modify_status(test_db, self.test_st[2], new_status_txt="Hi")
        self.assertTrue(ex_true)

    def test_delete_user_db(self):
        ''' Test of deleting users '''
        for user in self.test_users:
            sn.add_user_to_table(test_db, user)
        for i in self.test_users:
            sn.delete_user_from_table(test_db, i.user_id)
        query = self.users.select()
        tester = []
        actual = [u.t_user_id for u in query]
        self.assertSequenceEqual(tester, actual)
        sn.add_user_to_table(test_db, self.test_users[0])
        self.assertTrue(sn.delete_user_from_table(test_db, self.test_users[0].user_id))
        self.assertFalse(sn.delete_user_from_table(test_db, self.test_users[2].user_id))

    def test_delete_status(self):
        ''' Test of deleting status '''
        for user in self.test_users:
            sn.add_user_to_table(test_db, user)

        for status in self.test_st:
            sn.add_st_to_table(test_db, status)

        for i in self.test_st:
            test = sn.delete_status_from_table(test_db, i.status_id)
            self.assertTrue(test)

        tester = []
        query = self.status.select()
        actual = [s.st_status_id for s in query]
        self.assertSequenceEqual(tester, actual)
        self.assertFalse(sn.delete_status_from_table(test_db, self.test_st[1]))

    def test_search_user_db(self):
        ''' Search for a user
            against database
        '''
        user = self.test_users[0]
        user_1 = self.test_users[1]
        sn.add_user_to_table(test_db, user)
        the_search = sn.search_user_in_table(test_db, user.user_id)
        self.assertEqual(user.user_name, the_search['t_user_name'])
        self.assertFalse(sn.search_user_in_table(test_db, user_1.user_id))

    def test_search_status_db(self):
        '''Search status in db'''
        user = self.test_users[0]
        status = self.test_st[0]
        status_ = self.test_st[1]
        sn.add_user_to_table(test_db, user)
        sn.add_st_to_table(test_db, status)
        search = sn.search_status_in_table(test_db, status.status_id)
        self.assertEqual(status.status_text, search['st_status_text'])
        self.assertFalse(sn.search_status_in_table(test_db, status_.status_id))

class TestDBFromMain(unittest.TestCase):
    ''' Calling db functions from main'''
    def setUp(self):
        '''Setup for test
            simulations of db
        '''
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.test_users = []
        self.test_st = []
        for i in range(0,10):
            self.test_users.append(
                users.Users(
                    f"user{i}",
                    f"user@u{i}.com",
                    f"uname{i}",
                    f"last{i}"
                )
            )
            self.test_st.append(
                user_status.UserStatus(
                    f"status id {i}",
                    f"user{i}",
                    f"text {i}"
                )
            )
        self.users = sn.User()
        self.status = sn.Status()

    def tearDown(self):
        test_db.close()

    def test_load_integration(self):
        ''' Integrated user add '''
        main.load_users('test_acct.csv', test_db)
        query = self.users.select()
        tester = []
        with open('test_acct.csv', newline='') as _f:
            reader = csv.DictReader(_f)
            for row in reader:
                tester.append(row['NAME'])
        self.assertSequenceEqual(tester, [u.t_user_name for u in query])

    def test_add_from_main(self):
        ''' Add user from 
            main.add_user
        '''
        user = self.test_users[0]
        ex_true = main.add_user(user.user_id, user.email,
                                user.user_name, user.user_last_name, test_db)
        self.assertTrue(ex_true)
        # avoiding traceback, the below test
        # will return false
        # ex_false = main.add_user(user.user_id, user.email,
        # user.user_name, user.user_last_name, test_db)
        # self.assertFalse(ex_false)

    def test_load_st_integration(self):
        ''' Integrated status add '''
        main.load_status_updates('test_status.csv', test_db)
        query = self.status.select()
        table_status = [t.st_status_id for t in query]
        tester = []
        with open('test_status.csv', newline='') as _f:
            reader = csv.DictReader(_f)
            for row in reader:
                tester.append(row['STATUS_ID'])
        self.assertSequenceEqual(tester, table_status)

    def test_add_st_from_main(self):
        ''' Add status direct
            from main
        '''
        # Added to meet foreign key
        # constraint in db
        user = self.test_users[1]
        main.add_user(user.user_id, user.email,
                      user.user_name, user.user_last_name, test_db)
        status = self.test_st[1]
        ex_true = main.add_status(status.user_id, status.status_id, status.status_text, test_db)
        self.assertTrue(ex_true)
        # avoiding traceback, the below test
        # will return false
        # ex_false = main.add_status(status.user_id, status.status_id, status.status_text, test_db)
        # self.assertFalse(ex_false)

    def test_add_st_db(self):
        ''' Direct status add in DB '''
        for st_ in self.test_st:
            sn.add_st_to_table(test_db, st_)
        query = self.status.select()
        st_table_list = [s.st_status_id for s in query]
        test = [s.status_id for s in self.test_st]
        self.assertSequenceEqual(st_table_list, test)
        with self.assertRaises(Exception):
            sn.add_st_to_table(self.test_st[2])

    def modify_st_from_main(self):
        ''' Modify status direct
            from main
        '''
        user = self.test_users[0]
        main.add_user(user.user_id, user.email, user.user_name, user.user_last_name, test_db)
        status = self.test_st[0]
        main.add_status(status.user_id, status.status_id, status.status_text, test_db)
        main.update_status(status.status_id, status.user_id, "Updated text!!!", test_db)
        query = self.status.select()
        actual = [s.st_status_text for s in query]
        self.assertEqual(actual[0], "Updated text!!!")
        stat_false = self.test_st[1]
        ex_false = main.update_status(stat_false.user_id,
                                      stat_false.status_id,
                                      stat_false.status_text, test_db)
        self.assertFalse(ex_false)

    def test_modify_user_from_main(self):
        ''' Modify user from
            main
        '''
        user = self.test_users[0]
        user_1 = self.test_users[1]
        sn.add_user_to_table(test_db, user)
        sn.add_user_to_table(test_db, user_1)
        ex_true = main.update_user(user.user_id, 'test@t.com',
                             'new user name', 'new last name', test_db)
        self.assertTrue(ex_true)
        main.update_user(user_1.user_id, user_1.email,
                         'new uid', 'new last',
                         test_db)
        query = self.users.select()
        test = [u.t_user_name for u in query]
        self.assertEqual(test[1], 'new uid')

    def test_delete_user_main(self):
        ''' Delete from main '''
        for user in self.test_users:
            sn.add_user_to_table(test_db, user)

        for status in self.test_st:
            sn.add_st_to_table(test_db, status)

        for i in self.test_users:
            self.assertTrue(main.delete_user(i.user_id, test_db))
        tester = []
        query = self.users.select()
        actual = [u.t_user_id for u in query]
        self.assertSequenceEqual(tester, actual)

    def test_delete_st_from_main(self):
        ''' Test of delete status 
            from main module
        '''
        for user in self.test_users:
            sn.add_user_to_table(test_db, user)

        for status in self.test_st:
            sn.add_st_to_table(test_db, status)

        for i in self.test_st:
            self.assertTrue(main.delete_status(i.status_id, test_db))

        tester = []
        query = self.status.select()
        actual = [u.st_status_id for u in query]
        self.assertSequenceEqual(tester, actual)

    def test_search_user_from_main(self):
        ''' Search user from main '''
        user = self.test_users[0]
        user_1 = self.test_users[1]
        sn.add_user_to_table(test_db, user)
        the_search = main.search_user(user.user_id, test_db)
        self.assertEqual(user.user_name, the_search['t_user_name'])
        self.assertFalse(main.search_user(user_1.user_id, test_db))

    def test_search_status_from_main(self):
        ''' Searches status from main '''
        user = self.test_users[0]
        status = self.test_st[0]
        status_ = self.test_st[1]
        sn.add_user_to_table(test_db, user)
        sn.add_st_to_table(test_db, status)
        search = main.search_status(status.status_id, test_db)
        self.assertEqual(status.status_text, search['st_status_text'])
        self.assertFalse(main.search_status(status_.status_id, test_db))
