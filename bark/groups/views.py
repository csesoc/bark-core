from flask import jsonify
from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.groups.models import Group

class CreateGroupView(BarkAuthenticatedApiEndpoint):
    required_fields = {
       "post": [
            ("name", str),
            ("description", str),
       ]
    }
 
    def post(self, json):
        group = Group(json['name'], self.user, description=json['description'])
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
    def get(self):
        group = Group.query.get(group_id)
        if group:
            return jsonify(group)
        else:
            return {
                "status": "RESOURCE_ERROR",
                "error": "Group does not exist",
            }
    def delete(self, json):
        group = Group.query.get(group_id)
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
