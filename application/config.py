import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '\x05\x08\\\xf5/\xaf\xbd@'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:z748159@localhost:3306/db'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
