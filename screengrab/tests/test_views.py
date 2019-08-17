import unittest, os
from flask import current_app
from screengrab import create_app
from screengrab.extensions import db
from screengrab.models import Screenshot
from datetime import datetime 

basedir = os.path.abspath(os.path.dirname(__file__))

class FlaskViewsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            db.session.commit()
        self.client = self.app.test_client(use_cookies=False)

    def test_main_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('To create a screenshot' in response.get_data(as_text=True))

    def test_api(self):
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Documentation' in response.get_data(as_text=True))

    def test_api_screenshots(self):

        screenshot = Screenshot(
            id=123456789, 
            source_url="source_url", 
            created_on=datetime(2012, 3, 12, 15, 12, 10), 
            desktop_view="desktop_image_name", 
            mobile_view="mobile_image_name"
            )
        db.session.add(screenshot)
        db.session.commit()

        response = self.client.get('/api/v1/screenshots/123456789')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('mobile_image_name' in response.get_data(as_text=True))
