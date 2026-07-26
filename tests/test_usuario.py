def usuario_json():

    return {

        "nome":"Carlos",

        "email":"carlos@email.com",

        "senha":"123456"

    }



def test_criar_usuario(client):


    response = client.post(
        "/usuarios/",
        json=usuario_json()
    )


    assert response.status_code == 201


    dados = response.json()


    assert dados["nome"] == "Carlos"

    assert dados["email"] == "carlos@email.com"



def test_criar_usuario_email_duplicado(client):


    client.post(
        "/usuarios/",
        json=usuario_json()
    )


    response = client.post(
        "/usuarios/",
        json=usuario_json()
    )


    assert response.status_code in [400,409]



def test_listar_usuarios(client, auth_headers):


    client.post(
        "/usuarios/",
        json=usuario_json()
    )


    response = client.get(
        "/usuarios/",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert len(
        response.json()
    ) >= 1




def test_buscar_usuario(client, auth_headers):


    criar = client.post(
        "/usuarios/",
        json=usuario_json()
    )


    id = criar.json()["id"]



    response = client.get(
        f"/usuarios/{id}",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert response.json()["id"] == id




def test_atualizar_usuario(client, auth_headers):


    criar = client.post(
        "/usuarios/",
        json=usuario_json()
    )


    id = criar.json()["id"]



    response = client.put(
        f"/usuarios/{id}",
        headers=auth_headers,
        json={
            "nome":"Novo Nome"
        }
    )


    assert response.status_code == 200


    assert response.json()["nome"] == "Novo Nome"




def test_deletar_usuario(client, auth_headers):


    criar = client.post(
        "/usuarios/",
        json={
            "nome":"Usuario Teste",
            "email":"teste_delete@email.com",
            "senha":"123456"
        }
    )


    id = criar.json()["id"]


    response = client.delete(
        f"/usuarios/{id}",
        headers=auth_headers
    )


    assert response.status_code == 204