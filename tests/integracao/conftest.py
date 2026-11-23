"""Integração via HTTP.

Por padrão, a API precisa estar iniciada. Defina POAS_API_URL se não usar localhost:8000.
Os testes que alteram dados usam identificadores/e-mails exclusivos.
"""
import os
import uuid
import pytest
import requests

@pytest.fixture(scope="session")
def api_url():
    return os.getenv("POAS_API_URL", "http://127.0.0.1:8000").rstrip("/")

@pytest.fixture
def http():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture
def email_unico():
    return f"teste_{uuid.uuid4().hex[:12]}@example.test"

@pytest.fixture
def token_admin():
    token = os.getenv("POAS_ADMIN_TOKEN")
    if not token:
        pytest.skip("Configure POAS_ADMIN_TOKEN com um token de administrador de teste.")
    return token

@pytest.fixture
def token_veterinario():
    token = os.getenv("POAS_VETERINARIO_TOKEN")
    if not token:
        pytest.skip("Configure POAS_VETERINARIO_TOKEN com um token de veterinário de teste.")
    return token

@pytest.fixture
def token_cliente():
    token = os.getenv("POAS_CLIENTE_TOKEN")
    if not token:
        pytest.skip("Configure POAS_CLIENTE_TOKEN com um token de cliente de teste.")
    return token
