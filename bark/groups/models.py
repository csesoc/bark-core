import datetime

from bark import db
from flask import jsonify
from bark.users.models import User
from sqlalchemy.ext.associationproxy import association_proxy

group_owners_associations = db.Table('group_owners_associations',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Membership(db.Model):
    __tablename__ = 'group_members_associations'

    expiry = db.Column(db.DateTime, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)

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
    memberships = db.relationship("Membership", backref="group")
    events = db.relationship("Event", backref="group")
    
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        
    def add_member(self, person, membership_length=365):
        expiry = datetime.datetime.today() + datetime.timedelta(days=membership_length)
        m = Membership(self, person, expiry)
        self.memberships.append(m)

    def add_owner(self, user):
        self.owners.append(user)
