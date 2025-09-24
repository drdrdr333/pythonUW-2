'''
    Tests for Mongo DB
'''

# pylint:  disable=W0611
import unittest
from mock import Mock, MagicMock
from pymongo import MongoClient, database
import pymongo
import mongo_connect as mc
import users
import user_status


class TestMongo(unittest.TestCase):
    '''
        Tests for Mongo DB
        connections, methods
    '''
    def test_connection(self):
        ''' Direct connection works '''
        test = mc.MongoConnection()
        self.assertEqual(type(test), mc.MongoConnection)
        with test:
            self.assertEqual(test.connection.HOST, 'localhost')
            self.assertEqual(test.connection.PORT, 27017)

    def setUp(self):
        ''' Setup of objects to pass to DB '''
        self.user = users.Users(1, 'test@test_test_test.com', 'test', 'test last name')
        self.status = user_status.UserStatus(1, 1, "hello world")

    # def test_create_collection(self):
    #     ''' Create appropriately named collection
    #         **this test can be run only once**
    #     '''
    #     collection_name = "UserStatus"
    #     ex_true = mc.create_collection(collection_name)
    #     self.assertTrue(ex_true)

    def test_insert_objects(self):
        ''' Insert one object into Mongo db '''
        test = users.Users(3, 'test@test.com', 'test', 'test last name')
        test_three = user_status.UserStatus(2, 22, "hello!!!! world")
        ex_true = mc.insert_to_db(test)
        ex_true_two = mc.insert_to_db(user_status.UserStatus(1, 3, "hello world"))
        ex_false = mc.insert_to_db(test_three)
        self.assertTrue(ex_true)
        self.assertTrue(ex_true_two)
        self.assertFalse(ex_false)

    def test_modify_objects(self):
        ''' Modify an existent object in Mongo DB '''
        mc.insert_to_db(self.user)
        test = mc.modify_object_in_db(users.Users(1,
                                                  'test@test_test_test.com',
                                                  'test',
                                                  'test last name'))
        self.assertTrue(test)
        test_two = mc.modify_object_in_db(users.Users(2,
                                                      'test@test_test_test.com',
                                                      'test',
                                                      'test last name'))
        self.assertFalse(test_two)
        mc.insert_to_db(self.status)
        test_three = mc.modify_object_in_db(user_status.UserStatus(
            1,
            1,
            "new hello world!!"
        ))
        self.assertTrue(test_three)

    def test_delete_user(self):
        ''' Delete object within a collection
            of a Mongo DB
        '''
        mc.insert_to_db(self.user)
        ex_true = mc.delete_user_in_db(self.user.user_id)
        self.assertTrue(ex_true)

    def test_delete_status(self):
        ''' Test of status delete in Mongo '''
        mc.insert_to_db(self.user)
        mc.insert_to_db(users.Users(3, 'test@test.com', 'test', 'test last name'))
        mc.insert_to_db(self.status)
        ex_true = mc.delete_status_in_db(self.status.user_id)
        self.assertTrue(ex_true)
        ex_false = mc.delete_status_in_db(self.status.user_id)
        self.assertFalse(ex_false)

    def test_search_user(self):
        ''' Test of search for user in Mongo DB '''
        mc.insert_to_db(self.user)
        the_user = mc.search_user_in_db(self.user.user_id)
        self.assertEqual('test', the_user['User Name'])
        ex_false = mc.search_user_in_db(22)
        self.assertFalse(ex_false)

    def test_search_status(self):
        ''' Test of search statuses '''
        mc.insert_to_db(self.user)
        mc.insert_to_db(self.status)
        ex_true = mc.search_status_in_db(self.status.status_id)
        self.assertTrue(ex_true)
        self.assertEqual('hello world', ex_true['Status Text'])
