import unittest, os
from flask import current_app
from screengrab import create_app
from screengrab.extensions import db
from screengrab.models import Screenshot
from datetime import datetime 

basedir = os.path.abspath(os.path.dirname(__file__))

class FlaskBasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
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

    def test_to_json(self):
        given = Screenshot(id=1, 
            source_url="source_url", 
            created_on=datetime(2012, 3, 12, 15, 12, 10), 
            desktop_view="desktop_image_name", 
            mobile_view="mobile_image_name")
        expected = {
            "id": 1, 
            "source_url": "source_url", 
            "created_on": "12-03-2012 15:12:10", 
            "desktop_view": "desktop_image_name", 
            "mobile_view": "mobile_image_name"
        }
        self.assertEqual(given.to_json(), expected)