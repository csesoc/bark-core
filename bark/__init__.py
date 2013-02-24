from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import bark.config

db = SQLAlchemy()

__all__ = ['create_app']

def make_json_error(ex):
   response = jsonify(message=str(ex))
   response.status_code = (ex.code if isinstance(ex, HTTPException)
                           else 500)
   return response

def create_app():
    app = Flask(__name__)
    app.config.from_object(bark.config)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    # Component imports. Must be here to fix cyclical problems
    from auth import bp_auth
    app.register_blueprint(bp_auth)

    from swipes import bp_swipe
    app.register_blueprint(bp_swipe, url_prefix='/swipe')

    from events import bp_events
    app.register_blueprint(bp_swipe, url_prefix='/events')

    db.init_app(app)

    return app
