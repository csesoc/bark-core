from bark.lib.tests import BarkTestCase
from bark.persons.models import Person

from db_session import *

class PersonCreateTest(BarkTestCase):

    def setUp(self):
        BarkTestCase.setUp(self)

        db.drop_all()
        db.create_all()

        u = User('person_test', 'password')
        db.session.add(u)
        db.session.commit()

        self.token = self.post_json('/login', username='person_test', password='password')['auth_token']

    def test_create(self):
        person = self.auth_post_json('/persons', card_uid = 'awesomelol', student_number = '123456789')

        self.assertEquals(person['student_number'], '123456789') 
        self.assertEquals(person['card_uids'], ['awesomelol']) 

    def test_update(self):
        card = Card('testuid')
        person = Person()
        card.set_person(person)
        db.session.add(card)
        db.session.add(person)
        db.session.commit()

        person = self.auth_post_json('/persons', card_uid = 'testuid', student_number = '123456789')

        self.assertEquals(person['student_number'], '123456789') 
        self.assertEquals(person['card_uids'], ['testuid']) 

    def test_update(self):
        card = Card('testuid')
        person = Person()
        person.student_number = '12321'
        card.set_person(person)
        db.session.add(card)
        db.session.add(person)
        db.session.commit()

        person = self.auth_post_json('/persons', card_uid = 'testuid', student_number = '123456789')

        self.assertEquals(person['student_number'], '12321') 
        self.assertEquals(person['card_uids'], ['testuid']) 
