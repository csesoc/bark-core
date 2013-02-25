from bark import db

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship("Event")

    comments = db.Column(db.Text)
    from_event_token = db.Column(db.Boolean)

    swipes = db.relationship("Swipe")

    def __init__(self, user, event, comments='', from_event_token=False):
        self.user_id = user.id
        self.event_id = event.id
        self.comments = comments
        self.from_event_token = from_event_token

    def to_json(self):
        json = {}
        json['id'] = self.id
        json['user_id'] = self.user_id
        json['event_id'] = self.event_id
        json['comments'] = self.comments
        return json
