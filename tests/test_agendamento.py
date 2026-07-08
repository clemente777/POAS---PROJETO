def criar_cliente_animal(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Cliente Agenda",
            "telefone":"999",
            "email":"agenda@email.com"
        }
    )

    cliente_id = cliente.json()["id"]


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome":"Animal Agenda",
            "especie":"Cachorro",
            "raca":"Labrador",
            "idade":2,
            "cliente_id":cliente_id
        }
    )


    return animal.json()["id"]



def test_criar_agendamento(client, auth_headers):

    animal_id = criar_cliente_animal(
        client,
        auth_headers
    )


    response = client.post(
        "/agendamentos/",
        headers=auth_headers,
        json={
            "animal_id":animal_id,
            "data":"2026-07-10T10:00:00",
            "tipo":"Consulta"
        }
    )


    assert response.status_code in [200,201]



def test_listar_agendamentos(client, auth_headers):

    response = client.get(
        "/agendamentos/",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_buscar_agendamento(client, auth_headers):

    animal_id = criar_cliente_animal(
        client,
        auth_headers
    )


    criar = client.post(
        "/agendamentos/",
        headers=auth_headers,
        json={
            "animal_id":animal_id,
            "data":"2026-07-10T10:00:00",
            "tipo":"Banho"
        }
    )


    id_agendamento = criar.json()["id"]


    response = client.get(
        f"/agendamentos/{id_agendamento}",
        headers=auth_headers
    )


    assert response.status_code == 200