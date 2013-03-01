from flask import jsonify
from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from .models import Group
from bark.lib import api

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
                return api.json_error(
                    "REQUEST_DENIED",
                    "A group with that name already exists"
                    )

            return api.json_ok({
                "group": group.to_json()
                })

        return api.json_error(
                    "UNAUTHORISED",
                    "You are not admin"
            )

    def get(self):
        groups_json = [g.to_json() for g in self.user.owned_groups]
        return api.json_ok({
            "groups": groups_json
        })
        

class SingleGroupView(BarkAuthenticatedApiEndpoint):
    def get(self, group_id=None):
        group = Group.query.get(group_id)
        if group and self.user in group.owners:
            return api.json_ok({
                "group": group.to_json(),
                })
        return api.json_error(
            "RESOURCE_ERROR",
            "Group does not exist"
        )
