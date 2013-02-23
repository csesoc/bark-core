from bark import db
from bark.groups.models import Group

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    name = db.Column(db.Text)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, group, name, description, start_time, end_time):
        self.group = group
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
