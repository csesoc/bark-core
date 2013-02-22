from bark import db
from bark.lib.api import BarkApiEndpoint
from bark.users import User

from .models import Session
from .shared import BarkAuthenticatedApiEndpoint

class LoginView(BarkApiEndpoint):
    required_fields_ = {
        "post": [
            ("username", unicode),
            ("password", unicode),
        ],
    }

    def post(self, json):
        user = User.authenticate(json["username"], json["password"])

        if user is not None:
            s = Session(user)
            db.session.add(s)
            db.session.commit()

            return {
                "status": "OK",
                "auth_token": s.auth_token,
            }
        else:
            return {
                "status": "REQUEST_DENIED",
                "error_detail": "Invalid credentials",
            }

class LogoutView(BarkApiEndpoint):
    required_fields_ = {
        "post": [
            ("auth_token", unicode),
        ],
    }

    def post(self, json):
        s = Session.query.filter_by(auth_token=json["auth_token"]).first()
        if s:
            db.session.delete(s)
            db.session.commit()

        return {
            "status": "OK",
        }

class AuthenticationTestingView(BarkAuthenticatedApiEndpoint):
    """
    Just a class for testing API authentication. Thus, no-op by design.
    """

    required_fields_ = { "post": [], "get": [] }

    def post(self, json):
        return { "status": "OK" }

    def get(self, request):
        return { "status": "OK" }
