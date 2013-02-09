from flask import Blueprint

from bark import db, user
from bark.api import BarkApiEndpoint
from bark.models import Session, User

bp_auth = Blueprint("bp_auth", __name__)

class LoginView(BarkApiEndpoint):
    required_fields_ = {
        "post": ["username", "password"],
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
        "post": ["auth_token"],
    }

    def post(self, json):
        s = Session.query.filter_by(auth_token=json["auth_token"]).first()
        if s:
            db.session.delete(s)
            db.session.commit()

        return {
            "status": "OK",
        }

bp_auth.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login"),
    methods=["POST"])

bp_auth.add_url_rule(
    "/logout",
    view_func=LogoutView.as_view("logout"),
    methods=["POST"])
