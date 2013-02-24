from datetime import datetime, timedelta
import json

from db_session import *
from bark.lib.tests import BarkTestCase

class OWeekScan(BarkTestCase):

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

        u = User("test_user", "password")
        db.session.add(u)

        g = Group("test_group")
        db.session.add(g)
        g.add_owner(u)

        now = datetime.now()
        then = datetime.now() + timedelta(hours=24)
        e = Event(g, "test_event", "Just a test...", now, then)
        db.session.add(e) 

        db.session.commit()

    def test_swipe_session(self):
        data = self.post_json('/login', username='test_user', password='password')
        self.token = data['auth_token']

        event = self.auth_get_json('/events')['events'][0]
        device = self.auth_post_json('/devices', event_id=event['id'])

        swipe_1 = self.auth_post_json('/swipes', device_id=device['id'], event_id=event['id'], card_uid='123456789', timestamp = datetime.now().isoformat())
        self.assertEquals(swipe_1['card_uid'], '123456789')
        self.assertEquals(swipe_1['device_id'], device['id'])

        swipe_2 = self.auth_post_json('/swipes', device_id=device['id'], event_id=event['id'], card_uid='987654321', timestamp = datetime.now().isoformat())
        self.assertEquals(swipe_2['card_uid'], '987654321')
        self.assertEquals(swipe_2['device_id'], device['id'])
