"""
Unit tests for the auth module.
"""
import json, unittest

import bark
import bark.lib

from bark.lib.tests import BarkTestCase
from db_session import *

class BarkAuthApiTests(BarkTestCase):

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

        u = User('test', 'aaa')
        db.session.add(u)
        db.session.commit()

    def test_login_wrong_username(self):
        data = self.post_json('/login', username='wrong', password='aaa')
        self.assertEquals(data['status'], 'REQUEST_DENIED')
        self.assertEquals(data['error_detail'], 'Invalid credentials')

    def test_login_wrong_password(self):
        data = self.post_json('/login', username='test', password='wrong')
        self.assertEquals(data['status'], 'REQUEST_DENIED')
        self.assertEquals(data['error_detail'], 'Invalid credentials')

    def test_login_succeeds(self):
        data = self.post_json('/login', username='test', password='aaa')
        self.assertEquals(data['status'], 'OK')
        self.assertTrue('auth_token' in data)

    def test_login_with_logout_succeed(self):
        data = self.post_json('/login', username='test', password='aaa')
        self.assertEquals(data['status'], 'OK')
        self.assertTrue('auth_token' in data)

        token = data['auth_token']
        self.assertTrue(len(token) == 64)

        data = self.post_json('/logout', auth_token=token)
        self.assertEquals(data, {'status': 'OK'})

    def test_missing_fields(self):
        data = self.post_json('/login', username='test')
        self.assertEquals(data['status'], 'BAD_REQUEST')
        self.assertTrue('password' in data['error_detail'])

        data = self.post_json('/login', password='aaa')
        self.assertEquals(data['status'], 'BAD_REQUEST')
        self.assertTrue('username' in data['error_detail'])

    def test_wrong_type_of_fields(self):
        data = self.post_json('/login', username=123, password='aaa')
        self.assertEquals(data['status'], 'BAD_REQUEST')
        self.assertTrue('username' in data['error_detail'])

        data = self.post_json('/login', username='test', password=123)
        self.assertEquals(data['status'], 'BAD_REQUEST')
        self.assertTrue('password' in data['error_detail'])

class BarkAuthSharedTests(BarkTestCase):
    def test_authentication_required(self):
        data = self.post_json('/login', username='test', password='aaa')
        self.assertEquals(data['status'], 'OK')
        self.assertTrue('auth_token' in data)

        token = data['auth_token']

        data = self.post_json('/test-api-auth')
        self.assertEquals(data['status'], 'UNAUTHORISED')
        self.assertTrue('auth_token' in data['error_detail'])

        data = self.post_json('/test-api-auth', auth_token='')
        self.assertEquals(data['status'], 'UNAUTHORISED')
        self.assertTrue('auth_token' in data['error_detail'])

        data = self.post_json('/test-api-auth', auth_token='a'*64)
        self.assertEquals(data['status'], 'UNAUTHORISED')
        self.assertTrue('auth_token' in data['error_detail'])

        data = self.post_json('/test-api-auth', auth_token=token)
        self.assertEquals(data['status'], 'UNAUTHORISED')

        self.token = token
        data = self.auth_post_json('/test-api-auth')
        self.assertEquals(data['status'], 'OK')

if __name__ == '__main__':
    unittest.main()
