import bcrypt

from bark import db

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
