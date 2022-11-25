"""The application factory"""
import os
from flask import Flask
from . import odds, auth, db

app = None
def create_app(test_config=None):
    app = Flask(__name__)
   
    if test_config:
        app.config.from_mapping(test_config)
    else:
        env_var = os.getenv('DEPLOY_SETTINGS', 'config.DevelopmentConfig')
        app.config.from_object(env_var)
        
    # register extended parts.
    app.register_blueprint(odds.bp)
    app.register_blueprint(auth.bp)

    # db.init_app(app=app, choice=app.config.get('DATABASE'))

    return app