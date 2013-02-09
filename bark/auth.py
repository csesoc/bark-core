# vim: expandtab:ts=4:sw=4

from datetime import datetime, timedelta
import os
import base64

from flask import Blueprint

from bark import db
import user
from bark.api import BarkApiEndpoint

bp_auth = Blueprint('bp_auth', __name__)

auth_token_length = 32
session_timeout = 24

class Session(db.Model):
    __tablename__ = 'sessions'
    auth_token = db.Column(db.String(auth_token_length*2), primary_key=True)
    user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, user):
        self.user = user
        self.create_time = datetime.utcnow()
        self.auth_token = os.urandom(auth_token_length).encode('hex')

class LoginView(BarkApiEndpoint):
    required_fields_ = {
        "post": ["username", "password"],
    }

    def post(self, json):
        user_id = user.get_valid(json["username"], json["password"])
        if user_id:
            s = Session(user_id)
            db.session.add(s)
            db.session.commit()

            return {
                "status": "OK",
                "auth_token": s.auth_token,
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
    view_func=LoginView.as_view('login'),
    methods=["POST"])

bp_auth.add_url_rule(
    "/logout",
    view_func=LogoutView.as_view('logout'),
    methods=["POST"])

def get_user_id(auth_token):
    s = Session.query.filter_by(auth_token=auth_token).first()
    if s:
        if s.create_time + timedelta(hours=session_timeout) > datetime.utcnow():
            return s.user
        else:
            db.session.delete(s)
            return None 
    else:
        return None

