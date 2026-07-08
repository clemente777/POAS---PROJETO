def test_criar_produto(client, auth_headers):

    response = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome": "Ração Premium",
            "descricao": "Ração para cães adultos",
            "preco": 80.00,
            "estoque": 10
        }
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["nome"] == "Ração Premium"



def test_listar_produtos(client, auth_headers):

    response = client.get(
        "/produtos/",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )



def test_buscar_produto(client, auth_headers):

    criar = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome":"Shampoo Pet",
            "descricao":"Produto para banho",
            "preco":25,
            "estoque":5
        }
    )


    produto_id = criar.json()["id"]


    response = client.get(
        f"/produtos/{produto_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == produto_id



def test_atualizar_produto(client, auth_headers):

    criar = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome":"Produto Antigo",
            "descricao":"Teste",
            "preco":20,
            "estoque":2
        }
    )


    produto_id = criar.json()["id"]


    response = client.put(
        f"/produtos/{produto_id}",
        headers=auth_headers,
        json={
            "nome":"Produto Novo"
        }
    )


    assert response.status_code == 200

    assert response.json()["nome"] == "Produto Novo"



def test_deletar_produto(client, auth_headers):

    criar = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome":"Excluir Produto",
            "descricao":"Teste",
            "preco":10,
            "estoque":1
        }
    )


    produto_id = criar.json()["id"]


    response = client.delete(
        f"/produtos/{produto_id}",
        headers=auth_headers
    )


    assert response.status_code in [200,204]