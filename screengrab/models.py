from .extensions import db
from datetime import datetime

class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(100))
    desktop_view = db.Column(db.String(150))
    mobile_view = db.Column(db.String(150))
    created_on = db.Column(db.DateTime)

    def to_json(self):
        screenshot_json = {
            'id': self.id,
            'source_url': self.source_url,
            'desktop_view': self.desktop_view,
            'mobile_view': self.mobile_view,
            'created_on': datetime.strftime(self.created_on, '%d-%m-%Y %H:%M:%S')
        }
        return screenshot_json