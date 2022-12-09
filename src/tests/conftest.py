import pytest
from starlette.testclient import TestClient
from app.main import app


@pytest.fixture
def test_app():
    client = TestClient(app)
    return client
