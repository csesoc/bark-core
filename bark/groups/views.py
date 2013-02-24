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

class GroupView(BarkAuthenticatedApiEndpoint):
    def get(self):
        group = Group.query.get(group_id)
        if group and self.user in group.owners:
            return group.to_json()
        else:
            return {
                "status": "RESOURCE_ERROR",
                "error": "Group does not exist",
            }
