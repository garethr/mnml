#!/usr/bin/env python

import sys
import os
import unittest

from common import CommonTest

# insert application path
app_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../'
)
sys.path.insert(0, app_path)

from mnml import HttpResponse, HttpRequest, HttpError

class UnitTest(CommonTest):
    def setUp(self):
        pass

    def test_invalid_method_in_request_creation(self):  
        
        def should_raise_exception():
            fake_environ = {
                'REQUEST_METHOD': 'BOB',
                'QUERY_STRING': '',
                'PATH_INFO': '/',
                'wsgi.input': '{}',
            }
            return HttpRequest(fake_environ)

        self.assert_raises(HttpError, should_raise_exception)

    def test_get_request(self):
        fake_environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'test=test',
            'PATH_INFO': '/',
            'wsgi.input': '{}',
        }
        request = HttpRequest(fake_environ)
        self.assertEqual(request.GET, {'test': ['test'],})
        
    def test_response_default_content_type(self):
        response = HttpResponse()
        self.assertEqual(response.headers[1][1], 'text/html')
        
    def test_response_set_invalid_code(self):
        response = HttpResponse()
        response.set_status(900)
        self.assertEqual(response.get_status(), '500 Internal Server Error')

    def test_response_headers(self):
        response = HttpResponse()
        self.assertEqual(response.get_headers(), [('content-length', '0'), ('content-type', 'text/html'), ('Location', '/')])

    def test_get_content(self):
        response = HttpResponse()
        self.assertEqual(response.get_content(), [b'', '\n'])

    def test_response_properties(self):
        response = HttpResponse()
        self.assertEqual(response.headers, [('content-length', '0'), ('content-type', 'text/html'), ('Location', '/')])
        self.assertEqual(response.content, [b'', '\n'])
        self.assertEqual(response.status, '200 OK')

if __name__ == "__main__":
    unittest.main()