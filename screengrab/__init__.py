from flask import Flask 

import os

from .extensions import db
from .commands import create_db, test_query
from .views.api import api
from .views.main import main


def create_app():
    app = Flask(__name__, instance_path='/')

    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api/v1')

    app.cli.add_command(create_db)
    app.cli.add_command(test_query)

    return app