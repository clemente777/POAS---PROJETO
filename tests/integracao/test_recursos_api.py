import pytest
import requests

@pytest.mark.integracao
@pytest.mark.parametrize("path", [
    "/usuarios/", "/clientes/", "/animais/", "/agendamentos/",
    "/atendimentos/", "/vacinas/", "/aplicacoes-vacina/",
    "/produtos/", "/carrinhos/",
])
def test_recurso_tem_endpoint_documentado(api_url, path):
    spec = requests.get(f"{api_url}/openapi.json", timeout=10).json()
    assert path in spec.get("paths", {}), (
        f"Endpoint {path} não consta no OpenAPI. "
        "Se a rota real tiver outro caminho, ajuste este caso de teste."
    )

@pytest.mark.integracao
def test_endpoint_de_login_esta_documentado(api_url):
    spec = requests.get(f"{api_url}/openapi.json", timeout=10).json()
    assert "/login/" in spec.get("paths", {})
