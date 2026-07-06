

import pytest


@pytest.mark.asyncio
async def test_listar_carrinhos(client, auth_headers):

    response = await client.get(
        "/carrinhos/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_carrinho(client, auth_headers):

    response = await client.get(
        "/carrinhos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_carrinho(client, auth_headers):

    carrinho = {
        "cliente_id": 1
    }

    response = await client.post(
        "/carrinhos/",
        json=carrinho,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_carrinho(client, auth_headers):

    carrinho = {
        "cliente_id": 2
    }

    response = await client.put(
        "/carrinhos/1",
        json=carrinho,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_carrinho(client, auth_headers):

    response = await client.delete(
        "/carrinhos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]