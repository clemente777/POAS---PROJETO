from backend.models.usuario_model import Usuarios
from pwdlib import PasswordHash

senha_context = PasswordHash.recommended()
def criar_usuario(session):

    usuario = Usuarios(
        nome="Admin",
        email="admin@test.com",
        senha_hash=senha_context.hash("123456"),
        perfil="Administrador"
    )

    session.add(usuario)

    session.commit()

    session.refresh(usuario)

    return usuario
def test_login_sucesso(client, session):

    criar_usuario(session)

    response = client.post(
        "/login/",
        data={
            "username":"admin@test.com",
            "password":"123456"
        }
    )


    assert response.status_code == 200


    dados = response.json()


    assert "access_token" in dados

    assert dados["token_type"] == "bearer"



def test_login_usuario_inexistente(client):


    response = client.post(
        "/login/",
        data={
            "username":"teste@test.com",
            "password":"123456"
        }
    )


    assert response.status_code == 401



def test_login_senha_errada(client, session):

    criar_usuario(session)


    response = client.post(
        "/login/",
        data={
            "username":"admin@test.com",
            "password":"errada"
        }
    )


    assert response.status_code == 401