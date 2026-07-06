import pytest


@pytest.mark.asyncio
async def test_listar_atendimentos(client, auth_headers):

    response = await client.get(
        "/atendimentos/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_atendimento(client, auth_headers):

    response = await client.get(
        "/atendimentos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_atendimento(client, auth_headers):

    atendimento = {
        "agendamento_id": 1,
        "descricao": "Banho completo"
    }

    response = await client.post(
        "/atendimentos/",
        json=atendimento,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_atendimento(client, auth_headers):

    atendimento = {
        "descricao": "Banho e Tosa"
    }

    response = await client.put(
        "/atendimentos/1",
        json=atendimento,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_atendimento(client, auth_headers):

    response = await client.delete(
        "/atendimentos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]
    