from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import default_settings

db = SQLAlchemy()

__all__ = ['create_app']

def make_json_error(ex):
   response = jsonify(message=str(ex))
   response.status_code = (ex.code if isinstance(ex, HTTPException)
                           else 500)
   return response

def create_app():
    app = Flask(__name__)
    app.config.from_object(default_settings)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    # Component imports. Must be here to fix cyclical problems
    from auth import bp_auth
    from events import bp_events
    app.register_blueprint(bp_auth)

    db.init_app(app)

    return app
