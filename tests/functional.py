#!/usr/bin/env python

import sys
import os
import unittest
from webtest import TestApp, AppError

# insert application path
app_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../'
)
sys.path.insert(0, app_path)

from example_app import application

class FunctionalTest(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(application) 

    def test_index_returns_200(self):  
        response = self.app.get('/', expect_errors=True)        
        self.assertEquals("200 OK", response.status)
            
    def test_index_return_correct_mime_type(self):
        response = self.app.get('/', expect_errors=True)
        self.assertEquals(response.content_type, "text/html")
        
    def test_multiple_args_in_url(self):
        response = self.app.get('/foo/1/2', expect_errors=True)        
        response.mustcontain("Hello World of 1 and 2")

    def test_put(self):
        response = self.app.put('/', expect_errors=True)        
        self.assertEquals("200 OK", response.status)
        response.mustcontain("Hello World of Put")
        
    def test_404_handler(self):  
        response = self.app.get('/does-not-exist', expect_errors=True)        
        self.assertEquals("404 Not Found", response.status)

    def test_404_handler(self):  
        response = self.app.get('/does-not-exist', expect_errors=True)        
        self.assertEquals("404 Not Found", response.status)

    def test_HTTPResponseRedirect_handler(self):
        response = self.app.get('/bar', expect_errors=True)        
        self.assertEquals("/", response.headers['Location'])
        self.assertEquals("301 Moved Permanently", response.status)

    def test_temporaty_HTTPResponseRedirect_handler(self):
        response = self.app.delete('/bar', expect_errors=True)        
        self.assertEquals("/", response.headers['Location'])
        self.assertEquals("302 Found", response.status)

    def test_unregistered_post_request(self):
        response = self.app.post('/', expect_errors=True)        
        self.assertEquals("405 Method Not Allowed", response.status)

    def test_unregistered_delete_request(self):
        response = self.app.delete('/', expect_errors=True)        
        self.assertEquals("405 Method Not Allowed", response.status)

    def test_unregistered_put_request(self):
        response = self.app.put('/bar', expect_errors=True)        
        self.assertEquals("405 Method Not Allowed", response.status)

    def test_query_string(self):  
        response = self.app.get('/?test=test', expect_errors=True)        
        self.assertEqual("test", response.request.GET['test'])
        self.assertEquals("200 OK", response.status)

    def test_addition_of_method_to_request(self):  
        response = self.app.get('/', expect_errors=True)        
        self.assertEqual("GET", response.request.method)
                                       
if __name__ == "__main__":
    unittest.main()