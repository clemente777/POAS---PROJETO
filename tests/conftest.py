"""Fixtures comuns. O banco de testes deve ser isolado do banco de desenvolvimento."""
import os
import pytest

@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("POAS_API_URL", "http://127.0.0.1:8000")

@pytest.fixture
def credenciais_teste():
    """Credenciais opcionais para testes funcionais; configure via variáveis de ambiente."""
    return {
        "email": os.getenv("POAS_TEST_EMAIL"),
        "senha": os.getenv("POAS_TEST_PASSWORD"),
    }
