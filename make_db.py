#!/usr/bin/env python
import argparse

from bark import db, create_app
from bark.users.models import User

parser = argparse.ArgumentParser(description="Make changes to the Bark DB")
parser.add_argument("-d", "--drop", help="Drop tables before creation", action="store_true")
args = parser.parse_args()

app = create_app()

# Someone tell me this is the right way to do it.
# Basically, it needs an app.request_context to do db.session calls.
# Normal app.request_context() takes in a WSGI environ object (like a dict),
# meaning that we'd have to fake 9001 params in it.
# This one works by creating a request_context for the unittests.
#
# tl;dr: hacks.
with app.test_request_context():
    if args.drop:
        db.drop_all(app=app)
    db.create_all(app=app)
    u = User("test", "aaa")
    db.session.add(u)
    db.session.commit()
