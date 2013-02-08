from flask import Flask
import default_settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(default_settings)
    
    #from auth import bp_auth
    #from swipe import swipe

    #app.register_blueprint(bp_auth)
    #app.register_blueprint(swipe)
    return app
