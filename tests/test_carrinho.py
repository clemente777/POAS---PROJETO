def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json={
            "nome": "João Silva",
            "cpf": "52998224725",
            "telefone": "84999999999",
            "email": "joao@email.com",
            "endereco": "Rua A"
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


    assert response.status_code in [200, 201]

    return response.json()



# ============================
# CREATE
# ============================


def test_criar_carrinho(client, auth_headers):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    assert carrinho["cliente_id"] > 0



# ============================
# LISTAR
# ============================


def test_listar_carrinhos(client, auth_headers):

    criar_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        "/carrinhos/",
        headers=auth_headers
    )


    assert response.status_code == 200

    dados = response.json()

    assert len(dados) == 1



# ============================
# BUSCAR
# ============================


def test_buscar_carrinho(client, auth_headers):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        f"/carrinhos/{carrinho['id']}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert (
        response.json()["id"]
        ==
        carrinho["id"]
    )



# ============================
# ATUALIZAR
# ============================


def test_atualizar_carrinho(client, auth_headers):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    response = client.put(
        f"/carrinhos/{carrinho['id']}",
        json={
            "cliente_id": carrinho["cliente_id"]
        },
        headers=auth_headers
    )


    assert response.status_code == 200



# ============================
# DELETE
# ============================


def test_deletar_carrinho(client, auth_headers):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    response = client.delete(
        f"/carrinhos/{carrinho['id']}",
        headers=auth_headers
    )


    assert response.status_code in [
        200,
        204
    ]



# ============================
# REGRAS DE NEGÓCIO
# ============================


def test_criar_carrinho_cliente_inexistente(
    client,
    auth_headers
):

    response = client.post(
        "/carrinhos/",
        json={
            "cliente_id":9999
        },
        headers=auth_headers
    )


    assert response.status_code == 404



def test_carrinho_sem_cliente(
    client,
    auth_headers
):

    response = client.post(
        "/carrinhos/",
        json={},
        headers=auth_headers
    )


    # erro do Pydantic
    assert response.status_code == 422



def test_carrinho_cliente_duplicado(
    client,
    auth_headers
):

    cliente = criar_cliente(
        client,
        auth_headers
    )


    client.post(
        "/carrinhos/",
        json={
            "cliente_id":cliente["id"]
        },
        headers=auth_headers
    )


    response = client.post(
        "/carrinhos/",
        json={
            "cliente_id":cliente["id"]
        },
        headers=auth_headers
    )


    assert response.status_code in [
        400,
        409
    ]