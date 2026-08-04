from sqlalchemy import select
from pwdlib import PasswordHash

from backend.database.database import SessionLocal
from backend.models.usuario_model import Usuarios


senha_context = PasswordHash.recommended()


def criar_admin():

    session = SessionLocal()

    try:

        admin = session.scalar(

            select(Usuarios).where(
                Usuarios.email == "admin@poas.com"
            )

        )

        if admin:

            print("Administrador já existe.")
            return

        admin = Usuarios(

            nome="Administrador",

            email="admin@poas.com",

            senha_hash=senha_context.hash("admin123"),

            perfil="Administrador"

        )

        session.add(admin)

        session.commit()

        session.refresh(admin)

        print("====================================")
        print("Administrador criado com sucesso!")
        print("Email : admin@poas.com")
        print("Senha : admin123")
        print("====================================")

    except Exception as e:

        session.rollback()

        print("Erro ao criar administrador:")
        print(e)

    finally:

        session.close()