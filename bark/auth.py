from datetime import datetime, timedelta
import os
import base64

from flask import Blueprint, jsonify, request, abort

from bark import db
import user

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

@bp_auth.route('/login', methods=['POST'])
def login():
    if request.headers['Content-Type'] == 'application/json':
        try:
            user_id = user.get_valid(request.json["username"], request.json["password"])
            if user_id:
                s = Session(user_id)
                db.session.add(s)
                db.session.commit()
                return jsonify(auth_token=s.auth_token)
        except (ValueError, KeyError, TypeError) as error:
            abort(400)
    abort(400)


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

