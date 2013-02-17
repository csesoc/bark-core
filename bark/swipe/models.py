from bark import db

# STUB, REMOVE
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)

class Swipe(db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)

    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    event = db.relationship('Event')
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    device = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.String)

    def __init__(self, **kwargs):
        """
        Put in here for safety: *must* call super.__init__
        """

        super(Swipe, self).__init__(**kwargs)
