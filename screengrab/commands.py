import click 

from flask.cli import with_appcontext
from sqlalchemy.sql import func

from .extensions import db
from .models import Screenshot

@click.command(name='create_db')
@with_appcontext
def create_db():
    db.create_all()

@click.command(name='test_query')
@with_appcontext
def test_query():
    screenshots = db.session.query(Screenshot).all()
    last_screenshot_loc = Screenshot.query.order_by(Screenshot.id.desc()).first().desktop_view
    print("All objects in Screenshots:" , screenshots)
    print("Last screenshot location is:", last_screenshot_loc)