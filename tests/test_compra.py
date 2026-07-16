def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json={
            "nome": "Carlos Silva",
            "cpf": "52998224725",
            "telefone": "84999999999",
            "email": "carlos@email.com",
            "endereco": "Rua C"
        },
        headers=auth_headers
    )

    assert response.status_code in [200, 201]

    return response.json()



def criar_produto(client, auth_headers, estoque=10):

    response = client.post(
        "/produtos/",
        json={
            "nome": "Shampoo Pet",
            "descricao": "Produto para banho",
            "preco": 25.50,
            "estoque": estoque
        },
        headers=auth_headers
    )

    assert response.status_code in [200,201]

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



def criar_item_compra(
    client,
    auth_headers,
    quantidade=2
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
            "carrinho_id": carrinho["id"],
            "produto_id": produto["id"],
            "quantidade": quantidade
        },
        headers=auth_headers
    )


    assert response.status_code in [200,201]


    return carrinho, produto



# =========================================
# FINALIZAR COMPRA
# =========================================


def test_finalizar_compra_sucesso(
    client,
    auth_headers
):

    carrinho, produto = criar_item_compra(
        client,
        auth_headers
    )


    response = client.post(
        f"/carrinhos/{carrinho['id']}/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 200


    dados = response.json()


    assert "mensagem" in dados
    assert "valor_total" in dados
    assert "quantidade_itens" in dados



# =========================================
# CARRINHO VAZIO
# =========================================


def test_finalizar_compra_carrinho_vazio(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    response = client.post(
        f"/carrinhos/{carrinho['id']}/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 400



# =========================================
# CARRINHO INEXISTENTE
# =========================================


def test_finalizar_compra_carrinho_inexistente(client, auth_headers):

    response = client.post(
        "/carrinhos/999/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Carrinho não encontrado"
    )



# =========================================
# ESTOQUE INSUFICIENTE
# =========================================


def test_finalizar_compra_sem_estoque(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    produto = criar_produto(
        client,
        auth_headers,
        estoque=1
    )


    response = client.post(
        "/itens-carrinho/",
        json={
            "carrinho_id": carrinho["id"],
            "produto_id": produto["id"],
            "quantidade":5
        },
        headers=auth_headers
    )


    assert response.status_code == 400



# =========================================
# CONFERIR BAIXA DO ESTOQUE
# =========================================


def test_finalizar_compra_baixa_estoque(
    client,
    auth_headers
):

    carrinho, produto = criar_item_compra(
        client,
        auth_headers
    )


    response = client.post(
        f"/carrinhos/{carrinho['id']}/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 200


    produto_atualizado = client.get(
        f"/produtos/{produto['id']}",
        headers=auth_headers
    )


    assert produto_atualizado.status_code == 200


    estoque = produto_atualizado.json()["estoque"]


    assert estoque == 8