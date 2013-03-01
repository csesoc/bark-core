from bark import db
from bark.groups.models import Group
from sqlalchemy.ext.associationproxy import association_proxy

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship("Group")

    name = db.Column(db.Text)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    devices = db.relationship("Device", backref="event")
    swipes = association_proxy("devices", "swipes")

    def __init__(self, group, name, description, start_time, end_time):
        self.group = group
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

    def to_json(self):
        json = {}
        json['id'] = self.id
        json['group_id'] = self.group_id
        json['group'] = self.group.name
        json['name'] = self.name
        json['description'] = self.description
        json['start_time'] = self.start_time.isoformat()
        json['end_time'] = self.end_time.isoformat()
        return json

