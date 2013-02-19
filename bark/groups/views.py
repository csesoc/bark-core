from flask import jsonify
from bark import db
from bark.lib.api import BarkApiEndpoint
from bark.groups.models import Event
from bark.users.models import User
from bark.groups.models import Group

class CreateGroupVeiw(BarkApiEndpoint)
    required_fields = {
       "post": [
            ("group_id", int),
            ("name", str),
            ("description", str),
       ]
    }
    def post(self, json):
        user = Session.get_user(auth_token)
        name = jsonify["name"]
        g = jsonify(Group.query.filter_by(name=name)
        if not g:
            #Assume that the person creating the group is an owner
            group = Group(name, user, user, description)
            db.session.add(group)
            db.session.commit()

            return {
                "status": "OK",
                "group_id": group.group_id,
            }
        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "A group with that name already exists"
            }

class GroupView(BarkApiEndpoint):
    required_fields = {
        "get": [
            ("auth_token", str)
        ],
        "delete": [
            ("auth_token", str),
        ]    
    }
    def get(self, json):
        group = jsonify(Group.query.filter_by(group_id=group_id))
        if group:
            return jsonify(group)
        else:
            return {
                "status": "RESOURCE_ERROR"
                "error": "Group does not exist"
            }
    def delete(self, json):
        group = jsonify(Group.query.filter_by(group_id=group_id))
        if group:
            if Session.get_user(auth_token) in group.owners:
                db.session.delete(g)
                db.session.commit()

                return {
                    "status": "OK",
                }
            else:
                return {
                    "status": "REQUEST_DENIED",
                    "error": "User not owner of the group",
                }
        else:
            return{
                "status": "RESOURCE_ERROR",
                "error": "The requested group could not be found"
            }                 
