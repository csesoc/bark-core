from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.events.models import Event

from .models import Device

class DeviceView(BarkAuthenticatedApiEndpoint):
    required_fields_ = {
        "post": [("event_id", int)]
    }

    def post(self, json):
        event = Event.query.get(json['event_id'])
        if event and self.user in event.group.owners:
            d = Device(self.user, event)
            db.session.add(d)
            db.session.commit()
            return d.to_json()

        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "Event not found"
            }
