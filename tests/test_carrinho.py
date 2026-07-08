def test_criar_carrinho(client, auth_headers):

    response = client.post(
        "/carrinhos/",
        headers=auth_headers,
        json={}
    )


    assert response.status_code in [200,201]



def test_listar_carrinhos(client, auth_headers):

    response = client.get(
        "/carrinhos/",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_buscar_carrinho(client, auth_headers):

    criar = client.post(
        "/carrinhos/",
        headers=auth_headers,
        json={}
    )


    carrinho_id = criar.json()["id"]


    response = client.get(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_atualizar_carrinho(client, auth_headers):

    criar = client.post(
        "/carrinhos/",
        headers=auth_headers,
        json={}
    )


    carrinho_id = criar.json()["id"]


    response = client.put(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers,
        json={}
    )


    assert response.status_code == 200



def test_deletar_carrinho(client, auth_headers):

    criar = client.post(
        "/carrinhos/",
        headers=auth_headers,
        json={}
    )


    carrinho_id = criar.json()["id"]


    response = client.delete(
        f"/carrinhos/{carrinho_id}",
        headers=auth_headers
    )


    assert response.status_code in [200,204]