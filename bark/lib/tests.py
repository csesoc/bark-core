"""
Base class for all Bark unit tests.
"""
import json, unittest

import bark

class BarkTestCase(unittest.TestCase):
    """
    Base class for all bark unit tests.
    """

    def setUp(self):
        self.app = bark.create_app().test_client()

    def get(self, url, **kwargs):
        return self.app.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.app.post(url, **kwargs)

    def auth_get(self, url, **kwargs):
        assert self.token is not None, 'Must authenticate and set self.token'
        if 'headers' not in kwargs:
            kwargs['headers'] = []
        kwargs['headers'].append(('auth_token', self.token))
        return self.get(url, **kwargs)

    def auth_post(self, url, **kwargs):
        assert self.token is not None, 'Must authenticate and set self.token'
        if 'headers' not in kwargs:
            kwargs['headers'] = []
        kwargs['headers'].append(('auth_token', self.token))
        return self.post(url, **kwargs)

    def post_json(self, url, **kwargs):
        # JSON passed as kwargs, slightly messy
        response = self.post(url, data=json.dumps(kwargs), content_type='application/json')
        return json.loads(response.data)

    def auth_post_json(self, url, **kwargs):
        # Conflict between two different kwargs needs. Dayum.
        response = self.auth_post(url, data=json.dumps(kwargs), content_type='application/json')
        return json.loads(response.data)
