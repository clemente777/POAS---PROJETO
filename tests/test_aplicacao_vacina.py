from datetime import datetime

from backend.models.animal_model import Animais
from backend.models.vacina_model import Vacinas



def criar_animal(session, criar_cliente):

    animal = Animais(

        nome="Rex",

        especie="Cachorro",

        raca="Golden Retriever",

        idade=3,

        cliente_id=criar_cliente.id

    )


    session.add(animal)

    session.commit()

    session.refresh(animal)


    return animal




def criar_vacina(session):

    vacina = Vacinas(

        nome="V10",

        fabricante="Zoetis",

        quantidade_doses=3,

        intervalo_dias=30,

        descricao="Vacina múltipla para cães"

    )


    session.add(vacina)

    session.commit()

    session.refresh(vacina)


    return vacina





# ==================================================
# TESTE APLICAR VACINA
# ==================================================

def test_aplicar_vacina(

    client,

    session,

    veterinario_headers,

    criar_cliente

):


    animal = criar_animal(

        session,

        criar_cliente

    )


    vacina = criar_vacina(

        session

    )



    resposta = client.post(

        "/aplicacoes-vacina/",

        headers=veterinario_headers,

        json={

            "animal_id": animal.id,

            "vacina_id": vacina.id,

            "lote": "LOTE123",

            "observacoes": "Primeira dose"

        }

    )



    print(resposta.json())


    assert resposta.status_code == 200


    dados = resposta.json()



    assert dados["animal_id"] == animal.id

    assert dados["vacina_id"] == vacina.id

    assert dados["lote"] == "LOTE123"

    assert dados["observacoes"] == "Primeira dose"





# ==================================================
# TESTE LISTAR APLICAÇÕES
# ==================================================

def test_listar_aplicacoes_vacina(

    client,

    session,

    veterinario_headers,

    criar_cliente

):


    animal = criar_animal(

        session,

        criar_cliente

    )


    vacina = criar_vacina(

        session

    )



    client.post(

        "/aplicacoes-vacina/",

        headers=veterinario_headers,

        json={

            "animal_id": animal.id,

            "vacina_id": vacina.id,

            "lote": "ABC"

        }

    )



    resposta = client.get(

        "/aplicacoes-vacina/",

        headers=veterinario_headers

    )



    assert resposta.status_code == 200


    dados = resposta.json()



    assert len(dados) == 1





# ==================================================
# TESTE DUPLICIDADE
# ==================================================

def test_nao_permite_aplicar_mesma_vacina_no_mesmo_dia(

    client,

    session,

    veterinario_headers,

    criar_cliente

):


    animal = criar_animal(

        session,

        criar_cliente

    )


    vacina = criar_vacina(

        session

    )


    dados = {

        "animal_id": animal.id,

        "vacina_id": vacina.id,

        "lote": "TESTE"

    }



    primeira = client.post(

        "/aplicacoes-vacina/",

        headers=veterinario_headers,

        json=dados

    )


    assert primeira.status_code == 200




    segunda = client.post(

        "/aplicacoes-vacina/",

        headers=veterinario_headers,

        json=dados

    )



    assert segunda.status_code == 400


    assert (

        segunda.json()["detail"]

        ==

        "Este animal já recebeu esta vacina hoje."

    )





# ==================================================
# TESTE PERMISSÃO ADMIN NÃO APLICA
# ==================================================

def test_admin_nao_aplica_vacina(

    client,

    session,

    admin_headers,

    criar_cliente

):


    animal = criar_animal(

        session,

        criar_cliente

    )


    vacina = criar_vacina(

        session

    )



    resposta = client.post(

        "/aplicacoes-vacina/",

        headers=admin_headers,

        json={

            "animal_id": animal.id,

            "vacina_id": vacina.id

        }

    )



    assert resposta.status_code == 403