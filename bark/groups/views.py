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
        group = Group(json['name'], json['description'])
        group.add_owner(self.user)  # Owners are separate from members, for now.
        group.add_member(self.user)
        try:
            db.session.add(group)
            db.session.commit()
        except db.IntegrityError:
            return {
                "status": "REQUEST_DENIED",
                "error": "A group with that name already exists",
                }

        return {
            "status": "ok", 
            "group id": "group.id",
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
