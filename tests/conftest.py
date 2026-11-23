"""Configuração compartilhada da suíte Petonline24h."""
import os
import pytest
import requests

@pytest.fixture(scope="session")
def api_url():
    return os.getenv("POAS_API_URL", "http://127.0.0.1:8000").rstrip("/")

@pytest.fixture(scope="session")
def http_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()

@pytest.fixture(scope="session")
def openapi(api_url, http_session):
    response = http_session.get(f"{api_url}/openapi.json", timeout=15)
    assert response.status_code == 200, (
        f"Não foi possível acessar {api_url}/openapi.json: "
        f"HTTP {response.status_code} - {response.text[:500]}"
    )
    return response.json()

@pytest.fixture
def token_admin():
    token = os.getenv("POAS_ADMIN_TOKEN")
    if not token:
        pytest.skip("Defina POAS_ADMIN_TOKEN com token de uma conta admin exclusiva de testes.")
    return token

@pytest.fixture
def token_veterinario():
    token = os.getenv("POAS_VETERINARIO_TOKEN")
    if not token:
        pytest.skip("Defina POAS_VETERINARIO_TOKEN com token de uma conta veterinária de testes.")
    return token

@pytest.fixture
def token_cliente():
    token = os.getenv("POAS_CLIENTE_TOKEN")
    if not token:
        pytest.skip("Defina POAS_CLIENTE_TOKEN com token de uma conta cliente de testes.")
    return token
