from db_session import *

p = Person.query.all()[0]
g = Group.query.all()[0]
u = User.query.all()[0]
e = Event.query.all()[0]
c = Card.query.all()[0]
d = Device.query.all()[0]
s = Swipe.query.all()[0]
