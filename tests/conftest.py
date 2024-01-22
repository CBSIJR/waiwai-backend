import pytest
from fastapi.testclient import TestClient
from backend.waiwai import app

@pytest.fixture
def client():
    return TestClient(app)