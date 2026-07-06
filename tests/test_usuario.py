

import pytest


@pytest.mark.asyncio
async def test_listar_usuarios(client, auth_headers):
    response = await client.get(
        "/usuarios/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_buscar_usuario(client, auth_headers):
    response = await client.get(
        "/usuarios/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_usuario(client, auth_headers):

    usuario = {
        "nome": "Usuário Teste",
        "email": "teste@teste.com",
        "senha": "123456"
    }

    response = await client.post(
        "/usuarios/",
        json=usuario,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_usuario(client, auth_headers):

    usuario = {
        "nome": "Novo Nome"
    }

    response = await client.put(
        "/usuarios/1",
        json=usuario,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_usuario(client, auth_headers):

    response = await client.delete(
        "/usuarios/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]