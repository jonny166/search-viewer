#!/usr/bin/python2.7
"""Unit tests for search_api.py
.. moduleauthoer:: Kathy Church <kathy.church@gmail.com>
"""
import unittest
import logging
import search_api
import inspect
from flask import json

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

logger = search_api.logger
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(search_api.__name__ + ".log", "w"))
logger.propagate = False


class RestAPITests(unittest.TestCase):
    '''Testing the twitter functions in the rest api'''

    def setUp(self):
        '''Called for each test'''
        search_api.CONSUMER_KEY = "QMrPSdmGUrd2PX5nqh8izxPOS"
        search_api.CONSUMER_SECRET = "a4WqlRCvOb834a4hXkUJxY19oiYgMFTNJxyzNcnG1UM75pDZvY"

    def test_success(self):
        """Successful Wikipedia search"""
        logger.debug("###Starting Test: " + inspect.getframeinfo(inspect.currentframe())[2])
        with search_api.app.test_client() as client:
            response = client.get('/search_viewer/api/v1.0/search', 
                                  query_string= {'search_term': 'Flask'},
                                  follow_redirects=True)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('message', ""), 'Twitter search successful')
        self.assertNotEqual(len(data.get('data', ())), 0)
        for tweet in data.get('data', ()):
            author = tweet.get('author', '')
            content = tweet.get('content', '')
            self.assertNotEqual(len(author), 0)
            self.assertNotEqual(len(content), 0)


    def test_authentication_fail(self):
        """Bad Consumer Key"""
        search_api.CONSUMER_SECRET = "INVALID"
        logger.debug("/n/n###Starting Test: " + inspect.getframeinfo(inspect.currentframe())[2])
        with search_api.app.test_client() as client:
            response = client.get('/search_viewer/api/v1.0/search', 
                                  query_string= {'search_term': 'Flask'},
                                  follow_redirects=True)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get('message', ""), 'Twitter API Error')


    def test_no_tweets_found(self):
        """Search term produces no results"""
        logger.debug("/n/n###Starting Test: " + inspect.getframeinfo(inspect.currentframe())[2])
        with search_api.app.test_client() as client:
            bogus = "klfj34kl6j3l;ktjfekl;sjgt3kl5j6l34j56"
            response = client.get('/search_viewer/api/v1.0/search', 
                                  query_string= {'search_term': bogus},
                                  follow_redirects=True)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('message', ""), 'No matching tweets found')
        self.assertEqual(len(data.get('data', ())), 0)        


    def test_no_search_term(self):
        """Search term not given"""
        logger.debug("/n/n###Starting Test: " + inspect.getframeinfo(inspect.currentframe())[2])
        with search_api.app.test_client() as client:
            response = client.get('/search_viewer/api/v1.0/search', 
                                  follow_redirects=True)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('message', ""), 'search_term must be provided')
        self.assertEqual(len(data.get('data', ())), 0)        


    @unittest.skip("TODO: Not able to produce test condition yet")
    def test_rate_limit_exceeded(self):
        '''Twitter API rate limit exceeded error'''
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(RestAPITests)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
