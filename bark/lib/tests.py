"""
Base class for all Bark unit tests.
"""
import unittest
import json

import bark

class BarkTestCase(unittest.TestCase):
    """
    Base class for all bark unit tests.
    """

    def setUp(self):
        self.app = bark.create_app().test_client()

    def post(self, url, **kwargs):
        return self.app.post(
            url,
            data=json.dumps(kwargs),
            content_type='application/json')

    def post_json(self, url, **kwargs):
        return json.loads(self.post(url, **kwargs).data)
