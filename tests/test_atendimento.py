# tests/test_atendimento.py


# =====================================================
# DADOS
# =====================================================


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



ATENDIMENTO = {
    "diagnostico": "Gripe canina",
    "observacoes": "Animal medicado"
}





# =====================================================
# AUXILIARES
# =====================================================


def criar_cliente(client, auth_headers):

    response = client.post(
        "/clientes/",
        json=CLIENTE,
        headers=auth_headers
    )


    assert response.status_code in [200,201]


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


    assert response.status_code in [200,201]


    return response.json()["id"]






def criar_atendimento(client, auth_headers):


    animal_id = criar_animal(
        client,
        auth_headers
    )


    dados = ATENDIMENTO.copy()


    dados["animal_id"] = animal_id


    dados["usuario_id"] = 1



    response = client.post(
        "/atendimentos/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code in [200,201]


    return response.json()





# =====================================================
# CRIAR
# =====================================================


def test_criar_atendimento(client, auth_headers):


    atendimento = criar_atendimento(
        client,
        auth_headers
    )


    assert (
        atendimento["diagnostico"]
        ==
        "Gripe canina"
    )





# =====================================================
# LISTAR
# =====================================================


def test_listar_atendimentos(client, auth_headers):


    criar_atendimento(
        client,
        auth_headers
    )



    response = client.get(
        "/atendimentos/",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert len(response.json()) == 1





# =====================================================
# BUSCAR
# =====================================================


def test_buscar_atendimento(client, auth_headers):


    atendimento = criar_atendimento(
        client,
        auth_headers
    )


    atendimento_id = atendimento["id"]



    response = client.get(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers
    )


    assert response.status_code == 200


    assert (
        response.json()["id"]
        ==
        atendimento_id
    )





# =====================================================
# ATUALIZAR
# =====================================================


def test_atualizar_atendimento(client, auth_headers):


    atendimento = criar_atendimento(
        client,
        auth_headers
    )


    atendimento_id = atendimento["id"]



    response = client.put(
        f"/atendimentos/{atendimento_id}",
        json={
            "diagnostico":
                "Diagnostico atualizado"
        },
        headers=auth_headers
    )


    assert response.status_code == 200


    assert (
        response.json()["diagnostico"]
        ==
        "Diagnostico atualizado"
    )





# =====================================================
# DELETAR
# =====================================================

def test_deletar_atendimento_bloqueado(
    client,
    auth_headers
):

    # criar cliente
    cliente = client.post(
        "/clientes/",
        json={
            "nome": "João Silva",
            "cpf": "52998224725",
            "telefone": "84999999999",
            "email": "joao@email.com",
            "endereco": "Rua A"
        },
        headers=auth_headers
    )

    cliente_id = cliente.json()["id"]


    # criar animal
    animal = client.post(
        "/animais/",
        json={
            "nome": "Rex",
            "especie": "Cachorro",
            "raca": "Pastor Alemão",
            "idade": 5,
            "cliente_id": cliente_id
        },
        headers=auth_headers
    )

    animal_id = animal.json()["id"]


    # criar atendimento
    atendimento = client.post(
        "/atendimentos/",
        json={
            "diagnostico": "Infecção",
            "observacoes": "Tratamento iniciado",
            "animal_id": animal_id,
            "usuario_id": 1
        },
        headers=auth_headers
    )


    atendimento_id = atendimento.json()["id"]


    # tentar deletar

    response = client.delete(
        f"/atendimentos/{atendimento_id}",
        headers=auth_headers
    )


    assert response.status_code == 409


    assert response.json()["detail"] == (
        "Atendimentos não podem ser excluídos. "
        "O histórico deve ser preservado."
    )



# =====================================================
# REGRA - ANIMAL INEXISTENTE
# =====================================================


def test_atendimento_animal_inexistente(client, auth_headers):


    dados = {

        "diagnostico":
            "Teste",

        "observacoes":
            "Teste",

        "animal_id":
            999999,

        "usuario_id":
            1
    }



    response = client.post(
        "/atendimentos/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code in [
        400,
        404
    ]





# =====================================================
# REGRA - DIAGNOSTICO VAZIO
# =====================================================


def test_atendimento_diagnostico_vazio(client, auth_headers):


    animal_id = criar_animal(
        client,
        auth_headers
    )


    dados = {

        "diagnostico":
            "",

        "observacoes":
            "teste",

        "animal_id":
            animal_id,

        "usuario_id":
            1
    }



    response = client.post(
        "/atendimentos/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code == 400