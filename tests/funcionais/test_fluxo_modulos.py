import pytest

@pytest.mark.funcional
@pytest.mark.parametrize("path", [
    "/animais/", "/agendamentos/", "/atendimentos/",
    "/vacinas/", "/aplicacoes-vacina/", "/produtos/",
])
def test_api_retorna_resposta_autenticada_para_modulos(
    api_url, cliente_http, token_cliente, openapi, path
):
    if path not in openapi.get("paths", {}):
        pytest.skip(f"A rota {path} não está documentada nesta instalação.")
    response = cliente_http.get(
        f"{api_url}{path}",
        headers={"Authorization": f"Bearer {token_cliente}"},
        timeout=15,
    )
    assert response.status_code in (200, 403), (
        f"Resposta inesperada em GET {path}: "
        f"HTTP {response.status_code} - {response.text[:500]}"
    )
    if response.status_code == 200:
        assert isinstance(response.json(), (list, dict))
