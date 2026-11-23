import pytest
import requests

@pytest.mark.integracao
def test_api_responde(api_url):
    r = requests.get(f"{api_url}/openapi.json", timeout=10)
    assert r.status_code == 200
    assert "openapi" in r.json()

@pytest.mark.integracao
def test_documentacao_openapi_contem_rotas_de_negocio(api_url):
    spec = requests.get(f"{api_url}/openapi.json", timeout=10).json()
    paths = " ".join(spec.get("paths", {}).keys()).lower()
    termos = ["login", "animal", "agendamento", "produto"]
    ausentes = [termo for termo in termos if termo not in paths]
    assert not ausentes, f"Rotas esperadas não encontradas no OpenAPI: {ausentes}"
