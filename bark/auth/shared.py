from flask import jsonify

from bark.lib.api import BarkApiEndpoint, BarkApiException
from .models import Session

auth_spec = [
    ("auth_token", unicode),
]

class AuthenticationException(BarkApiException):
    def status(self): return "UNAUTHORISED"

class BarkAuthenticatedApiEndpoint(BarkApiEndpoint):
    """
    Checks for authentication token in the request, verifies its validity,
    stores the current user, and proceeds as normal.
    """

    def verify_request(self, request):
        self.verify_json(request.json, auth_spec)

        auth_token = request.json["auth_token"]
        self.user = Session.get_user(auth_token)

        if self.user is None:
            raise AuthenticationException("Invalid auth_token")

        super(BarkAuthenticatedApiEndpoint, self).verify_request(request)
