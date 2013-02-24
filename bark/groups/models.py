import datetime

from bark import db
from flask import jsonify
from bark.users.models import User
from bark.persons.models import Person
from sqlalchemy.ext.associationproxy import association_proxy

group_owners_associations = db.Table('group_owners_associations',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Membership(db.Model):
    __tablename__ = 'group_members_associations'

    expiry = db.Column(db.DateTime, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    group = db.relationship("Group")
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    person = db.relationship("Person")

    def __init__(self, group, person, expiry):
        self.group_id = group.id
        self.person_id = person.id
        self.expiry = expiry

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    owners = db.relationship("User", secondary=group_owners_associations, backref='owned_groups')
    events = db.relationship("Event",)
    memberships = db.relationship("Membership")
    members = association_proxy("memberships", "person")
    
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        
    def add_member(self, person, membership_length=365):
        expiry = datetime.datetime.today() + datetime.timedelta(days=membership_length)
        m = Membership(self, person, expiry)
        self.memberships.append(m)

    def add_owner(self, user):
        self.owners.append(user)

    def to_json(self):
        json = {}
        json['id'] = self.id
        json['name'] = self.name
        json['description'] = self.description
        json['owners'] = [o.username for o in self.owners]
        json['events'] = [e.id for e in self.events]
        json['members'] = [p.to_json() for p in self.members]
        return json

