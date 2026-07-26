from backend.models.usuario_model import Usuarios


# =====================================================
# Cadastro normal sempre cria Cliente
# =====================================================

def test_cadastro_normal_cria_cliente(client):

    response = client.post(
        "/usuarios/",
        json={
            "nome": "Maria",
            "email": "maria@email.com",
            "senha": "123456"
        }
    )


    assert response.status_code == 201


    data = response.json()


    assert data["nome"] == "Maria"

    assert data["email"] == "maria@email.com"

    assert data["perfil"] == "Cliente"



# =====================================================
# Administrador cria Veterinário
# =====================================================

def test_admin_cria_veterinario(
    client,
    admin_headers
):

    response = client.post(
        "/usuarios/admin",
        headers=admin_headers,
        json={
            "nome": "Carlos",
            "email": "carlos@email.com",
            "senha": "123456",
            "perfil": "Veterinário"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["nome"] == "Carlos"

    assert data["perfil"] == "Veterinário"



# =====================================================
# Administrador cria outro Administrador
# =====================================================

def test_admin_cria_administrador(
    client,
    admin_headers
):

    response = client.post(
        "/usuarios/admin",
        headers=admin_headers,
        json={
            "nome": "Ana",
            "email": "ana@email.com",
            "senha": "123456",
            "perfil": "Administrador"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["perfil"] == "Administrador"



# =====================================================
# Cliente tentando criar usuário administrativo
# =====================================================

def test_cliente_nao_pode_criar_admin(
    client,
    cliente_headers
):

    response = client.post(
        "/usuarios/admin",
        headers=cliente_headers,
        json={
            "nome": "Teste",
            "email": "teste@email.com",
            "senha": "123456",
            "perfil": "Administrador"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 403



# =====================================================
# Perfil inválido
# =====================================================

def test_admin_nao_cria_perfil_invalido(
    client,
    admin_headers
):

    response = client.post(
        "/usuarios/admin",
        headers=admin_headers,
        json={
            "nome": "Teste",
            "email": "perfil@email.com",
            "senha": "123456",
            "perfil": "Gerente"
        }
    )


    assert response.status_code == 400


    assert response.json()["detail"] == (
        "Perfil inválido."
    )



# =====================================================
# Email duplicado
# =====================================================

def test_admin_nao_cria_email_existente(
    client,
    admin_headers
):

    client.post(
        "/usuarios/admin",
        headers=admin_headers,
        json={
            "nome": "João",
            "email": "joao@email.com",
            "senha": "123456",
            "perfil": "Veterinário"
        }
    )


    response = client.post(
        "/usuarios/admin",
        headers=admin_headers,
        json={
            "nome": "Outro",
            "email": "joao@email.com",
            "senha": "123456",
            "perfil": "Cliente"
        }
    )


    assert response.status_code == 409


    assert response.json()["detail"] == (
        "Email já cadastrado."
    )