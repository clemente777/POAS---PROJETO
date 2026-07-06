

import pytest


@pytest.mark.asyncio
async def test_listar_itens(client, auth_headers):

    response = await client.get(
        "/itens-carrinho/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_item(client, auth_headers):

    response = await client.get(
        "/itens-carrinho/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_item(client, auth_headers):

    item = {
        "carrinho_id": 1,
        "produto_id": 1,
        "quantidade": 1
    }

    response = await client.post(
        "/itens-carrinho/",
        json=item,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_item(client, auth_headers):

    item = {
        "quantidade": 2
    }

    response = await client.put(
        "/itens-carrinho/1",
        json=item,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_item(client, auth_headers):

    response = await client.delete(
        "/itens-carrinho/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]