import os
# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ADMIN_CODE=os.environ['ADMIN_CODE']
    SERVER_NAME=os.environ['SERVER_NAME']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # RuntimeError: Application was not able to create a URL adapter for request independent URL generation. You might be able to fix this by setting the SERVER_NAME config variable.


class TestingConfig(Config):
    TESTING = True
