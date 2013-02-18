"""
Unit tests for the swipe module.
"""

import unittest

from bark.lib.tests import BarkTestCase

class BarkSwipeCreationTests(BarkTestCase):
    def setUp(self):
        BarkTestCase.setUp(self)

        self.token = self.post_json('/login', username='test', password='aaa')['auth_token']

    def test_auth_required(self):
        data = self.post_json(
            '/swipe/',
            device='device',
            event_id=1,
            timestamp='2013-02-17T12:00:00+11:00',
            uid='uid')

        self.assertEquals(data['status'], 'BAD_REQUEST')
        self.assertTrue('auth_token' in data['error_detail'])

    def test_simple(self):
        data = self.auth_post(
            '/swipe/',
            device='device',
            event_id=1,
            timestamp='2013-02-17T12:00:00+11:00',
            uid='uid')

        self.assertEquals(data['status'], 'OK')

    def test_bad_timestamp(self):
        data = self.auth_post(
            '/swipe/',
            device='device',
            event_id=1,
            timestamp='2013-02-17T123:00:00',
            uid='uid')

        self.assertEquals(data['status'], 'BAD_REQUEST')
        self.assertTrue('timestamp' in data['error_detail'])

if __name__ == '__main__':
    unittest.main()
