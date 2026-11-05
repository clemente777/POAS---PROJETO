from sqlalchemy import select
from pwdlib import PasswordHash

from backend.database.database import SessionLocal
from backend.models.usuario_model import Usuarios
from backend.models.produto_model import Produtos


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


def criar_produtos_teste():
    session = SessionLocal()

    produtos = [
        {
            "nome": "Ração para Cães Adultos",
            "descricao": "Ração para alimentação diária de cães adultos.",
            "preco": 89.90,
            "estoque": 20,
        },
        {
            "nome": "Ração para Gatos",
            "descricao": "Alimento completo para gatos adultos.",
            "preco": 74.90,
            "estoque": 15,
        },
        {
            "nome": "Shampoo para Pets",
            "descricao": "Shampoo para higiene e cuidado dos pelos.",
            "preco": 24.90,
            "estoque": 12,
        },
        {
            "nome": "Brinquedo para Cães",
            "descricao": "Brinquedo para diversão e entretenimento.",
            "preco": 19.90,
            "estoque": 10,
        },
        {
            "nome": "Coleira para Cães",
            "descricao": "Coleira ajustável para passeios.",
            "preco": 29.90,
            "estoque": 8,
        },
        {
            "nome": "Areia para Gatos",
            "descricao": "Areia higiênica para a caixa dos gatos.",
            "preco": 32.90,
            "estoque": 18,
        },
    ]

    try:
        for dados in produtos:
            existente = session.scalar(
                select(Produtos).where(
                    Produtos.nome == dados["nome"]
                )
            )

            if existente is None:
                session.add(Produtos(**dados))

        session.commit()
        print("Produtos de teste verificados com sucesso!")

    except Exception as erro:
        session.rollback()
        print("Erro ao criar produtos de teste:", erro)

    finally:
        session.close()
