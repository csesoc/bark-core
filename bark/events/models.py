from bark import db

# Another stub. You know the drill...
class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    group = db.relationship("Group")
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    name = db.Column(db.Text)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, group_id, name, description, start_time, end_time):
        self.group_id = group_id
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
