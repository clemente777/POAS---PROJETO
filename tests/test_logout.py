def test_logout(
    client,
    auth_headers
):

    response = client.post(
        "/logout/",
        headers=auth_headers
    )


    assert response.status_code == 200



def test_token_revogado(
    client,
    auth_headers
):


    logout = client.post(
        "/logout/",
        headers=auth_headers
    )


    assert logout.status_code == 200



    response = client.get(
        "/clientes/",
        headers=auth_headers
    )


    assert response.status_code == 401