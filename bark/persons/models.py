from bark import db

max_uid_length = 16
max_student_number_length = 24

class Person(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    card_uid = db.Column(db.String(max_uid_length))
    student_number = db.Column(db.String(max_student_number_length))
    memberships = db.relationship("Membership", backref='person')

    # We need to discuss the relationship between persons
    # and Users. Github issue opened.

    # We should also discuss collecting student data such
    # as names and arc membership status.

    def __init__(self, card_uid, student_number=''):
        self.card_uid = card_uid
        self.student_number = student_number
