import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from messaging.db.base import Base
from messaging.db.message import Message  # Don't delete this. message table isn't created if deleted.


# monkeypatch = function scoped fixture
@pytest.fixture(scope='function', autouse=True)
def override_config(monkeypatch):
    # Override DB URI so that the app uses testing DB
    monkeypatch.setattr(
        'messaging.config.Config.SQLALCHEMY_DATABASE_URI',
        'sqlite:///:memory:'
    )


@pytest.fixture(scope='session')
def engine():
    engine = create_engine('sqlite:///:memory:', future=True)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope='session')
def session(engine):
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = TestingSession()
    yield db
    db.rollback()
    db.close()


# monkeypatch = function scoped fixture
@pytest.fixture(scope='function')
def client(session, monkeypatch):
    # Replacing app's engine and session with the testing's
    monkeypatch.setattr('messaging.db.conn.engine', session.bind)
    monkeypatch.setattr('messaging.db.conn.LocalSession', lambda: session)

    # Replacing Celery async call
    monkeypatch.setattr('messaging.task.tasks.process_message.delay', lambda _id: None)

    from messaging.app import create_app    # Must import here. Create replaced DB
    app = create_app()

    with app.test_client() as c:
        yield c
