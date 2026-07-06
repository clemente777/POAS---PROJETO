import pytest
from httpx import AsyncClient

from main import app


@pytest.fixture
def client():
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def auth_headers():
    # depois você troca por login real
    return {
        "Authorization": "Bearer TOKEN_TESTE"
    }