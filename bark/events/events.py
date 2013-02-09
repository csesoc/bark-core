from bark import db
from bark.lib.api import BarkApiEndpoint
from bark.events.models import Event
from bark.users.models import User
from bark.groups.models import Group
from bark.auth.models import Session

class CreateEventView(BarkApiEndpoint):
    required_fields_ = {
        "post": ["auth_token", "group_id", "name", 
                 "description", "start_time", "end_time"],
    }

    def post(self, json):
        user = Session.get_user(auth_token)

        group = Group.by_id(json["group_id"])

        if user in group.members:
            event = Event(
        
