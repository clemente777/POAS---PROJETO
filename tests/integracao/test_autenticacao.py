import pytest

ROTAS_PROTEGIDAS = [
    ("/clientes/", "get"),
    ("/animais/", "get"),
    ("/agendamentos/", "get"),
    ("/atendimentos/", "get"),
    ("/dashboard/admin", "get"),
]

@pytest.mark.integracao
@pytest.mark.parametrize(("path", "method"), ROTAS_PROTEGIDAS)
def test_rotas_protegidas_rejeitam_usuario_anonimo(api_url, http_session, openapi, path, method):
    # Não mascara endpoint inexistente como sucesso: rota precisa existir no OpenAPI.
    assert path in openapi["paths"], f"Rota {path} não consta no OpenAPI; ajuste o caminho ao contrato real."
    response = getattr(http_session, method)(
        f"{api_url}{path}", timeout=15
    )
    assert response.status_code in (401, 403), (
        f"{method.upper()} {path} deveria exigir autenticação, "
        f"mas respondeu {response.status_code}: {response.text[:500]}"
    )

@pytest.mark.integracao
def test_login_rejeita_credenciais_inexistentes(api_url, http_session):
    response = http_session.post(
        f"{api_url}/login/",
        data={
            "username": "usuario_inexistente_9f13@example.test",
            "password": "Senha_Incorreta_123!",
        },
        timeout=15,
    )
    assert response.status_code in (400, 401), (
        f"Login com credenciais inexistentes deveria falhar com 400/401; "
        f"recebido {response.status_code}: {response.text[:500]}"
    )

@pytest.mark.integracao
def test_login_rejeita_requisicao_sem_campos(api_url, http_session):
    response = http_session.post(f"{api_url}/login/", data={}, timeout=15)
    assert response.status_code == 422, (
        f"Esperado 422 para formulário incompleto, recebido {response.status_code}."
    )
