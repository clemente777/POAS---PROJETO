def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Item Carrinho",
            "cpf": "11111111111",
            "telefone": "999999999",
            "email": "itemcarrinho@email.com",
            "endereco": "Rua Teste"
        }
    )

    print("CLIENTE:", response.status_code)
    print("CLIENTE JSON:", response.json())

    assert response.status_code in [200, 201], response.json()

    return response.json()["id"]


def criar_produto(client, auth_headers):

    response = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome": "Produto Item",
            "descricao": "Teste",
            "preco": 30,
            "estoque": 10
        }
    )

    print("PRODUTO:", response.status_code)
    print("PRODUTO JSON:", response.json())

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

    print("CARRINHO STATUS:", response.status_code)
    print("CARRINHO JSON:", response.json())

    assert response.status_code in [200, 201]

    return response.json()["id"]


def criar_item_carrinho(client, auth_headers):

    produto_id = criar_produto(
        client,
        auth_headers
    )

    carrinho_id = criar_carrinho(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        headers=auth_headers,
        json={
            "produto_id": produto_id,
            "carrinho_id": carrinho_id,
            "quantidade": 2
        }
    )

    print("ITEM STATUS:", response.status_code)
    print("ITEM JSON:", response.json())

    assert response.status_code in [200, 201]

    return response.json()["id"]



def test_criar_item(client, auth_headers):

    item_id = criar_item_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        f"/itens-carrinho/{item_id}",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_listar_itens(client, auth_headers):

    response = client.get(
        "/itens-carrinho/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_item(client, auth_headers):

    item_id = criar_item_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        f"/itens-carrinho/{item_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == item_id



def test_atualizar_item(client, auth_headers):

    item_id = criar_item_carrinho(
        client,
        auth_headers
    )


    response = client.put(
        f"/itens-carrinho/{item_id}",
        headers=auth_headers,
        json={
            "quantidade": 5
        }
    )


    assert response.status_code == 200

    assert response.json()["quantidade"] == 5



def test_deletar_item(client, auth_headers):

    item_id = criar_item_carrinho(
        client,
        auth_headers
    )


    response = client.delete(
        f"/itens-carrinho/{item_id}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]