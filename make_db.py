#!/usr/bin/env python

from bark import db, create_app
from bark.models import *

app = create_app()

# Someone tell me this is the right way to do it.
# Basically, it needs an app.request_context to do db.session calls.
# Normal app.request_context() takes in a WSGI environ object (like a dict),
# meaning that we'd have to fake 9001 params in it.
# This one works by creating a request_context for the unittests.
#
# tl;dr: hacks.
with app.test_request_context():
    db.create_all(app=app)
    u = User('test', 'aaa')
    db.session.add(u)
    db.session.commit()
