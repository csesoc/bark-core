from flask import jsonify
from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.groups.models import Group

class CreateGroupView(BarkAuthenticatedApiEndpoint):
    required_fields = {
       "post": [
            ("group_id", int),
            ("name", str),
            ("description", str),
       ]
    }
    def post(self, json):
        name = jsonify["name"]
        g = jsonify(Group.query.filter_by(name=name))
        if not g:
            #Assume that the person creating the group is an owner
            group = Group(name, description)
            group.add_member(self.user)
            group.add_owner(self.user)
            db.session.add(group)
            db.session.commit()

            return {
                "status": "OK",
                "group_id": group_id,
            }
        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "A group with that name already exists",
            }

class GroupView(BarkAuthenticatedApiEndpoint):
    def get(self, json):
        group = Group.query.get(json['group_id'])
        if group:
            return jsonify(group)
        else:
            return {
                "status": "RESOURCE_ERROR",
                "error": "Group does not exist",
            }
    def delete(self, json):
        group = Group.query.get(json['group_id'])
        if group:
            if self.user in group.owners:
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
                "error": "The requested group could not be found",
            }                 
