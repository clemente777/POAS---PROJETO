# tests/test_agendamento.py


from datetime import datetime, timedelta
from urllib import response

from datetime import datetime, timedelta


from datetime import datetime, timedelta


from datetime import datetime, timedelta



from datetime import datetime, timedelta


def agendamento_json(animal_id):

    return {

        "data_agendamento": (
            datetime.now()
            + timedelta(days=5)
        ).isoformat(),

        "descricao": "Consulta veterinaria",

        "animal_id": animal_id

    }

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
# AUXILIARES
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


    return response.json()["id"]




def criar_agendamento(client, auth_headers):


    animal_id = criar_animal(
        client,
        auth_headers
    )



    dados = {

        "data_agendamento":
            (
                datetime.now()
                +
                timedelta(days=1)
            )
            .isoformat(),

        "descricao":
            "Consulta de rotina",

        "animal_id":
            animal_id
    }



    response = client.post(
        "/agendamentos/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code in [200,201]


    return response.json()





# =====================================================
# CRIAR AGENDAMENTO
# =====================================================


def test_deletar_agendamento(client, auth_headers, criar_cliente):


    cliente = criar_cliente


    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Rex",
            "idade": 5,
            "raca": "Labrador",
            "especie": "Cachorro",
            "cliente_id": cliente.id
        }
    )


    print(animal.json())


    assert animal.status_code == 201


    animal_id = animal.json()["id"]



    # criar agendamento

    criar = client.post(
        "/agendamentos/",
        headers=auth_headers,
        json=agendamento_json(animal_id)
    )


    assert criar.status_code == 201



    id_agendamento = criar.json()["id"]



    # tentar deletar

    response = client.delete(
        f"/agendamentos/{id_agendamento}",
        headers=auth_headers
    )


    assert response.status_code == 409

# =====================================================
# ATUALIZAR
# =====================================================


def test_atualizar_agendamento(client, auth_headers):


    agendamento = criar_agendamento(
        client,
        auth_headers
    )


    agendamento_id = agendamento["id"]



    response = client.put(
        f"/agendamentos/{agendamento_id}",
        json={
            "descricao":
                "Consulta atualizada"
        },
        headers=auth_headers
    )


    assert response.status_code == 200


    assert (
        response.json()["descricao"]
        ==
        "Consulta atualizada"
    )





# =====================================================
# DELETAR
# =====================================================


def test_deletar_agendamento(client, auth_headers):


    # criar animal primeiro
    animal = client.post(
        "/animais/",
        headers=auth_headers,
        json={
            "nome": "Rex",
            "idade": 5,
            "raca": "Labrador",
            "especie_id": 1,
            "cliente_id": 1
        }
    )


    assert animal.status_code == 201


    animal_id = animal.json()["id"]



    # criar agendamento
    criar = client.post(
        "/agendamentos/",
        headers=auth_headers,
        json={

            "data_agendamento":
            "2030-01-10T10:00:00",

            "descricao":
            "Consulta veterinaria",

            "animal_id":
            animal_id

        }
    )


    print(criar.json())


    assert criar.status_code == 201


    id_agendamento = criar.json()["id"]



    # tentar deletar
    response = client.delete(
        f"/agendamentos/{id_agendamento}",
        headers=auth_headers
    )


    assert response.status_code == 409
# =====================================================
# REGRA - ANIMAL INEXISTENTE
# =====================================================


def test_agendamento_animal_inexistente(client, auth_headers):


    dados = {

        "data_agendamento":
            (
                datetime.now()
                +
                timedelta(days=1)
            )
            .isoformat(),

        "descricao":
            "Consulta",

        "animal_id":
            999999
    }



    response = client.post(
        "/agendamentos/",
        json=dados,
        headers=auth_headers
    )


    assert response.status_code in [
        400,
        404
    ]





# =====================================================
# REGRA - DESCRIÇÃO VAZIA
# =====================================================


def test_agendamento_descricao_vazia(client, auth_headers):


    animal_id = criar_animal(
        client,
        auth_headers
    )



    dados = {

        "data_agendamento":
            (
                datetime.now()
                +
                timedelta(days=1)
            )
            .isoformat(),

        "descricao":
            "",

        "animal_id":
            animal_id
    }



    response = client.post(
        "/agendamentos/",
        json=dados,
        headers=auth_headers
    )



    assert response.status_code == 400

