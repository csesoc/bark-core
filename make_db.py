#!/usr/bin/env python
import argparse
import datetime

from db_session import *

parser = argparse.ArgumentParser(description="Make changes to the Bark DB")
parser.add_argument("-d", "--drop", help="Drop tables before creation", action="store_true")
parser.add_argument("-t", "--test-data", help="Populate DB with test data", action="store_true")
args = parser.parse_args()

app = create_app()

# Someone tell me this is the right way to do it.
# Basically, it needs an app.request_context to do db.session calls.
# Normal app.request_context() takes in a WSGI environ object (like a dict),
# meaning that we'd have to fake 9001 params in it.
# This one works by creating a request_context for the unittests.
#
# tl;dr: hacks.
if args.drop:
    db.drop_all(app=app)
db.create_all(app=app)
if args.test_data:

    u = User("username", "password")
    db.session.add(u)

    g = Group("Test Group Please Ignore", "Just a test group")
    g.add_owner(u)
    db.session.add(g)

    d = datetime.datetime.now()
    e = Event(g, 'test_event', 'description', d, d)
    db.session.add(e)

    p = Person(123456)
    db.session.add(p)

    db.session.commit()
