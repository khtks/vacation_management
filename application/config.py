import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(8)


class ProdConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://sam:z748159!@localhost:3306/prod_db'


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://sam:z748159!@localhost:3306/dev_db'


class TestConfig(Config):
    ENV = 'testing'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://sam:z748159!@localhost:3306/test_db'


config_name = dict(
    prod=ProdConfig,
    dev=DevConfig,
    test=TestConfig
)