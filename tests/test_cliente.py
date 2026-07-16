import pytest


# =====================================================
# DADOS DE TESTE
# =====================================================

CLIENTE = {
    "nome": "João Silva",
    "cpf": "52998224725",
    "telefone": "84999999999",
    "email": "joao@email.com",
    "endereco": "Rua Principal"
}


# =====================================================
# CRIAR CLIENTE
# =====================================================

def test_criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    assert response.status_code == 201


    dados = response.json()


    assert dados["nome"] == CLIENTE["nome"]
    assert dados["cpf"] == CLIENTE["cpf"]
    assert dados["email"] == CLIENTE["email"]



# =====================================================
# REGRA - CPF INVÁLIDO
# =====================================================

def test_cliente_cpf_invalido(client, auth_headers):

    dados = CLIENTE.copy()

    dados["cpf"] = "12345678900"


    response = client.post(
        "/clientes/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "CPF inválido."
    )



# =====================================================
# REGRA - NOME OBRIGATÓRIO
# =====================================================

def test_cliente_nome_vazio(client, auth_headers):

    dados = CLIENTE.copy()

    dados["nome"] = ""


    response = client.post(
        "/clientes/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code == 400



# =====================================================
# REGRA - CPF DUPLICADO
# =====================================================

def test_cliente_cpf_duplicado(client, auth_headers):


    client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    response = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    assert response.status_code == 409


    assert (
        response.json()["detail"]
        ==
        "CPF já cadastrado."
    )



# =====================================================
# REGRA - EMAIL DUPLICADO
# =====================================================

def test_cliente_email_duplicado(client, auth_headers):


    client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    novo = CLIENTE.copy()

    novo["cpf"] = "11144477735"



    response = client.post(
        "/clientes/",
        json=novo,
        headers=auth_headers
    )


    assert response.status_code == 409


    assert (
        response.json()["detail"]
        ==
        "Email já cadastrado."
    )



# =====================================================
# LISTAR CLIENTES
# =====================================================

def test_listar_clientes(client, auth_headers):


    client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    response = client.get(
        "/clientes/",
        headers=auth_headers
    )


    assert response.status_code == 200


    dados = response.json()


    assert len(dados) == 1



# =====================================================
# BUSCAR CLIENTE POR ID
# =====================================================

def test_buscar_cliente(client, auth_headers):


    criar = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    cliente_id = criar.json()["id"]



    response = client.get(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert (
        response.json()["id"]
        ==
        cliente_id
    )



# =====================================================
# ATUALIZAR CLIENTE
# =====================================================

def test_atualizar_cliente(client, auth_headers):


    criar = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    cliente_id = criar.json()["id"]



    response = client.put(
        f"/clientes/{cliente_id}",
        json={
            "nome": "João Atualizado"
        },
        headers=auth_headers
    )


    assert response.status_code == 200


    assert (
        response.json()["nome"]
        ==
        "João Atualizado"
    )



# =====================================================
# DELETAR CLIENTE
# =====================================================

def test_deletar_cliente(client, auth_headers):


    criar = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    cliente_id = criar.json()["id"]



    response = client.delete(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]



# =====================================================
# BUSCA POR FILTRO
# =====================================================

def test_filtrar_cliente_nome(client, auth_headers):


    client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    response = client.get(
        "/clientes/?nome=João",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert len(response.json()) == 1



# =====================================================
# PAGINAÇÃO
# =====================================================

def test_paginacao_clientes(client, auth_headers):


    client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    response = client.get(
        "/clientes/?skip=0&limit=1",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert len(response.json()) == 1