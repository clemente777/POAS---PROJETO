def test_criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"João Silva",
            "telefone":"84999999999",
            "email":"joao@email.com"
        }
    )


    assert response.status_code in [200,201]

    assert response.json()["nome"] == "João Silva"



def test_listar_clientes(client, auth_headers):

    response = client.get(
        "/clientes/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_cliente(client, auth_headers):

    criar = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Maria",
            "telefone":"888888888",
            "email":"maria@email.com"
        }
    )


    cliente_id = criar.json()["id"]


    response = client.get(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == cliente_id



def test_atualizar_cliente(client, auth_headers):

    criar = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Cliente Teste",
            "telefone":"111111",
            "email":"teste@email.com"
        }
    )


    cliente_id = criar.json()["id"]


    response = client.put(
        f"/clientes/{cliente_id}",
        headers=auth_headers,
        json={
            "nome":"Cliente Alterado"
        }
    )


    assert response.status_code == 200



def test_deletar_cliente(client, auth_headers):

    criar = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Excluir",
            "telefone":"99999",
            "email":"excluir@email.com"
        }
    )


    cliente_id = criar.json()["id"]


    response = client.delete(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )


    assert response.status_code in [200,204]