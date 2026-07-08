def criar_cliente_animal(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Agenda",
            "cpf": "11111111111",
            "telefone": "999999",
            "email": "agenda@email.com",
            "endereco": "Rua Teste"
        }
    )

    assert cliente.status_code in [200, 201], cliente.json()

    cliente_id = cliente.json()["id"]


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Animal Agenda",
            "especie": "Cachorro",
            "raca": "Labrador",
            "idade": 2,
            "cliente_id": cliente_id
        }
    )

    assert animal.status_code in [200, 201], animal.json()

    return animal.json()["id"]


def criar_agendamento(client, auth_headers):

    animal_id = criar_cliente_animal(
        client,
        auth_headers
    )


    response = client.post(
        "/agendamentos/",
        headers=auth_headers,
        json={
            "animal_id": animal_id,
            "data_agendamento": "2026-07-10T10:00:00",
            "descricao": "Consulta veterinária"
        }
    )


    assert response.status_code in [200, 201]

    return response.json()["id"]



def test_criar_agendamento(client, auth_headers):

    animal_id = criar_cliente_animal(
        client,
        auth_headers
    )


    response = client.post(
        "/agendamentos/",
        headers=auth_headers,
        json={
            "animal_id": animal_id,
            "data_agendamento": "2026-07-10T10:00:00",
            "descricao": "Consulta"
        }
    )


    assert response.status_code in [200, 201]

    data = response.json()

    assert data["animal_id"] == animal_id



def test_listar_agendamentos(client, auth_headers):

    response = client.get(
        "/agendamentos/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_agendamento(client, auth_headers):

    id_agendamento = criar_agendamento(
        client,
        auth_headers
    )


    response = client.get(
        f"/agendamentos/{id_agendamento}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == id_agendamento



def test_atualizar_agendamento(client, auth_headers):

    id_agendamento = criar_agendamento(
        client,
        auth_headers
    )


    response = client.put(
        f"/agendamentos/{id_agendamento}",
        headers=auth_headers,
        json={
            "descricao": "Consulta atualizada",
            "status": "Confirmado"
        }
    )


    assert response.status_code == 200

    assert response.json()["descricao"] == "Consulta atualizada"



def test_deletar_agendamento(client, auth_headers):

    id_agendamento = criar_agendamento(
        client,
        auth_headers
    )


    response = client.delete(
        f"/agendamentos/{id_agendamento}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]