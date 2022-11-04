"""The application factory"""
import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE= os.path.join(app.instance_path, 'sportsbetx.sqlite')  # for quick setup will adjust to postgres later
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        env_var = os.getenv('DEPLOY_SETTINGS', 'config.DevelopmentConfig')
        app.config.from_object(env_var)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except(OSError):
        pass

    @app.route('/setup') # for quick setup. will be removed
    def setup():
        return "Setup route"

    # register extended parts.
    from . import db
    db.init_app(app)

    return app