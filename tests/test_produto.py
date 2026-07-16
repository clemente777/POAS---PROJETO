def criar_produto(client, auth_headers):

    response = client.post(
        "/produtos/",
        json={
            "nome": "Ração Premium",
            "descricao": "Ração para cães adultos",
            "preco": 120.50,
            "estoque": 10
        },
        headers=auth_headers
    )

    assert response.status_code in [200,201]

    return response.json()



def test_criar_produto(client, auth_headers):

    produto = criar_produto(
        client,
        auth_headers
    )

    assert produto["nome"] == "Ração Premium"
    assert produto["estoque"] == 10



def test_listar_produtos(client, auth_headers):

    criar_produto(
        client,
        auth_headers
    )


    response = client.get(
        "/produtos/",
        headers=auth_headers
    )


    assert response.status_code == 200

    dados = response.json()

    assert len(dados) == 1



def test_buscar_produto(client, auth_headers):

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.get(
        f"/produtos/{produto['id']}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == produto["id"]



def test_atualizar_produto(client, auth_headers):

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.put(
        f"/produtos/{produto['id']}",
        json={
            "nome":"Ração Atualizada"
        },
        headers=auth_headers
    )


    assert response.status_code == 200

    assert (
        response.json()["nome"]
        ==
        "Ração Atualizada"
    )



def test_deletar_produto(client, auth_headers):

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.delete(
        f"/produtos/{produto['id']}",
        headers=auth_headers
    )


    assert response.status_code in [
        200,
        204
    ]



# ==========================
# REGRAS DE NEGÓCIO
# ==========================


def test_produto_sem_nome(client, auth_headers):

    response = client.post(
        "/produtos/",
        json={
            "descricao": "Produto teste",
            "preco": 10,
            "estoque": 5
        },
        headers=auth_headers
    )


    assert response.status_code == 422



def test_produto_estoque_negativo(client, auth_headers):

    response = client.post(
        "/produtos/",
        json={
            "nome":"Produto",
            "descricao":"Teste",
            "preco":10,
            "estoque":-1
        },
        headers=auth_headers
    )


    assert response.status_code == 400



def test_produto_preco_negativo(client, auth_headers):

    response = client.post(
        "/produtos/",
        json={
            "nome":"Produto",
            "descricao":"Teste",
            "preco":-10,
            "estoque":5
        },
        headers=auth_headers
    )


    assert response.status_code == 400