from bark import db

class Swipe(db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(db.ForeignKey("Device"))
    device = db.relationship("Device")

    person_id = db.Person(db.ForeignKey("Device"))
    person = db.relationship("Person")

    timestamp = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        """
        Put in here for safety: *must* call super.__init__
        """

        super(Swipe, self).__init__(**kwargs)
