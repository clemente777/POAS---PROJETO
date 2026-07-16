# tests/test_animal.py


CLIENTE = {
    "nome": "João Silva",
    "cpf": "52998224725",
    "telefone": "84999999999",
    "email": "joao@email.com",
    "endereco": "Rua Principal"
}


ANIMAL = {
    "nome": "Rex",
    "especie": "Cachorro",
    "raca": "Labrador",
    "idade": 5
}



# =====================================================
# AUXILIAR
# =====================================================

def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )

    assert response.status_code in [200, 201]

    return response.json()["id"]




def criar_animal(client, auth_headers):

    cliente_id = criar_cliente(
        client,
        auth_headers
    )


    dados = ANIMAL.copy()

    dados["cliente_id"] = cliente_id



    response = client.post(
        "/animais/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code in [200, 201]


    return response.json()





# =====================================================
# CRIAR
# =====================================================

def test_criar_animal(client, auth_headers):

    animal = criar_animal(
        client,
        auth_headers
    )


    assert animal["nome"] == "Rex"

    assert animal["especie"] == "Cachorro"





# =====================================================
# LISTAR
# =====================================================

def test_listar_animais(client, auth_headers):


    criar_animal(
        client,
        auth_headers
    )


    response = client.get(
        "/animais/",
        headers=auth_headers
    )


    assert response.status_code == 200


    animais = response.json()


    assert len(animais) == 1





# =====================================================
# BUSCAR POR ID
# =====================================================

def test_buscar_animal(client, auth_headers):


    animal = criar_animal(
        client,
        auth_headers
    )


    animal_id = animal["id"]



    response = client.get(
        f"/animais/{animal_id}",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert response.json()["id"] == animal_id





# =====================================================
# ATUALIZAR
# =====================================================
def test_atualizar_animal(client, auth_headers):

    animal = criar_animal(
        client,
        auth_headers
    )


    animal_id = animal["id"]



    response = client.put(
        f"/animais/{animal_id}",
        json={
            "nome": "Rex atualizado",
            "idade": 6
        },
        headers=auth_headers
    )


    assert response.status_code == 200


    dados = response.json()


    assert dados["nome"].lower() == "rex atualizado"





# =====================================================
# DELETAR
# =====================================================

def test_deletar_animal(client, auth_headers):


    animal = criar_animal(
        client,
        auth_headers
    )


    animal_id = animal["id"]



    response = client.delete(
        f"/animais/{animal_id}",
        headers=auth_headers
    )


    assert response.status_code in [
        200,
        204
    ]





# =====================================================
# REGRA - CLIENTE INEXISTENTE
# =====================================================

def test_animal_cliente_inexistente(client, auth_headers):


    dados = ANIMAL.copy()

    dados["cliente_id"] = 999999



    response = client.post(
        "/animais/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code in [
        400,
        404
    ]





# =====================================================
# REGRA - NOME VAZIO
# =====================================================

def test_animal_nome_vazio(client, auth_headers):


    cliente_id = criar_cliente(
        client,
        auth_headers
    )


    dados = ANIMAL.copy()

    dados["cliente_id"] = cliente_id

    dados["nome"] = ""



    response = client.post(
        "/animais/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code == 400