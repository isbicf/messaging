# tests/conftest.py
import pytest


@pytest.fixture(scope='function', autouse=True)
def override_config(monkeypatch):
    # Ensure the Flask app never loads the real DB
    monkeypatch.setattr(
        'messaging.config.Config.SQLALCHEMY_DATABASE_URI',
        'sqlite:///:memory:'
    )


@pytest.fixture(scope='session')
def engine():
    from sqlalchemy import create_engine
    from messaging.db.base import Base
    from messaging.db.message import Message    # Don't delete this. message table isn't created if deleted.

    engine = create_engine('sqlite:///:memory:', future=True)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope='function')
def session(engine):
    from sqlalchemy.orm import sessionmaker

    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = TestingSession()
    yield db
    db.rollback()
    db.close()


@pytest.fixture(scope='function')
def client(session, monkeypatch):
    # Patch engine + LocalSession to use *the SAME* session
    monkeypatch.setattr('messaging.db.conn.engine', session.bind)
    monkeypatch.setattr('messaging.db.conn.LocalSession', lambda: session)

    # Mock Celery delay
    monkeypatch.setattr(
        'messaging.task.tasks.process_message.delay',
        lambda _id: None
    )

    from messaging.app import create_app
    app = create_app()

    with app.test_client() as c:
        yield c
