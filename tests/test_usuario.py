def test_criar_usuario(client):

    response = client.post(
        "/usuarios/",
        json={
            "nome": "João",
            "email": "joao@email.com",
            "senha": "123456"
        }
    )


    assert response.status_code == 201

    data = response.json()

    assert data["nome"] == "João"
    assert data["email"] == "joao@email.com"



def test_listar_usuarios(client, auth_headers):

    response = client.get(
        "/usuarios/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )



def test_buscar_usuario(client, auth_headers):

    criar = client.post(
        "/usuarios/",
        headers=auth_headers,
        json={
            "nome":"Maria",
            "email":"maria@email.com",
            "senha":"123456"
        }
    )


    usuario_id = criar.json()["id"]


    response = client.get(
        f"/usuarios/{usuario_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == usuario_id



def test_atualizar_usuario(client, auth_headers):

    criar = client.post(
        "/usuarios/",
        headers=auth_headers,
        json={
            "nome":"Carlos",
            "email":"carlos@email.com",
            "senha":"123456"
        }
    )


    usuario_id = criar.json()["id"]


    response = client.put(
        f"/usuarios/{usuario_id}",
        headers=auth_headers,
        json={
            "nome":"Carlos Atualizado"
        }
    )


    assert response.status_code == 200

    assert response.json()["nome"] == "Carlos Atualizado"



def test_deletar_usuario(client, auth_headers):

    criar = client.post(
        "/usuarios/",
        headers=auth_headers,
        json={
            "nome":"Excluir",
            "email":"excluir@email.com",
            "senha":"123456"
        }
    )


    usuario_id = criar.json()["id"]


    response = client.delete(
        f"/usuarios/{usuario_id}",
        headers=auth_headers
    )


    assert response.status_code == 204