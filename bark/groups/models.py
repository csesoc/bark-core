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

    id = db.Column('id', db.Integer, primary_key=True),
    student_id = db.Column(db.Integer, db.ForeignKey('students.id')),
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id')),
    expiry = db.Column(db.DateTime, nullable=False),

    group = db.relationship(Group, backref="memberships")
    student = db.relationship(Student, backref="memberships")


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    members = association_proxy("memberships", "students")
    owners = db.relationship("User", secondary=group_owners_associations)
    
    def __init__(self, name, owner, description=''):
        self.name = name
        self.description = description
        self.owners.append(owner)
        
    def add_member(self, student):
        self.members.append(student)

    def add_owner(self, user):
        self.owners.append(user)
