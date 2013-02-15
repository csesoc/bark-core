from flask import jsonify, request

from bark.lib.api import BarkApiEndpoint
from .models import Session

auth_spec = {
    "post": [
        ("auth_token", str),
    ],
}

class BarkAuthenticatedApiEndpoint(BarkApiEndpoint):
    """
    Checks for authentication token in the request, verifies its validity,
    stores the current user, and proceeds as normal.

    Calls out to bad_request if authentication token is invalid.
    """

    def dispatch_request(self):
        method = request.method.lower()
        self.verify_json(request.json, auth_spec[method])

        auth_token = request.json["auth_token"]
        self.user = Session.get_user(auth_token)

        if self.user is None:
            return jsonify({
                "status": "REQUEST_DENIED",
                "error_detail": "Invalid auth_token",
            })

        # Everything looks good at this point.
        return super(BarkAuthenticatedApiEndpoint, self).dispatch_request()
