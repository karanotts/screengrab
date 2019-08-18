import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    THUN_AUTH = os.environ.get('THUN_AUTH')
    UPLOAD_FOLDER = os.path.join(basedir, 'screengrab/static/uploads/')
