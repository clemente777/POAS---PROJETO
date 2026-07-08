def criar_animal_para_teste(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Atendimento",
            "telefone": "999999",
            "email": "atendimento@email.com"
        }
    )

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

    return animal.json()["id"]



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
            "descricao": "Consulta de rotina",
            "observacao": "Animal saudável"
        }
    )


    assert response.status_code in [200,201]



def test_listar_atendimentos(client, auth_headers):

    response = client.get(
        "/atendimentos/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_atendimento(client, auth_headers):

    animal_id = criar_animal_para_teste(
        client,
        auth_headers
    )


    criar = client.post(
        "/atendimentos/",
        headers=auth_headers,
        json={
            "animal_id": animal_id,
            "descricao":"Vacinação"
        }
    )


    atendimento_id = criar.json()["id"]


    response = client.get(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_atualizar_atendimento(client, auth_headers):

    animal_id = criar_animal_para_teste(
        client,
        auth_headers
    )


    criar = client.post(
        "/atendimentos/",
        headers=auth_headers,
        json={
            "animal_id":animal_id,
            "descricao":"Antigo"
        }
    )


    atendimento_id = criar.json()["id"]


    response = client.put(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers,
        json={
            "descricao":"Atualizado"
        }
    )


    assert response.status_code == 200



def test_deletar_atendimento(client, auth_headers):

    animal_id = criar_animal_para_teste(
        client,
        auth_headers
    )


    criar = client.post(
        "/atendimentos/",
        headers=auth_headers,
        json={
            "animal_id":animal_id,
            "descricao":"Excluir"
        }
    )


    atendimento_id = criar.json()["id"]


    response = client.delete(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers
    )


    assert response.status_code in [200,204]