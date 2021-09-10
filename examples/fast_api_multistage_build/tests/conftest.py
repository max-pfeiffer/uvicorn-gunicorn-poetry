import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="class")
def client(request):
    request.cls.client = TestClient(app)
