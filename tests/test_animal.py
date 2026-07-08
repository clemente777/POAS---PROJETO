def test_criar_animal(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Dono Teste",
            "telefone":"999999999",
            "email":"dono@email.com"
        }
    )

    cliente_id = cliente.json()["id"]


    response = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome":"Rex",
            "especie":"Cachorro",
            "raca":"Pastor Alemão",
            "idade":3,
            "cliente_id":cliente_id
        }
    )


    assert response.status_code in [200,201]

    assert response.json()["nome"] == "Rex"



def test_listar_animais(client, auth_headers):

    response = client.get(
        "/animais/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_animal(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Cliente Animal",
            "telefone":"111111",
            "email":"animal@email.com"
        }
    )

    cliente_id = cliente.json()["id"]


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome":"Bob",
            "especie":"Gato",
            "raca":"Siamês",
            "idade":2,
            "cliente_id":cliente_id
        }
    )


    animal_id = animal.json()["id"]


    response = client.get(
        f"/animais/{animal_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == animal_id



def test_atualizar_animal(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Cliente",
            "telefone":"123",
            "email":"clienteanimal2@email.com"
        }
    )


    cliente_id = cliente.json()["id"]


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome":"Totó",
            "especie":"Cachorro",
            "raca":"Vira-lata",
            "idade":1,
            "cliente_id":cliente_id
        }
    )


    animal_id = animal.json()["id"]


    response = client.put(
        f"/animais/{animal_id}",
        headers=auth_headers,
        json={
            "nome":"Totó Atualizado"
        }
    )


    assert response.status_code == 200

    assert response.json()["nome"] == "Totó Atualizado"



def test_deletar_animal(client, auth_headers):

    cliente = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome":"Cliente Delete",
            "telefone":"555",
            "email":"deleteanimal@email.com"
        }
    )


    cliente_id = cliente.json()["id"]


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome":"Excluir",
            "especie":"Cachorro",
            "raca":"Teste",
            "idade":1,
            "cliente_id":cliente_id
        }
    )


    animal_id = animal.json()["id"]


    response = client.delete(
        f"/animais/{animal_id}",
        headers=auth_headers
    )


    assert response.status_code in [200,204]