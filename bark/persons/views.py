from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.groups.models import Group

from .models import *

class PersonsView(BarkAuthenticatedApiEndpoint):
    required_fields_ = {
       "post": [
           ("student_number", unicode),
           ("card_uid", unicode),
       ],
    }

    def post(self, json):
        # Is the card already in the system
        card = Card.query.filter_by(card_uid = json['card_uid']).first()

        if card and card.person and card.person.student_number == None:
            card.person.student_number = json['student_number']

        elif not card:
            card = Card(json['card_uid'])
            person = Person()
            db.session.add(card)
            db.session.add(person)
            card.set_person(person)
            person.student_number = json['student_number']

        db.session.commit()

        person = Card.query.get(json['card_uid']).person
        return person.to_json()
