def test_dashboard(client, auth_headers):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "usuarios" in data
    assert "clientes" in data
    assert "animais" in data
    assert "agendamentos" in data
    assert "atendimentos" in data
    assert "produtos" in data
    assert "carrinhos" in data
    assert "itens_carrinho" in data


def test_dashboard_sem_token(client):

    response = client.get("/dashboard/")

    assert response.status_code == 401


def test_dashboard_retorna_inteiros(client, auth_headers):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    data = response.json()

    assert isinstance(data["usuarios"], int)
    assert isinstance(data["clientes"], int)
    assert isinstance(data["animais"], int)
    assert isinstance(data["agendamentos"], int)
    assert isinstance(data["atendimentos"], int)
    assert isinstance(data["produtos"], int)
    assert isinstance(data["carrinhos"], int)
    assert isinstance(data["itens_carrinho"], int)


def test_dashboard_banco_vazio(client, auth_headers):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["usuarios"] >= 0
    assert data["clientes"] >= 0
    assert data["animais"] >= 0
    assert data["agendamentos"] >= 0
    assert data["atendimentos"] >= 0
    assert data["produtos"] >= 0
    assert data["carrinhos"] >= 0
    assert data["itens_carrinho"] >= 0

def test_dashboard_com_dados(client, auth_headers, session):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["usuarios"] == 1