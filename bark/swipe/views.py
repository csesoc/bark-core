from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.lib import api, time

from .models import Swipe

class SwipeView(BarkAuthenticatedApiEndpoint):
    required_fields_ = {
        "post": [
            ("device", unicode),
            ("event_id", int),
            ("timestamp", unicode),
            ("uid", unicode),
        ]
    }

    def post(self, json):
        # TODO: Check event belongs to this user.
        swipe = Swipe(user=self.user, **json) # TODO: this will break if json contains other fields. What do?
        db.session.add(swipe)
        db.session.commit()

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
