from datetime import datetime

from flask import jsonify

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
                "event_id": event.event_id,
            }
        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "User not member of group",
            }
            
class EventView(BarkApiEndpoint):
    # event_id is global by url rules
    required_fields_ = {
        "get": {str: ["auth_token"]},
        "delete": {str: ["auth_token"]},
    }

    def get(self, json):
        e = jsonify(Event.query.filter_by(event_id=event_id))
        if e:
            group = Group.by_id(e.group_id)
            if Session.get_user(auth_token) in group.members:
                return jsonify(e) 

            return {
                "status": "REQUEST_DENIED",
                "error": "User not member of group",
            }
         
        return {
            "status": "RESOURCE_ERROR",
            "error": "The requested event could not be found",
        }
        
    def delete(self, json):
        e = jsonify(Event.query.filter_by(event_id=event_id))
        if e:
            group = Group.by_id(e.group_id)
            if Session.get_user(auth_token) in group.owners:
                db.session.delete(e)
                db.session.commit()

                return {
                    "status": "OK",
                }

            else:
                return {
                    "status": "REQUEST_DENIED",
                    "error": "User not owner of owning group",
                }
                
        return {
            "status": "RESOURCE_ERROR",
            "error": "The requested event could not be found",
        }
