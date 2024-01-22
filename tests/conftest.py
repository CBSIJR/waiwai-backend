import pytest

from fastapi.testclient import TestClient

from backend.waiwai import app
from backend.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
