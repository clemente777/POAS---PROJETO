import pytest


def criar_usuario_para_login(client):

    response = client.post(
        "/usuarios/",
        json={
            "nome": "Usuario Login",
            "email": "login@email.com",
            "senha": "123456"
        }
    )

    assert response.status_code in [200, 201]

    return response.json()



def test_login_sem_dados(client):

    response = client.post(
        "/login/",
        data={}
    )

    assert response.status_code in [400, 401, 422]



def test_login_usuario_inexistente(client):

    response = client.post(
        "/login/",
        data={
            "username": "naoexiste@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401



def test_login_senha_errada(client):

    criar_usuario_para_login(client)


    response = client.post(
        "/login/",
        data={
            "username": "login@email.com",
            "password": "senha_errada"
        }
    )


    assert response.status_code == 401



def test_login_sucesso(client):

    criar_usuario_para_login(client)


    response = client.post(
        "/login/",
        data={
            "username": "login@email.com",
            "password": "123456"
        }
    )


    assert response.status_code == 200


    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"



def test_login_formato_invalido(client):

    response = client.post(
        "/login/",
        data={
            "username": "",
            "password": ""
        }
    )


    assert response.status_code in [401, 422]