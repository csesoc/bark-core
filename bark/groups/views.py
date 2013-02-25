from flask import jsonify
from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from .models import Group

class GroupView(BarkAuthenticatedApiEndpoint):
    required_fields = {
       "post": [
            ("name", str),
            ("description", str),
       ]
    }
 
    def post(self, json):
        if self.user.is_admin:
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
                "group": group.to_json(),
                }

        return {
            "status": "REFUSED"
        }

    def get(self):
        groups_json = [g.to_json() for g in self.user.owned_groups]
        return {
            "status": "OK",
            "groups": groups_json,
        }
        

class SingleGroupView(BarkAuthenticatedApiEndpoint):
    def get(self, group_id=None):
        group = Group.query.get(group_id)
        if group and self.user in group.owners:
            return group.to_json()
        else:
            return {
                "status": "RESOURCE_ERROR",
                "error": "Group does not exist",
            }
