from datetime import datetime, timedelta
import os
from bark import db

auth_token_length = 32
session_timeout = 24

class Session(db.Model):
    __tablename__ = "sessions"
    auth_token = db.Column(db.String(auth_token_length*2), primary_key=True)
    user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, user):
        self.user = user
        self.create_time = datetime.utcnow()
        self.auth_token = os.urandom(auth_token_length).encode("hex")

    def is_expired(self):
        return s.create_time + timedelta(hours=session_timeout) < datetime.utcnow()

    @classmethod
    def get_user_id(cls, auth_token):
        session = cls.query.filter_by(auth_token=auth_token).first()
        if session:
            if not session.is_expired:
                return session.user
            else:
                db.session.delete(session)
                return None 
        else:
            return None
