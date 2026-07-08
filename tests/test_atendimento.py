def criar_animal_para_teste(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Atendimento",
            "cpf": "22222222222",
            "telefone": "999999",
            "email": "atendimento@email.com",
            "endereco": "Rua Teste"
        }
    )

    print("CLIENTE:", cliente.status_code)
    print("CLIENTE JSON:", cliente.json())

    assert cliente.status_code in [200, 201], cliente.json()

    cliente_id = cliente.json()["id"]


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Rex Atendimento",
            "especie": "Cachorro",
            "raca": "Golden",
            "idade": 4,
            "cliente_id": cliente_id
        }
    )

    print("ANIMAL:", animal.status_code)
    print("ANIMAL JSON:", animal.json())

    assert animal.status_code in [200, 201], animal.json()

    return animal.json()["id"]



def criar_atendimento(client, auth_headers):

    animal_id = criar_animal_para_teste(
        client,
        auth_headers
    )


    response = client.post(
        "/atendimentos/",
        headers=auth_headers,
        json={
            "animal_id": animal_id,
            "diagnostico": "Animal saudável",
            "observacoes": "Consulta de rotina",
            "usuario_id": 1
        }
    )


    assert response.status_code in [200, 201]

    return response.json()["id"]



def test_criar_atendimento(client, auth_headers):

    animal_id = criar_animal_para_teste(
        client,
        auth_headers
    )


    response = client.post(
        "/atendimentos/",
        headers=auth_headers,
        json={
            "animal_id": animal_id,
            "diagnostico": "Gripe canina",
            "observacoes": "Animal saudável",
            "usuario_id": 1
        }
    )


    assert response.status_code in [200, 201]

    data = response.json()

    assert data["animal_id"] == animal_id



def test_listar_atendimentos(client, auth_headers):

    response = client.get(
        "/atendimentos/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_atendimento(client, auth_headers):

    atendimento_id = criar_atendimento(
        client,
        auth_headers
    )


    response = client.get(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == atendimento_id



def test_atualizar_atendimento(client, auth_headers):

    atendimento_id = criar_atendimento(
        client,
        auth_headers
    )


    response = client.put(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers,
        json={
            "diagnostico": "Diagnóstico atualizado",
            "observacoes": "Nova observação"
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["diagnostico"] == "Diagnóstico atualizado"



def test_deletar_atendimento(client, auth_headers):

    atendimento_id = criar_atendimento(
        client,
        auth_headers
    )


    response = client.delete(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]