from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.lib import time
from bark.persons.models import Card, Person
from bark.events.models import Event
from bark.devices.models import Device

from .models import Swipe

class SwipeView(BarkAuthenticatedApiEndpoint):
    required_fields_ = {
        "post": [
            ("device_id", int),
            ("event_id", int),
            ("timestamp", unicode),
            ("card_uid", unicode),
        ]
    }

    def post(self, json):
        event = Event.query.get(json['event_id']) 
        if event and self.user in event.group.owners:
            device = Device.query.get(json['device_id'])
            if device and device.user == self.user and device.event_id == event.id:
                # Data is legitimate
                card_uid = json['card_uid']
                card = Card.query.get(card_uid)

                if not card:
                    card = Card(card_uid)
                    db.session.add(card)
                    person = Person()
                    db.session.add(card)
                    card.set_person(person)

                swipe = Swipe(device, card, json['timestamp'])
                db.session.add(swipe)
                db.session.commit()

                return swipe.to_json()

        return {
            "status": "OK",
        }

    def verify_request(self, request):
        """
        Convert incoming timestamp into Python datetime.
        """

        super(SwipeView, self).verify_request(request)

        try:
            request.json["timestamp"] = time.parse_time(request.json["timestamp"])
        except ValueError, e:
            error = "Field 'timestamp': " + str(e.args[0] if e.args else "wtf")
            raise api.VerificationException(error)
