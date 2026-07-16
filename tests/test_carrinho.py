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

def criar_produto(client, auth_headers):

    response = client.post(
        "/produtos/",
        headers=auth_headers,
        json={
            "nome": "Ração Premium",
            "descricao": "Ração para cachorro",
            "preco": 50.0,
            "estoque": 10
        }
    )

    assert response.status_code in [200, 201], response.json()

    return response.json()["id"]

def adicionar_item_carrinho(
    client,
    auth_headers,
    carrinho_id,
    produto_id,
    quantidade
):

    response = client.post(
        f"/itens-carrinho/",
        headers=auth_headers,
        json={
            "carrinho_id": carrinho_id,
            "produto_id": produto_id,
            "quantidade": quantidade
        }
    )

    assert response.status_code in [200, 201], response.json()

    return response.json()


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


# Regras do carrinho
def test_finalizar_compra_sucesso(
    client,
    auth_headers
):

    carrinho_id, _ = criar_carrinho(
        client,
        auth_headers
    )


    produto_id = criar_produto(
        client,
        auth_headers
    )


    adicionar_item_carrinho(
        client,
        auth_headers,
        carrinho_id,
        produto_id,
        2
    )


    response = client.post(
        f"/carrinhos/{carrinho_id}/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 200


    data = response.json()


    assert data["mensagem"] == (
        "Compra finalizada com sucesso."
    )

    assert data["quantidade_itens"] == 2


def test_finalizar_compra_carrinho_vazio(
    client,
    auth_headers
):

    carrinho_id, _ = criar_carrinho(
        client,
        auth_headers
    )


    response = client.post(
        f"/carrinhos/{carrinho_id}/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 400


    assert (
        response.json()["detail"]
        ==
        "Carrinho vazio"
    )

def test_finalizar_compra_carrinho_inexistente(
    client,
    auth_headers
):

    response = client.post(
        "/carrinhos/999/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 400


    assert (
        response.json()["detail"]
        ==
        "Carrinho não encontrado"
    )

def test_finalizar_compra_sem_estoque(
    client,
    auth_headers
):

    carrinho_id, _ = criar_carrinho(
        client,
        auth_headers
    )


    produto_id = criar_produto(
        client,
        auth_headers
    )


    adicionar_item_carrinho(
        client,
        auth_headers,
        carrinho_id,
        produto_id,
        20
    )


    response = client.post(
        f"/carrinhos/{carrinho_id}/finalizar",
        headers=auth_headers
    )


    assert response.status_code == 400