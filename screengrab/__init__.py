from flask import Flask 

import os

from .extensions import db
from .views.api import api
from .views.main import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api/v1')

    return app