import pytest


# ==========================================
# TESTE DE LOGOUT
# ==========================================

def test_logout(
    client,
    auth_headers
):

    response = client.post(
        "/logout",
        headers=auth_headers
    )


    assert response.status_code == 200


    dados = response.json()


    assert dados["message"] == (
        "Logout realizado com sucesso."
    )



# ==========================================
# TESTE TOKEN REVOGADO
# ==========================================

def test_token_revogado(
    client,
    auth_headers
):

    # Faz logout
    response = client.post(
        "/logout",
        headers=auth_headers
    )


    assert response.status_code == 200



    # Tenta acessar uma rota protegida
    resposta = client.get(
        "/clientes/",
        headers=auth_headers
    )


    assert resposta.status_code == 401


    assert resposta.json()["detail"] == (
        "Token revogado."
    )



# ==========================================
# TESTE SEM TOKEN
# ==========================================

def test_logout_sem_token(
    client
):

    response = client.post(
        "/logout"
    )


    assert response.status_code == 401



# ==========================================
# TESTE TOKEN INVALIDO
# ==========================================

def test_logout_token_invalido(
    client
):

    response = client.post(
        "/logout",
        headers={
            "Authorization":
            "Bearer token_errado"
        }
    )


    assert response.status_code == 401