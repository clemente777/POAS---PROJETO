from backend.models.token_revogado_model import TokenRevogado


def test_logout(client, auth_headers, session):

    response = client.post(
        "/login/logout",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Logout realizado com sucesso."
    }

    token = auth_headers["Authorization"].replace("Bearer ", "")

    token_revogado = (
        session.query(TokenRevogado)
        .filter(TokenRevogado.token == token)
        .first()
    )

    assert token_revogado is not None

def test_token_revogado(client, auth_headers):

    logout = client.post(
        "/login/logout",
        headers=auth_headers
    )

    assert logout.status_code == 200

    response = client.get(
        "/usuarios/",
        headers=auth_headers
    )

    assert response.status_code == 401
    