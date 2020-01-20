import pytest
from application import create_app, db
from application.models.model import *

Session = db.sessionmaker()


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app('test')
    yield _app


@pytest.yield_fixture(scope='session')
def tables():
    db.create_all()
    yield
    db.drop_all()


@pytest.yield_fixture(scope='function')
def dbsession():
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.session
    yield session

    session.close()
    transaction.rollback()


db.session.remove
