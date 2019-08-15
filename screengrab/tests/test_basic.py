import unittest, os
from flask import current_app
from screengrab import create_app
from screengrab.extensions import db
from screengrab.models import Screenshot

basedir = os.path.abspath(os.path.dirname(__file__))

class FlaskBasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['TESTING'] = True
        self.app.config['CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test2.db')
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)