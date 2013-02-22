from bark import db
from flask import jsonify
from bark.users.models import User

group_members_associations = db.Table('group_members_associations',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('students.id'))
)

group_owners_associations = db.Table('group_owners_associations',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    members = db.relationship("Student", secondary=group_members_associations)
    owners = db.relationship("User", secondary=group_owners_associations)
    
    def __init__(self, name, owner, description=''):
        self.name = name
        self.description = description
        self.owners.append(owner)
        
    def add_member(self, student):
        self.members.append(student)

    def add_owner(self, user):
        self.owners.append(user)
