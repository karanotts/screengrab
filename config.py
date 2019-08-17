import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    THUN_AUTH = os.environ.get('THUN_AUTH')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads/')