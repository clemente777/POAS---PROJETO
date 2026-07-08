def criar_cliente(client, auth_headers, email):

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

    assert response.status_code in [200,201], response.json()

    return response.json()["id"]
    
def test_criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "João Silva",
            "cpf": "12345678901",
            "telefone": "84999999999",
            "email": "joao@email.com",
            "endereco": "Rua A, 100"
        }
    )


    assert response.status_code in [200,201]

    assert response.json()["nome"] == "João Silva"



def test_listar_clientes(client, auth_headers):

    response = client.get(
        "/clientes/",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert isinstance(response.json(), list)



def test_buscar_cliente(client, auth_headers):

    criar = client.post(
        "/clientes/",
        headers=auth_headers,
       json={
            "nome": "Maria",
            "cpf": "11111111111",
            "telefone": "888888888",
            "email": "maria@email.com",
            "endereco": "Rua B"
       }
    )


    cliente_id = criar.json()["id"]


    response = client.get(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )


    assert response.status_code == 200

    assert response.json()["id"] == cliente_id



def test_atualizar_cliente(client, auth_headers):

    criar = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Excluir",
            "cpf": "33333333333",
            "telefone": "99999",
            "email": "excluir@email.com",
            "endereco": "Rua D"
        }
    )


    cliente_id = criar.json()["id"]


    response = client.put(
        f"/clientes/{cliente_id}",
        headers=auth_headers,
        json={
            "nome":"Cliente Alterado"
        }
    )


    assert response.status_code == 200




def test_deletar_cliente(client, auth_headers):

    criar = client.post(
        "/clientes/",
        headers=auth_headers,
        json={
            "nome": "Cliente Delete",
            "cpf": "55555555555",
            "telefone": "999999999",
            "email": "deletecliente@email.com",
            "endereco": "Rua Teste"
        }
    )

    print("CLIENTE DELETE:", criar.status_code)
    print("CLIENTE JSON:", criar.json())

    assert criar.status_code in [200, 201], criar.json()

    cliente_id = criar.json()["id"]


    response = client.delete(
        f"/clientes/{cliente_id}",
        headers=auth_headers
    )


    assert response.status_code in [200, 204]