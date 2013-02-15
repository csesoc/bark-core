from datetime import datetime, timedelta
import os
import bcrypt

from bark import db

auth_token_length = 32
session_timeout = 24

class Session(db.Model):
    __tablename__ = "sessions"

    auth_token = db.Column(db.String(auth_token_length*2), primary_key=True)
    create_time = db.Column(db.DateTime)

    user = db.relationship("User")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, user):
        self.user = user
        self.create_time = datetime.utcnow()
        self.auth_token = os.urandom(auth_token_length).encode("hex")

    def is_expired(self):
        return self.create_time + timedelta(hours=session_timeout) < datetime.utcnow()

    @classmethod
    def get_user(cls, auth_token):
        session = cls.query.filter_by(auth_token=auth_token).first()
        if session:
            if not session.is_expired():
                return session.user
            else:
                db.session.delete(session)
                return None
        else:
            return None

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True)
    password = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            return user
        else:
            return None

    @classmethod
    def encrypt_password_(cls, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def set_password(self, password):
        self.password = self.encrypt_password_(password)

    def check_password(self, password):
        return self.password is not None and bcrypt.hashpw(password, self.password) == self.password
