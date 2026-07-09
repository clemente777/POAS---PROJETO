import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pwdlib import PasswordHash

from backend.database.database import Base, get_session
from backend.models.usuario_model import Usuarios
from backend.auth.token import create_access_token

import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"



from main import app

# BANCO DE TESTE

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



# SESSION

@pytest.fixture
def session():

    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)


    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()



# CLIENT

@pytest.fixture
def client(session):

    def override_get_session():

        yield session


    app.dependency_overrides[get_session] = override_get_session


    with TestClient(app) as client:

        yield client


    app.dependency_overrides.clear()




# LOGIN AUTOMÁTICO

@pytest.fixture
def auth_headers(session):

    usuario = Usuarios(
        nome="Administrador",
        email="admin@admin.com",
        senha_hash=senha_context.hash("123456")
    )


    session.add(usuario)

    session.commit()

    session.refresh(usuario)


    token = create_access_token(
        {
            "sub": usuario.email
        }
    )


    return {
        "Authorization": f"Bearer {token}"
    }