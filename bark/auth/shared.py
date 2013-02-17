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

    Adds to instance:
      * auth_token: token from request. Removes it from request JSON.
      * user: authenticated user.
    """

    def verify_request(self, request):
        self.verify_json(request.json, auth_spec)

        self.auth_token = request.json["auth_token"]
        self.user = Session.get_user(self.auth_token)

        del request.json["auth_token"]

        if self.user is None:
            raise AuthenticationException("Invalid auth_token")

        super(BarkAuthenticatedApiEndpoint, self).verify_request(request)
