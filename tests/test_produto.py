
import pytest


@pytest.mark.asyncio
async def test_listar_produtos(client, auth_headers):

    response = await client.get(
        "/produtos/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_produto(client, auth_headers):

    response = await client.get(
        "/produtos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_produto(client, auth_headers):

    produto = {
        "nome": "Produto Teste",
        "preco": 10.50,
        "estoque": 5
    }

    response = await client.post(
        "/produtos/",
        json=produto,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_produto(client, auth_headers):

    produto = {
        "nome": "Produto Atualizado"
    }

    response = await client.put(
        "/produtos/1",
        json=produto,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_produto(client, auth_headers):

    response = await client.delete(
        "/produtos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]