def criar_produto(client, auth_headers):

    response = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome":"Produto Item",
            "descricao":"Teste",
            "preco":30,
            "estoque":10
        }
    )


    return response.json()["id"]



def criar_carrinho(client, auth_headers):

    response = client.post(
        "/carrinhos/",
        headers=auth_headers,
        json={}
    )


    return response.json()["id"]



def test_criar_item(client, auth_headers):

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
            "produto_id":produto_id,
            "carrinho_id":carrinho_id,
            "quantidade":2
        }
    )


    assert response.status_code in [200,201]



def test_listar_itens(client, auth_headers):

    response = client.get(
        "/itens-carrinho/",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_buscar_item(client, auth_headers):

    produto_id = criar_produto(
        client,
        auth_headers
    )

    carrinho_id = criar_carrinho(
        client,
        auth_headers
    )


    criar = client.post(
        "/itens-carrinho/",
        headers=auth_headers,
        json={
            "produto_id":produto_id,
            "carrinho_id":carrinho_id,
            "quantidade":1
        }
    )


    item_id = criar.json()["id"]


    response = client.get(
        f"/itens-carrinho/{item_id}",
        headers=auth_headers
    )


    assert response.status_code == 200