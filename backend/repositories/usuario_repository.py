from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.usuario_model import Usuarios


class UsuarioRepository:
    """Acesso ao banco de dados dos usuários."""

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # BUSCAR POR ID
    # ==========================================================

    def buscar_por_id(self, usuario_id: int):
        return self.session.scalar(
            select(Usuarios).where(
                Usuarios.id == usuario_id
            )
        )

    # ==========================================================
    # BUSCAR POR EMAIL
    # ==========================================================

    def buscar_por_email(self, email: str):
        return self.session.scalar(
            select(Usuarios).where(
                Usuarios.email == email
            )
        )

    # ==========================================================
    # LISTAR
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        email: str | None = None,
        perfil: str | None = None,
        sort_by: str = "id",
        order: str = "asc"
    ):
        query = select(Usuarios)

        # ------------------------------------------------------
        # FILTRO POR NOME
        # ------------------------------------------------------

        if nome:
            query = query.where(
                Usuarios.nome.ilike(
                    f"%{nome.strip()}%"
                )
            )

        # ------------------------------------------------------
        # FILTRO POR EMAIL
        # ------------------------------------------------------

        if email:
            query = query.where(
                Usuarios.email.ilike(
                    f"%{email.strip()}%"
                )
            )

        # ------------------------------------------------------
        # FILTRO POR PERFIL
        # ------------------------------------------------------

        if perfil:
            query = query.where(
                Usuarios.perfil == perfil
            )

        # ------------------------------------------------------
        # ORDENAÇÃO
        # ------------------------------------------------------

        campos = {
            "id": Usuarios.id,
            "nome": Usuarios.nome,
            "email": Usuarios.email,
            "perfil": Usuarios.perfil,
            "criado_em": Usuarios.criado_em
        }

        coluna = campos.get(
            sort_by,
            Usuarios.id
        )

        if order.lower() == "desc":
            query = query.order_by(
                desc(coluna)
            )
        else:
            query = query.order_by(
                asc(coluna)
            )

        # ------------------------------------------------------
        # PAGINAÇÃO
        # ------------------------------------------------------

        query = (
            query
            .offset(skip)
            .limit(limit)
        )

        return self.session.scalars(
            query
        ).all()

    # ==========================================================
    # CRIAR
    # ==========================================================

    def criar(self, usuario: Usuarios):

        try:
            self.session.add(usuario)
            self.session.commit()
            self.session.refresh(usuario)

            return usuario

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

    def atualizar(self, usuario: Usuarios):

        try:
            self.session.commit()
            self.session.refresh(usuario)

            return usuario

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # DELETAR
    # ==========================================================

    def deletar(self, usuario: Usuarios):

        try:
            self.session.delete(usuario)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

