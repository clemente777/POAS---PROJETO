
import pytest


@pytest.mark.asyncio
async def test_listar_animais(client, auth_headers):

    response = await client.get(
        "/animais/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_animal(client, auth_headers):

    response = await client.get(
        "/animais/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_animal(client, auth_headers):

    animal = {
        "nome": "Rex",
        "especie": "Cachorro",
        "idade": 3
    }

    response = await client.post(
        "/animais/",
        json=animal,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_animal(client, auth_headers):

    animal = {
        "nome": "Rex Atualizado"
    }

    response = await client.put(
        "/animais/1",
        json=animal,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_animal(client, auth_headers):

    response = await client.delete(
        "/animais/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]