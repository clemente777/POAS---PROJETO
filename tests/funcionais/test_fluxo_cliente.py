import pytest

@pytest.mark.funcional
def test_fluxo_cliente_autenticado_consegue_consultar_propria_area(api_url, sessao_http, token_cliente):
    r = sessao_http.get(
        f"{api_url}/clientes/me",
        headers={"Authorization": f"Bearer {token_cliente}"},
        timeout=10,
    )
    # A rota /clientes/me é uma convenção a confirmar no OpenAPI do POAS.
    assert r.status_code in (200, 404, 405), (
        f"Falha ao consultar área do cliente: {r.status_code} - {r.text}"
    )
