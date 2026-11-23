import pytest
import requests

@pytest.mark.integracao
@pytest.mark.parametrize("path", ["/dashboard/admin", "/clientes/", "/animais/"])
def test_rotas_protegidas_nao_devem_aceitar_requisicao_anonima(api_url, path):
    r = requests.get(f"{api_url}{path}", timeout=10)
    assert r.status_code in (401, 403, 404, 405), (
        f"{path} respondeu {r.status_code} sem autenticação. "
        "Confirme se o endpoint existe e exige autenticação."
    )

@pytest.mark.integracao
def test_login_rejeita_credenciais_inexistentes(api_url):
    r = requests.post(
        f"{api_url}/login/",
        data={"username": "nao_existe@example.test", "password": "senha-incorreta"},
        timeout=10,
    )
    assert r.status_code in (400, 401, 422), f"Resposta inesperada: {r.status_code}"
