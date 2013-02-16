from bark import db

group_owners = db.Table('group_owners',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

group_members = db.Table('group_members',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'))
)

class Group(db.Model):
    __tablename__ = "groups"
    
    id = db.Column(db.Integer, primary_key = True)

    owners = db.relationship("User", secondary=group_owners,
                             backref='owned_groups')
    members = db.relationship("Student", secondary=group_members,
                              backref='group_memberships')

    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)

    def __init__(self, name, owners, description=""):
        self.name = name
        self.owners = owners
        self.description = description
