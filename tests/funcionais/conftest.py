import os
import uuid
import pytest
import requests

@pytest.fixture(scope="session")
def api_url():
    return os.getenv("POAS_API_URL", "http://127.0.0.1:8000").rstrip("/")

@pytest.fixture
def sessao_http():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture
def usuario_teste():
    return {
        "nome": f"Cliente Teste {uuid.uuid4().hex[:6]}",
        "email": f"cliente_{uuid.uuid4().hex[:10]}@example.test",
        "senha": "Teste@123456",
        "cpf": "52998224725",
        "telefone": "84999999999",
        "endereco": "Rua de Teste, 100",
    }

@pytest.fixture
def token_cliente():
    token = os.getenv("POAS_CLIENTE_TOKEN")
    if not token:
        pytest.skip("Configure POAS_CLIENTE_TOKEN de uma conta cliente exclusiva para testes.")
    return token
