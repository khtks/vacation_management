import pytest
from application import create_app, db as _db, db
from sqlalchemy import create_engine, log


@pytest.fixture(scope='session')
def app():
    _app = create_app('test')
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def connection(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    connection = engine.connect()

    yield connection

    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = _db.scoped_session(_db.sessionmaker(bind=connection))
    db.session = session

    yield session

    session.close()
    transaction.rollback()
