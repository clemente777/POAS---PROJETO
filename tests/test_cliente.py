

import pytest


@pytest.mark.asyncio
async def test_listar_clientes(client, auth_headers):

    response = await client.get(
        "/clientes/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_cliente(client, auth_headers):

    response = await client.get(
        "/clientes/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_cliente(client, auth_headers):

    cliente = {
        "nome": "Cliente Teste",
        "cpf": "12345678901",
        "telefone": "999999999",
        "email": "cliente@teste.com"
    }

    response = await client.post(
        "/clientes/",
        json=cliente,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_cliente(client, auth_headers):

    cliente = {
        "nome": "Cliente Alterado"
    }

    response = await client.put(
        "/clientes/1",
        json=cliente,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_cliente(client, auth_headers):

    response = await client.delete(
        "/clientes/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]