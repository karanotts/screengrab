import os
basedir = os.path.abspath(os.path.dirname(__file__))


PORT = 5000
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'data.db')
