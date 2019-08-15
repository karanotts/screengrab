import click 

from flask.cli import with_appcontext

from .extensions import db
from .models import Screenshot


@click.command(name='create_db')
@with_appcontext
def create_db():
    db.create_all()