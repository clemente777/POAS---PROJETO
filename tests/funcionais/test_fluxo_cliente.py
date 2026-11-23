import pytest

@pytest.mark.funcional
def test_cliente_autenticado_acessa_animais(api_url, cliente_http, token_cliente):
    response = cliente_http.get(
        f"{api_url}/animais/",
        headers={"Authorization": f"Bearer {token_cliente}"},
        timeout=15,
    )
    assert response.status_code == 200, (
        f"Cliente autenticado não conseguiu consultar animais: "
        f"HTTP {response.status_code} - {response.text[:500]}"
    )
    assert isinstance(response.json(), (list, dict))

@pytest.mark.funcional
def test_cliente_autenticado_acessa_agendamentos(api_url, cliente_http, token_cliente):
    response = cliente_http.get(
        f"{api_url}/agendamentos/",
        headers={"Authorization": f"Bearer {token_cliente}"},
        timeout=15,
    )
    assert response.status_code == 200, (
        f"Cliente autenticado não conseguiu consultar agendamentos: "
        f"HTTP {response.status_code} - {response.text[:500]}"
    )
    assert isinstance(response.json(), (list, dict))
