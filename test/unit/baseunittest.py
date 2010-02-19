#!/usr/bin/python
# -*- coding: utf-8 -*-
# from python doc

import os, unittest, time, re

from src.utils import pathfix # pyflakes:ignore

from google.appengine.api import apiproxy_stub_map, datastore_file_stub, urlfetch_stub, user_service_stub, mail_stub
from google.appengine.api.memcache import memcache_stub
from google.appengine.api.labs.taskqueue import taskqueue_stub
from google.appengine.ext.db import NotSavedError

APP_ID = u'test_app'
AUTH_DOMAIN = 'gmail.com'
LOGGED_IN_USER = 'mary@gmail.com'  # set to '' for no logged in user

class GaeBaseUnitTest(unittest.TestCase):
    def setUp(self):
        os.environ['TZ'] = 'UTC'
        time.tzset()
        os.environ['AUTH_DOMAIN'] = 'test.com'
        os.environ['USER_EMAIL'] = 'u...@test.com'
        os.environ['APPLICATION_ID'] = 'MyAppId'
        os.environ['SERVER_NAME'] = 'unittest.local'
        os.environ['SERVER_PORT'] = '80'
        os.environ['SERVER_SOFTWARE'] = 'Development/Unittest'

        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        self.api_proxy_stub_map = apiproxy_stub_map

        datastore = datastore_file_stub.DatastoreFileStub('MyAppId', None, None)
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', datastore)
        apiproxy_stub_map.apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())
        apiproxy_stub_map.apiproxy.RegisterStub('mail', mail_stub.MailServiceStub())
        apiproxy_stub_map.apiproxy.RegisterStub('memcache', memcache_stub.MemcacheServiceStub())
        apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', taskqueue_stub.TaskQueueServiceStub())
        
    def assertLength(self, length, collection):
        self.assertEquals(length, len(collection))
        
    def assertRegex(self, regex, thing):
        self.assertTrue(re.search(regex, thing), "Expected '%s', Found: '%s'" % (regex, thing))
        
    def assertNotRegex(self, regex, thing):
        self.failIf(re.search(regex, thing))
        
    def assertEmpty(self, list_thing):
        self.assertTrue(len(list_thing) == 0)
        
    def assertNull(self, thing):
        self.failIf(thing)
        
    def assertNotNull(self, thing, *msg):
        self.failIf(not thing, *msg)
        
    def assertSaved(self, thing):
        self.assertNotNull(thing.key())

    def assertNotSaved(self, thing):
        try:
            self.assertNull(thing.key())
        except NotSavedError, e:
            None
            
    def assertException(self, exception_type, exception):
        # self.assertType(exception_type, exception, exception.message)
        self.failIf(not isinstance(exception, exception_type), exception.message)
        
    def assertExceptions(self, types, exception):
        for t in types:
            self.assertException(t, exception)
            
    def assertIsInstance(self, obj, typeof):
        self.assertTrue(isinstance(obj, typeof))
