from datetime import datetime

from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session, joinedload

from backend.models.atendimento_model import Atendimentos
from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios


class AtendimentoRepository:

    def __init__(
        self,
        session: Session
    ):
        self.session = session

    # ==========================================================
    # ATENDIMENTO
    # ==========================================================

    def buscar_por_id(
        self,
        atendimento_id: int
    ) -> Atendimentos | None:

        return self.session.scalar(
            select(Atendimentos)
            .where(
                Atendimentos.id == atendimento_id
            )
            .options(
                joinedload(Atendimentos.animal),
                joinedload(Atendimentos.usuario)
            )
        )

    def buscar_duplicado(
        self,
        animal_id: int,
        data: datetime,
        excluir_id: int | None = None
    ) -> Atendimentos | None:

        query = (
            select(Atendimentos)
            .where(
                Atendimentos.animal_id == animal_id,
                Atendimentos.data_atendimento == data
            )
        )

        if excluir_id is not None:

            query = query.where(
                Atendimentos.id != excluir_id
            )

        return self.session.scalar(query)

    # ==========================================================
    # USUÁRIO
    # ==========================================================

    def buscar_usuario(
        self,
        usuario_id: int
    ) -> Usuarios | None:

        return self.session.scalar(
            select(Usuarios)
            .where(
                Usuarios.id == usuario_id
            )
        )

    # ==========================================================
    # ANIMAL
    # ==========================================================

    def buscar_animal(
        self,
        animal_id: int
    ) -> Animais | None:

        return self.session.scalar(
            select(Animais)
            .where(
                Animais.id == animal_id
            )
            .options(
                joinedload(Animais.cliente)
            )
        )

    # ==========================================================
    # CLIENTE
    # ==========================================================

    def buscar_cliente_por_usuario(
        self,
        usuario_id: int
    ) -> Clientes | None:

        return self.session.scalar(
            select(Clientes)
            .where(
                Clientes.usuario_id == usuario_id
            )
        )

    # ==========================================================
    # LISTAR
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        usuario_id: int | None = None,
        diagnostico: str | None = None,
        data: datetime | None = None,
        cliente_id: int | None = None,
        sort_by: str = "data_atendimento",
        order: str = "asc"
    ) -> list[Atendimentos]:

        query = select(
            Atendimentos
        )

        # ------------------------------------------------------
        # FILTRO POR CLIENTE
        # ------------------------------------------------------

        if cliente_id is not None:

            query = (
                query
                .join(
                    Atendimentos.animal
                )
                .where(
                    Animais.cliente_id == cliente_id
                )
            )

        # ------------------------------------------------------
        # FILTROS
        # ------------------------------------------------------

        if animal_id is not None:

            query = query.where(
                Atendimentos.animal_id == animal_id
            )

        if usuario_id is not None:

            query = query.where(
                Atendimentos.usuario_id == usuario_id
            )

        if diagnostico:

            query = query.where(
                Atendimentos.diagnostico.ilike(
                    f"%{diagnostico.strip()}%"
                )
            )

        if data is not None:

            query = query.where(
                Atendimentos.data_atendimento == data
            )

        # ------------------------------------------------------
        # ORDENAÇÃO
        # ------------------------------------------------------

        campos = {
            "id": Atendimentos.id,
            "data_atendimento": Atendimentos.data_atendimento,
            "diagnostico": Atendimentos.diagnostico,
            "animal_id": Atendimentos.animal_id,
            "usuario_id": Atendimentos.usuario_id
        }

        coluna = campos.get(
            sort_by,
            Atendimentos.data_atendimento
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
    # HISTÓRICO
    # ==========================================================

    def listar_historico(
        self,
        animal_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> list[Atendimentos]:

        query = (
            select(Atendimentos)
            .where(
                Atendimentos.animal_id == animal_id
            )
            .options(
                joinedload(Atendimentos.usuario)
            )
            .order_by(
                desc(
                    Atendimentos.data_atendimento
                )
            )
            .offset(skip)
            .limit(limit)
        )

        return self.session.scalars(
            query
        ).all()

    # ==========================================================
    # PERSISTÊNCIA
    # ==========================================================

    def criar(
        self,
        atendimento: Atendimentos
    ) -> Atendimentos:

        try:

            self.session.add(
                atendimento
            )

            self.session.commit()

            self.session.refresh(
                atendimento
            )

            return atendimento

        except Exception:

            self.session.rollback()

            raise

    def atualizar(
        self,
        atendimento: Atendimentos
    ) -> Atendimentos:

        try:

            self.session.commit()

            self.session.refresh(
                atendimento
            )

            return atendimento

        except Exception:

            self.session.rollback()

            raise