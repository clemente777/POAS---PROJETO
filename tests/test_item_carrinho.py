def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json={
            "nome": "Maria Silva",
            "cpf": "11144477735",
            "telefone": "84999999999",
            "email": "maria@email.com",
            "endereco": "Rua B"
        },
        headers=auth_headers
    )

    assert response.status_code in [200, 201]

    return response.json()



def criar_produto(client, auth_headers):

    response = client.post(
        "/produtos/",
        json={
            "nome": "Ração Premium",
            "descricao": "Ração para cachorro",
            "preco": 50,
            "estoque": 20
        },
        headers=auth_headers
    )

    assert response.status_code in [200, 201]

    return response.json()



def criar_carrinho(client, auth_headers):

    cliente = criar_cliente(
        client,
        auth_headers
    )


    response = client.post(
        "/carrinhos/",
        json={
            "cliente_id": cliente["id"]
        },
        headers=auth_headers
    )


    assert response.status_code in [200,201]

    return response.json()



def criar_item(client, auth_headers):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id": carrinho["id"],
            "produto_id": produto["id"],
            "quantidade": 2
        },
        headers=auth_headers
    )


    assert response.status_code in [200,201]


    return response.json()



# =====================================
# CRIAR ITEM
# =====================================


def test_criar_item(client, auth_headers):

    item = criar_item(
        client,
        auth_headers
    )


    assert item["quantidade"] == 2



# =====================================
# LISTAR
# =====================================


def test_listar_itens(client, auth_headers):

    criar_item(
        client,
        auth_headers
    )


    response = client.get(
        "/itens-carrinho/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert len(response.json()) == 1



# =====================================
# BUSCAR
# =====================================


def test_buscar_item(client, auth_headers):

    item = criar_item(
        client,
        auth_headers
    )


    response = client.get(
        f"/itens-carrinho/{item['id']}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == item["id"]



# =====================================
# ATUALIZAR
# =====================================


def test_atualizar_item(client, auth_headers):

    item = criar_item(
        client,
        auth_headers
    )


    response = client.put(
        f"/itens-carrinho/{item['id']}",
        json={
            "quantidade":5
        },
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["quantidade"] == 5



# =====================================
# DELETAR
# =====================================


def test_deletar_item(client, auth_headers):

    item = criar_item(
        client,
        auth_headers
    )


    response = client.delete(
        f"/itens-carrinho/{item['id']}",
        headers=auth_headers
    )


    assert response.status_code in [
        200,
        204
    ]



# =====================================
# REGRAS DE NEGÓCIO
# =====================================



def test_item_produto_inexistente(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id":carrinho["id"],
            "produto_id":9999,
            "quantidade":1
        },
        headers=auth_headers
    )


    assert response.status_code == 404



def test_item_carrinho_inexistente(
    client,
    auth_headers
):

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id":9999,
            "produto_id":produto["id"],
            "quantidade":1
        },
        headers=auth_headers
    )


    assert response.status_code == 404



def test_quantidade_zero(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id":carrinho["id"],
            "produto_id":produto["id"],
            "quantidade":0
        },
        headers=auth_headers
    )


    assert response.status_code == 400



def test_quantidade_maior_que_estoque(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id":carrinho["id"],
            "produto_id":produto["id"],
            "quantidade":1000
        },
        headers=auth_headers
    )


    assert response.status_code == 400



def test_quantidade_negativa(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )

    produto = criar_produto(
        client,
        auth_headers
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id":carrinho["id"],
            "produto_id":produto["id"],
            "quantidade":-1
        },
        headers=auth_headers
    )


    assert response.status_code == 400