import pytest
import os

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pwdlib import PasswordHash


from backend.database.database import Base, get_session

from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes


from backend.auth.token import create_access_token


from main import app



# ==================================================
# BANCO TESTE
# ==================================================

os.environ["DATABASE_URL"] = "sqlite:///./test.db"


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"



engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)



TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)



senha_context = PasswordHash.recommended()



# ==================================================
# SESSION
# ==================================================

@pytest.fixture
def session():

    Base.metadata.drop_all(
        bind=engine
    )


    Base.metadata.create_all(
        bind=engine
    )


    db = TestingSessionLocal()


    try:

        yield db


    finally:

        db.close()




# ==================================================
# CLIENT FASTAPI
# ==================================================

@pytest.fixture
def client(session):


    def override_get_session():

        yield session



    app.dependency_overrides[
        get_session
    ] = override_get_session



    with TestClient(app) as client:

        yield client



    app.dependency_overrides.clear()





# ==================================================
# CRIAR USUARIO
# ==================================================

def criar_usuario(
    session,
    perfil
):


    usuario = Usuarios(

        nome=f"{perfil} Teste",

        email=f"{perfil.lower()}@test.com",

        senha_hash=senha_context.hash(
            "123456"
        ),

        perfil=perfil

    )



    session.add(usuario)

    session.commit()

    session.refresh(usuario)



    return usuario





# ==================================================
# GERAR TOKEN
# ==================================================

def gerar_token(usuario):


    token = create_access_token(
        {
            "sub": usuario.email
        }
    )


    return {

        "Authorization":
        f"Bearer {token}"

    }





# ==================================================
# ADMIN
# ==================================================

@pytest.fixture
def admin_headers(session):


    usuario = criar_usuario(

        session,

        "Administrador"

    )


    return gerar_token(
        usuario
    )





# ==================================================
# VETERINARIO
# ==================================================

@pytest.fixture
def veterinario_headers(session):


    usuario = criar_usuario(

        session,

        "Veterinário"

    )


    return gerar_token(
        usuario
    )





# ==================================================
# CLIENTE
# ==================================================

@pytest.fixture
def cliente_headers(session):


    usuario = criar_usuario(

        session,

        "Cliente"

    )


    return gerar_token(
        usuario
    )





# ==================================================
# PADRÃO AUTENTICADO
# ==================================================

@pytest.fixture
def auth_headers(admin_headers):

    return admin_headers





# ==================================================
# CRIAR CLIENTE COMPLETO
# ==================================================

@pytest.fixture
def criar_cliente(session):


    usuario = criar_usuario(

        session,

        "Cliente"

    )



    cliente = Clientes(

        usuario_id=usuario.id,

        nome="Cliente Teste",

        cpf="52998224725",

        telefone="84999999999",

        email="cliente@test.com",

        endereco="Rua Teste"

    )



    session.add(cliente)

    session.commit()

    session.refresh(cliente)



    return cliente