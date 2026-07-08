def criar_cliente(client, auth_headers, email="carrinho@email.com"):

    response = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Carrinho",
            "cpf": "33333333333",
            "telefone": "999999999",
            "email": email,
            "endereco": "Rua Teste"
        }
    )

    assert response.status_code in [200, 201], response.json()

    return response.json()["id"]



def criar_carrinho(client, auth_headers):

    cliente_id = criar_cliente(
        client,
        auth_headers
    )

    response = client.post(
        "/carrinhos/",
        headers=auth_headers,
        json={
            "cliente_id": cliente_id
        }
    )

    assert response.status_code in [200, 201], response.json()

    return response.json()["id"], cliente_id



def test_criar_carrinho(client, auth_headers):

    carrinho_id, cliente_id = criar_carrinho(
        client,
        auth_headers
    )

    response = client.get(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cliente_id"] == cliente_id



def test_buscar_carrinho(client, auth_headers):

    carrinho_id, _ = criar_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == carrinho_id



def test_atualizar_carrinho(client, auth_headers):

    carrinho_id, cliente_id = criar_carrinho(
        client,
        auth_headers
    )


    response = client.put(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers,
        json={
            "cliente_id": cliente_id
        }
    )


    assert response.status_code == 200



def test_deletar_carrinho(client, auth_headers):

    carrinho_id, _ = criar_carrinho(
        client,
        auth_headers
    )


    response = client.delete(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]