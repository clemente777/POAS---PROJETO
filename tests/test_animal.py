def criar_cliente(client, auth_headers, email="cliente@email.com"):

    response = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Teste",
            "cpf": "11111111111",
            "telefone": "999999999",
            "email": email,
            "endereco": "Rua Teste"
        }
    )

    print("STATUS CLIENTE:", response.status_code)
    print("RESPOSTA CLIENTE:", response.json())

    assert response.status_code in [200, 201]

    return response.json()["id"]

def criar_animal(client, auth_headers):

    cliente_id = criar_cliente(
        client,
        auth_headers,
        "animal@email.com"
    )

    response = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Rex",
            "especie": "Cachorro",
            "raca": "Pastor Alemão",
            "idade": 3,
            "cliente_id": cliente_id
        }
    )

    assert response.status_code in [200, 201]

    return response.json()["id"]


def criar_animal(client, auth_headers):

    cliente_id = criar_cliente(
        client,
        auth_headers,
        "animal@email.com"
    )

    response = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Rex",
            "especie": "Cachorro",
            "raca": "Pastor Alemão",
            "idade": 3,
            "cliente_id": cliente_id
        }
    )

    print("STATUS ANIMAL:", response.status_code)
    print("RESPOSTA ANIMAL:", response.json())

    assert response.status_code in [200, 201]

    return response.json()["id"]
def test_criar_animal(client, auth_headers):

    cliente_id = criar_cliente(
        client,
        auth_headers
    )

    response = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Rex",
            "especie": "Cachorro",
            "raca": "Pastor Alemão",
            "idade": 3,
            "cliente_id": cliente_id
        }
    )


    assert response.status_code in [200, 201]

    data = response.json()

    assert data["nome"] == "Rex"
    assert data["cliente_id"] == cliente_id



def test_listar_animais(client, auth_headers):

    response = client.get(
        "/animais/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_animal(client, auth_headers):

    animal_id = criar_animal(
        client,
        auth_headers
    )


    response = client.get(
        f"/animais/{animal_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == animal_id



def test_atualizar_animal(client, auth_headers):

    animal_id = criar_animal(
        client,
        auth_headers
    )


    response = client.put(
        f"/animais/{animal_id}",
        headers=auth_headers,
        json={
            "nome": "Rex Atualizado"
        }
    )


    assert response.status_code == 200

    assert response.json()["nome"] == "Rex Atualizado"



def test_deletar_animal(client, auth_headers):

    animal_id = criar_animal(
        client,
        auth_headers
    )


    response = client.delete(
        f"/animais/{animal_id}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]