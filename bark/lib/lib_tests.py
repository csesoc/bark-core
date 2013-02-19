"""
Tests for bark.lib.*
"""

import json

from bark.lib.tests import BarkTestCase

class BarkLibApiTests(BarkTestCase):
    def test_nonjson_request(self):
        data = json.loads(self.app.post('/login', data='{}').data)
        self.assertEqual(data['status'], 'BAD_REQUEST')
        self.assertTrue('JSON' in data['error_detail'])

    def test_frontpage_not_found(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 404)

    def test_jsonp_compliance(self):
        data = self.post(
            '/login?callback=cb314',
            username='test',
            password='aaa').data
        self.assertTrue(data.startswith('cb314'))

if __name__ == '__main__':
    unittest.main()
