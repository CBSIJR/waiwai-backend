import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from backend.models import Base
from backend.waiwai import app


class SADeListener(object):
    def __init__(self, class_, event_, callable_):
        self.class_ = class_
        self.event = event_
        self.callable_ = callable_

    def __enter__(self):
        event.remove(self.class_, self.event, self.callable_)

    def __exit__(self, type_, value, tb):
        event.listen(self.class_, self.event, self.callable_)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)
