import pytest

@pytest.mark.funcional
def test_fluxo_login_e_validacao_do_token(api_url, cliente_http, credenciais_cliente):
    response = cliente_http.post(
        f"{api_url}/login/",
        data={
            "username": credenciais_cliente["email"],
            "password": credenciais_cliente["senha"],
        },
        timeout=15,
    )
    assert response.status_code == 200, (
        f"Login falhou: HTTP {response.status_code} - {response.text[:500]}"
    )
    body = response.json()
    assert body.get("access_token"), f"Resposta não contém access_token: {body}"
    assert body.get("token_type", "bearer").lower() == "bearer"

    protegido = cliente_http.get(
        f"{api_url}/clientes/",
        headers={"Authorization": f"Bearer {body['access_token']}"},
        timeout=15,
    )
    assert protegido.status_code == 200, (
        "O token foi emitido, mas não conseguiu acessar GET /clientes/: "
        f"HTTP {protegido.status_code} - {protegido.text[:500]}"
    )
