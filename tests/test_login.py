def criar_usuario(client):

    return client.post(
        "/usuarios/",
        json={
            "nome":"Admin",
            "email":"admin@test.com",
            "senha":"123456"
        }
    )



def test_login_sucesso(client):


    criar_usuario(client)



    response = client.post(
        "/login/",
        data={
            "username":"admin@test.com",
            "password":"123456"
        }
    )


    assert response.status_code == 200


    dados = response.json()


    assert "access_token" in dados

    assert dados["token_type"] == "bearer"



def test_login_usuario_inexistente(client):


    response = client.post(
        "/login/",
        data={
            "username":"teste@test.com",
            "password":"123456"
        }
    )


    assert response.status_code == 401



def test_login_senha_errada(client):


    criar_usuario(client)



    response = client.post(
        "/login/",
        data={
            "username":"admin@test.com",
            "password":"errada"
        }
    )


    assert response.status_code == 401