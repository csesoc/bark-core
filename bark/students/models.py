from bark import db

max_uid_length = 16

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    card_uid = db.Column(db.String(max_uid_length))

    # We need to discuss the relationship between Students
    # and Users. Github issue opened.

    # We should also discuss collecting student data such
    # as names and arc membership status.
