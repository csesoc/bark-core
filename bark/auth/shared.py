from flask import jsonify

from bark.lib.api import BarkApiEndpoint, BarkApiException
from .models import Session

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

        self.auth_token = request.headers.get('auth_token')
        if self.auth_token is None:
            raise AuthenticationException("No auth_token in header")

        self.user = Session.get_user(self.auth_token)
        if self.user is None:
            raise AuthenticationException("Invalid auth_token")

        super(BarkAuthenticatedApiEndpoint, self).verify_request(request)
