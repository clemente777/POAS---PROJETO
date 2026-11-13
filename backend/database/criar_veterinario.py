"""
Cria (ou atualiza) um veterinário direto no banco, sem precisar do /docs.

Rode UMA vez, na raiz do projeto (a pasta que contém "backend" e "main.py"),
com o ambiente virtual ativado:

    python -m backend.database.criar_veterinario

Com os dados padrão abaixo, o login fica:
    e-mail: ana.vet@poas.com
    senha:  vet12345

Para usar outros dados:

    python -m backend.database.criar_veterinario "Dr. Carlos" carlos@poas.com senha123

Se o e-mail já existir, a senha e o perfil são redefinidos
(útil quando o login dá "Senha inválida").
"""

import importlib
import pkgutil
import sys

from pwdlib import PasswordHash
from sqlalchemy import select

import backend.models
from backend.database.database import SessionLocal
from backend.models.usuario_model import Usuarios

# Carrega todos os models para o SQLAlchemy resolver os relacionamentos,
# já que este script roda fora do main.py.
for modulo in pkgutil.iter_modules(backend.models.__path__):
    importlib.import_module(f"backend.models.{modulo.name}")


NOME_PADRAO = "Dra. Ana Souza"
EMAIL_PADRAO = "ana.vet@poas.com"
SENHA_PADRAO = "vet12345"
PERFIL = "Veterinário"  # exatamente assim: com acento e inicial maiúscula

senha_context = PasswordHash.recommended()


def main():

    nome = sys.argv[1] if len(sys.argv) > 1 else NOME_PADRAO
    email = (sys.argv[2] if len(sys.argv) > 2 else EMAIL_PADRAO).strip().lower()
    senha = sys.argv[3] if len(sys.argv) > 3 else SENHA_PADRAO

    session = SessionLocal()

    try:

        usuario = session.scalar(
            select(Usuarios).where(Usuarios.email == email)
        )

        if usuario:

            usuario.nome = nome
            usuario.senha_hash = senha_context.hash(senha)
            usuario.perfil = PERFIL

            acao = "atualizado"

        else:

            session.add(
                Usuarios(
                    nome=nome,
                    email=email,
                    senha_hash=senha_context.hash(senha),
                    perfil=PERFIL,
                )
            )

            acao = "criado"

        session.commit()

        print(f"Veterinário {acao}: {email} / {senha}")

    except Exception as erro:

        session.rollback()
        print("Erro ao salvar veterinário:", erro)

    finally:

        session.close()


if __name__ == "__main__":
    main()
