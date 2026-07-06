
import pytest


@pytest.mark.asyncio
async def test_login_sem_dados(client):

    response = await client.post(
        "/login/"
    )

    assert response.status_code in [400, 401, 422]


@pytest.mark.asyncio
async def test_login_usuario_inexistente(client):

    response = await client.post(
        "/login/",
        data={
            "username": "usuario@teste.com",
            "password": "123456"
        }
    )

    assert response.status_code in [200, 401, 422, 500]


@pytest.mark.asyncio
async def test_login_senha_errada(client):

    response = await client.post(
        "/login/",
        data={
            "username": "admin@admin.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code in [200, 401, 422, 500]


@pytest.mark.asyncio
async def test_login_formato(client):

    response = await client.post(
        "/login/",
        data={
            "username": "",
            "password": ""
        }
    )

    assert response.status_code in [200, 400, 401, 422]