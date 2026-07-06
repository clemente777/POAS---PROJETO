import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.auth.token import create_access_token


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_headers():

    token = create_access_token(
        {
            "sub": "admin@admin.com"
        }
    )

    return {
        "Authorization": f"Bearer {token}"
    }