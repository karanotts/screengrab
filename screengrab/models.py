from .extensions import db

class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(100))
    desktop_view = db.Column(db.String(150))
    mobile_view = db.Column(db.String(150))
    created_on = db.Column(db.DateTime)