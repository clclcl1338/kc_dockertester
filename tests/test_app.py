import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, get_token

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_auth_no_creds(self):
        # Test auth endpoint with no credentials
        response = self.app.post('/auth')
        self.assertEqual(response.status_code, 401)

    def test_check_no_token(self):
        # Test check endpoint with no token
        response = self.app.get('/check')
        self.assertEqual(response.status_code, 401)

    def test_check_invalid_token(self):
        # Test check endpoint with invalid token
        response = self.app.get('/check', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
