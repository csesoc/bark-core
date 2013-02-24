from sqlalchemy.ext.associationproxy import association_proxy

from bark import db

max_uid_length = 16
max_student_number_length = 24

class Card(db.Model):
    __tablename__ = "cards"

    card_uid = db.Column(db.String(max_uid_length), primary_key=True)
    person_id = db.Column(db.ForeignKey('persons.id'))
    person = db.relationship("Person")

    def __init__(self, card_uid):
        self.card_uid = card_uid

    def set_person(self, person):
        self.person_id = person.id

class Person(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(max_student_number_length))
    memberships = db.relationship("Membership")
    groups = association_proxy("memberships", "group")
    cards = db.relationship("Card")
