from datetime import datetime, timedelta
import json

from db_session import *
from bark.lib.tests import BarkTestCase

class EventsTest(BarkTestCase):

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

        u = User("test_user", "password")
        db.session.add(u)

        g = Group("test_group")
        db.session.add(g)
        g.add_owner(u)

        g2 = Group("other_group")
        db.session.add(g2)

        now = datetime.now()
        then = datetime.now() + timedelta(hours=24)

        e = Event(g, "test_event", "Just a test...", now, then)
        db.session.add(e) 

        e2 = Event(g2, "other_event", "Just a test...", now, then)
        db.session.add(e2) 

        db.session.commit()

    def test_get_all(self):
        data = self.post_json('/login', username='test_user', password='password')
        self.token = data['auth_token']

        events = self.auth_get_json('/events')
        self.assertEquals(len(events), 1)
        self.assertEquals(events['events'][0]['name'], 'test_event')

    def test_get_specific(self):
        data = self.post_json('/login', username='test_user', password='password')
        self.token = data['auth_token']
       
        event_id = Event.query.filter_by(name='test_event').first().id
        event = self.auth_get_json('/events/' + str(event_id))
        self.assertEquals(event['id'], event_id)
        self.assertEquals(event['name'], "test_event")

