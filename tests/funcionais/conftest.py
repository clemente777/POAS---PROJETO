import os
import pytest
import requests

@pytest.fixture
def cliente_http():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    yield s
    s.close()

@pytest.fixture
def credenciais_cliente():
    email = os.getenv("POAS_TEST_EMAIL")
    senha = os.getenv("POAS_TEST_PASSWORD")
    if not email or not senha:
        pytest.skip("Defina POAS_TEST_EMAIL e POAS_TEST_PASSWORD de uma conta cliente de testes.")
    return {"email": email, "senha": senha}

@pytest.fixture
def token_cliente():
    token = os.getenv("POAS_CLIENTE_TOKEN")
    if not token:
        pytest.skip("Defina POAS_CLIENTE_TOKEN com token de uma conta cliente de testes.")
    return token
