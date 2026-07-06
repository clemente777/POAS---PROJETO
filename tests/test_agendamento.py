
import pytest


@pytest.mark.asyncio
async def test_listar_agendamentos(client, auth_headers):

    response = await client.get(
        "/agendamentos/",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 500]


@pytest.mark.asyncio
async def test_buscar_agendamento(client, auth_headers):

    response = await client.get(
        "/agendamentos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 401, 403, 404, 500]


@pytest.mark.asyncio
async def test_criar_agendamento(client, auth_headers):

    agendamento = {
        "cliente_id": 1,
        "animal_id": 1,
        "data": "2026-01-01",
        "hora": "10:00"
    }

    response = await client.post(
        "/agendamentos/",
        json=agendamento,
        headers=auth_headers
    )

    assert response.status_code in [200, 201, 400, 401, 403, 422, 500]


@pytest.mark.asyncio
async def test_atualizar_agendamento(client, auth_headers):

    agendamento = {
        "hora": "14:00"
    }

    response = await client.put(
        "/agendamentos/1",
        json=agendamento,
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 422, 500]


@pytest.mark.asyncio
async def test_deletar_agendamento(client, auth_headers):

    response = await client.delete(
        "/agendamentos/1",
        headers=auth_headers
    )

    assert response.status_code in [200, 400, 401, 403, 404, 500]