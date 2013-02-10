from datetime import datetime

from bark import db
from bark.lib.api import BarkApiEndpoint
from bark.events.models import Event
from bark.users.models import User
from bark.groups.models import Group
from bark.auth.models import Session

class CreateEventView(BarkApiEndpoint):
    required_fields_ = {
        "post": {str: ["auth_token", "description", "name"],
                 int: ["start_time", "end_time", "group_id"]},
    }

    def post(self, json):
        user = Session.get_user(auth_token)
        group_id = json["group_id"]
        group = Group.by_id(group_id)

        if user in group.members:
            name = json["name"]
            description = json["name"]
            start_time = json["start_time"]
            end_time = json["end_time"]

            event = Event(group_id, name, description, start_time, end_time)
            db.session.add(event)
            db.session.commit()

            return {
                "status": "OK",
                "event_id":, event.event_id,
            }
        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "User not member of group",
            }
            
