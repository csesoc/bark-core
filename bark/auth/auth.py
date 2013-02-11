from bark import db
from bark.lib.api import BarkApiEndpoint
from bark.auth.models import Session, User

class LoginView(BarkApiEndpoint):
    required_fields_ = {
        "post": [
            ("username", str),
            ("password", str),
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
                "error_detail:": "Invalid credentials",
            }

class LogoutView(BarkApiEndpoint):
    required_fields_ = {
        "post": [
            ("auth_token", str),
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
