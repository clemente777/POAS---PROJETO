def test_dashboard_banco_vazio(
    client,
    auth_headers
):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["usuarios"] >= 1
    assert dados["clientes"] == 0
    assert dados["animais"] == 0
    assert dados["produtos"] == 0



def test_dashboard_com_dados(
    client,
    auth_headers
):

    cliente = client.post(
        "/clientes/",
        json={
            "nome":"Carlos",
            "cpf":"12345678909",
            "telefone":"84999999999",
            "email":"carlos@email.com",
            "endereco":"Rua A"
        },
        headers=auth_headers
    )


    assert cliente.status_code == 201


    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )


    assert response.status_code == 200


    dados = response.json()


    assert dados["clientes"] == 1



def test_dashboard_retorna_inteiros(
    client,
    auth_headers
):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )


    dados = response.json()


    for valor in dados.values():

        assert isinstance(
            valor,
            int
        )