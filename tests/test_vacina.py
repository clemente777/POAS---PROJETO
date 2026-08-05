from backend.models.vacina_model import Vacinas
from backend.models.animal_model import Animais
from backend.models.aplicacao_vacina_model import AplicacoesVacina



def criar_vacina(client, headers):

    response = client.post(

        "/vacinas/",

        headers=headers,

        json={

            "nome": "V10",

            "fabricante": "Zoetis",

            "quantidade_doses": 3,

            "intervalo_dias": 30,

            "descricao": "Vacina para cães"

        }

    )

    return response





def test_admin_cadastra_vacina(
    client,
    admin_headers
):

    response = criar_vacina(

        client,

        admin_headers

    )


    assert response.status_code == 200


    data = response.json()


    assert data["nome"] == "V10"





def test_veterinario_lista_vacinas(
    client,
    veterinario_headers
):


    response = client.get(

        "/vacinas/",

        headers=veterinario_headers

    )


    assert response.status_code == 200


    assert isinstance(

        response.json(),

        list

    )





def test_cliente_nao_lista_vacinas(
    client,
    cliente_headers
):


    response = client.get(

        "/vacinas/",

        headers=cliente_headers

    )


    assert response.status_code == 403





def test_admin_busca_vacina_por_id(
    client,
    admin_headers
):


    criar = criar_vacina(

        client,

        admin_headers

    )


    vacina_id = criar.json()["id"]



    response = client.get(

        f"/vacinas/{vacina_id}",

        headers=admin_headers

    )


    assert response.status_code == 200


    assert response.json()["id"] == vacina_id





def test_admin_atualiza_vacina(
    client,
    admin_headers
):


    criar = criar_vacina(

        client,

        admin_headers

    )


    vacina_id = criar.json()["id"]



    response = client.put(

        f"/vacinas/{vacina_id}",

        headers=admin_headers,

        json={

            "fabricante": "MSD",

            "descricao": "Atualizada"

        }

    )


    assert response.status_code == 200


    assert response.json()["fabricante"] == "MSD"





def test_admin_deleta_vacina(
    client,
    admin_headers
):


    criar = criar_vacina(

        client,

        admin_headers

    )


    vacina_id = criar.json()["id"]



    response = client.delete(

        f"/vacinas/{vacina_id}",

        headers=admin_headers

    )


    assert response.status_code == 200





def test_nao_permite_vacina_duplicada(
    client,
    admin_headers
):


    criar_vacina(

        client,

        admin_headers

    )


    response = criar_vacina(

        client,

        admin_headers

    )


    assert response.status_code == 400