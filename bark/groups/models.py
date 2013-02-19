from bark import db
from flask import jsonify
from bark.users.models import User

group_members = db.Table('group_members',
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'))
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
)

group_owners = db.Table('group_owners',
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'))
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
)

class Group(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    members = db.relationships("User", secondary=members, 
        backref=db.backref('member_groups', lazy='dynamic'))
    owners = db.relationships("User", secondary=owners, 
        backref=db.backref('owned_groups', lazy='dynamic'))
    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    def __init__(self, name, members, owners, description):
        self.name = name
       
        self.members = group_members
        self.members = self.members.append(User(members))
        self.members.execute()
        
        self.owners = group_owners
        self.owners = self.owners.append(User(owners))
        self.owners.execute()
        
        self.name = name
        self.description = description
