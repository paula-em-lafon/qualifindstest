from app import app as app
import app as glob
from importlib import reload
import unittest
import requests
import json

class Create(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_creation(self):
        payload = {"key": "whateverKey","value": 300}
        response = self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.assertEqual({'key': 'whateverKey', 'value': 300, 'version': 1}, response.json)
    
    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class CreateOtherKey(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_second_creation(self):
        payload = {"key": "whateverKey","value": 300}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        response = self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.assertEqual({'key': 'whateverKey1', 'value': 300, 'version': 2}, response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class RetrievePastKey(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_retrieve_past_key(self):
        payload = {"key": "whateverKey","value": 300}
        payload2 = {"key": "superImportantKey","value": 250}
        payloadget = {"key": "whateverKey","version": 2}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload2)
        response = self.app.get('http://127.0.0.1:5000/api/v1/', json=payloadget)
        self.assertEqual({'value': 300}, response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class RetrievePresentKeyNoVersion(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_retrieve_present_key_no_version(self):
        payload = {"key": "whateverKey","value": 300}
        payloadget = {"key": "whateverKey"}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        response = self.app.get('http://127.0.0.1:5000/api/v1/', json=payloadget)
        self.assertEqual({'value': 300}, response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class RetrievePastKeyVersion(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_second_creation(self):
        payload = {"key": "whateverKey","value": 300}
        payload2 = {"key": "whateverKey","value": 400}
        payloadget = {"key": "whateverKey", 'version': 1}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload2)
        response = self.app.get('http://127.0.0.1:5000/api/v1/', json=payloadget)
        self.assertEqual({'value': 300}, response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class RetrievePastKeyWithError(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_second_creation(self):
        payload = {"key": "whateverKey","value": 300}
        payload2 = {"key": "superImportantKey","value": 400}
        payloadget = {"key": "superImportantKey", 'version': 1}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload2)
        response = self.app.get('http://127.0.0.1:5000/api/v1/', json=payloadget)
        self.assertEqual({'error': '404 Not Found: the key, version pair is not available'}\
            , response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class RetrievePastKeyWithError(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_second_creation(self):
        payload = {"key": "whateverKey","value": 300}
        payload2 = {"key": "superImportantKey","value": 400}
        payloadget = {"key": "superImportantKey", 'version': 1}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload2)
        response = self.app.get('http://127.0.0.1:5000/api/v1/', json=payloadget)
        self.assertEqual({'error': '404 Not Found: the key, version pair is not available'}\
            , response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0

class RetrieveUnexistentKeyWithError(unittest.TestCase): 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_second_creation(self):
        payload = {"key": "whateverKey","value": 300}
        payload2 = {"key": "superImportantKey","value": 400}
        payloadget = {"key": "nonExistentKey"}
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload)
        self.app.put('http://127.0.0.1:5000/api/v1/', json=payload2)
        response = self.app.get('http://127.0.0.1:5000/api/v1/', json=payloadget)
        self.assertEqual({'error': '404 Not Found: the key is not available'}\
            , response.json)

    def tearDown(self):
        glob.keyvalue = []
        glob.current_version = 0