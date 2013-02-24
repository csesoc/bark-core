from flask import jsonify

from bark import db
from .models import Event
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.groups.models import Group

class EventView(BarkAuthenticatedApiEndpoint):
    required_fields_ = {
        "post": [
            ("description", unicode),
            ("name",        unicode),
            ("start_time",  int), 
            ("end_time",    int),
            ("group_id",    int),
        ],
    }

    def get(self):
        owned_group_ids = [g.id for g in self.user.owned_groups]
        events = Event.query.filter(Event.group_id.in_(owned_group_ids))
        events_json = [e.to_json() for e in events.all()]
        return {
            "status": "OK",
            'events': events_json
        }

    def post(self, json):
        # User set by AuthenticatedApiEndpoint
        group_id = json["group_id"]
        group = Group.query.get(group_id)

        if self.user in group.owners:
            name = json["name"]
            description = json["description"]
            start_time = json["start_time"]
            end_time = json["end_time"]

            event = Event(group_id, name, description, start_time, end_time)
            db.session.add(event)
            db.session.commit()

            return {
                "status": "OK",
                "event_id": event.event_id,
            }
        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "User not member of group",
            }
            
class SingleEventView(BarkAuthenticatedApiEndpoint):

    def get(self, event_id=None):
        event = Event.query.get(event_id)
        if event is not None:
            group = Group.query.get(event.group_id)
            if group and self.user in group.owners:
                return {
                    "status": "OK",
                    "event": event.to_json(),
                }

        return {
            "status": "RESOURCE_ERROR",
            "error_detail": "The requested event could not be found",
        }
        
    def delete(self, json):
        event = Event.query.get(event_id)
        if event:
            group = Group.by_id(event.group_id)
            if user in group.owners:
                db.session.delete(event)
                db.session.commit()

                return {
                    "status": "OK",
                }

        return {
            "status": "RESOURCE_ERROR",
            "error_detail": "The requested event could not be found",
        }
