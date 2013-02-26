import unittest

from bark.lib import api

class ApiTest(unittest.TestCase):
    def test_json_invalid_status(self):
        response = api.json_response('INVALID_STATUS_YO')
        self.assertEquals(response['status'], 'BACKEND_ERROR')

    def test_valid_status(self):
        response = api.json_response('OK', {'test_worked': 'yes'})
        self.assertEquals(response['status'], 'OK')
        self.assertEquals(response['test_worked'], 'yes')

    def test_json_ok(self):
        response = api.json_ok({'test_worked': 'yes'})
        self.assertEquals(response['status'], 'OK')
        self.assertEquals(response['test_worked'], 'yes')

    def test_json_error(self):
        response = api.json_error('UNAUTHORISED', 'Invalid auth token')
        self.assertEquals(response['status'], 'UNAUTHORISED')
        self.assertEquals(response['error_detail'], 'Invalid auth token')
