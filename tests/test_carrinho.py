# tests/test_carrinho.py


CLIENTE = {
    "nome": "João Silva",
    "cpf": "52998224725",
    "telefone": "84999999999",
    "email": "joao@email.com",
    "endereco": "Rua A"
}



def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    assert response.status_code in [
        200,
        201
    ]


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


    assert response.status_code in [
        200,
        201
    ]


    return response.json()



# ==========================================
# CRIAR
# ==========================================

def test_criar_carrinho(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    assert carrinho["cliente_id"] > 0



# ==========================================
# LISTAR
# ==========================================

def test_listar_carrinhos(
    client,
    auth_headers
):

    criar_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        "/carrinhos/",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert len(response.json()) == 1



# ==========================================
# BUSCAR
# ==========================================

def test_buscar_carrinho(
    client,
    auth_headers
):

    carrinho = criar_carrinho(
        client,
        auth_headers
    )


    response = client.get(
        f"/carrinhos/{carrinho['id']}",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert response.json()["id"] == carrinho["id"]



# ==========================================
# ATUALIZAR
# ==========================================

def test_atualizar_carrinho(
    client,
    auth_headers
):

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



# ==========================================
# DELETAR
# ==========================================

def test_deletar_carrinho(
    client,
    auth_headers
):

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



# ==========================================
# REGRA - CLIENTE INEXISTENTE
# ==========================================

def test_carrinho_cliente_inexistente(
    client,
    auth_headers
):

    response = client.post(
        "/carrinhos/",
        json={
            "cliente_id":99999
        },
        headers=auth_headers
    )


    assert response.status_code == 404



# ==========================================
# REGRA - SEM CLIENTE
# ==========================================

def test_carrinho_sem_cliente(
    client,
    auth_headers
):

    response = client.post(
        "/carrinhos/",
        json={},
        headers=auth_headers
    )


    assert response.status_code == 422



# ==========================================
# REGRA - CLIENTE COM DOIS CARRINHOS
# ==========================================

def test_carrinho_cliente_duplicado(
    client,
    auth_headers
):

    cliente = criar_cliente(
        client,
        auth_headers
    )


    primeiro = client.post(
        "/carrinhos/",
        json={
            "cliente_id": cliente["id"]
        },
        headers=auth_headers
    )


    assert primeiro.status_code in [
        200,
        201
    ]



    segundo = client.post(
        "/carrinhos/",
        json={
            "cliente_id": cliente["id"]
        },
        headers=auth_headers
    )


    assert segundo.status_code in [
        400,
        409
    ]