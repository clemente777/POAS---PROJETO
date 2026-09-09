from datetime import datetime

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.atendimento_model import Atendimentos
from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios


class AtendimentoRepository:
    """
    Repository responsável exclusivamente pelo acesso
    ao banco de dados dos atendimentos.
    """

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # BUSCAR ATENDIMENTO POR ID
    # ==========================================================

    def buscar_por_id(
        self,
        atendimento_id: int
    ) -> Atendimentos | None:

        return self.session.get(
            Atendimentos,
            atendimento_id
        )

    # ==========================================================
    # BUSCAR USUÁRIO
    # ==========================================================

    def buscar_usuario(
        self,
        usuario_id: int
    ) -> Usuarios | None:

        return self.session.get(
            Usuarios,
            usuario_id
        )

    # ==========================================================
    # BUSCAR ANIMAL
    # ==========================================================

    def buscar_animal(
        self,
        animal_id: int
    ) -> Animais | None:

        return self.session.get(
            Animais,
            animal_id
        )

    # ==========================================================
    # BUSCAR CLIENTE PELO USUÁRIO
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
    # VERIFICAR ATENDIMENTO DUPLICADO
    # ==========================================================

    def buscar_duplicado(
        self,
        animal_id: int,
        data: datetime,
        excluir_id: int | None = None
    ) -> Atendimentos | None:

        query = (
            select(Atendimentos)
            .where(
                Atendimentos.animal_id == animal_id
            )
            .where(
                Atendimentos.data_atendimento == data
            )
        )

        if excluir_id is not None:

            query = query.where(
                Atendimentos.id != excluir_id
            )

        return self.session.scalar(query)

    # ==========================================================
    # LISTAR ATENDIMENTOS
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

        query = select(Atendimentos)

        # ------------------------------------------------------
        # FILTRO POR CLIENTE
        # ------------------------------------------------------

        if cliente_id is not None:

            query = (
                query
                .join(
                    Animais,
                    Animais.id == Atendimentos.animal_id
                )
                .where(
                    Animais.cliente_id == cliente_id
                )
            )

        # ------------------------------------------------------
        # FILTRO POR ANIMAL
        # ------------------------------------------------------

        if animal_id is not None:

            query = query.where(
                Atendimentos.animal_id == animal_id
            )

        # ------------------------------------------------------
        # FILTRO POR USUÁRIO / VETERINÁRIO
        # ------------------------------------------------------

        if usuario_id is not None:

            query = query.where(
                Atendimentos.usuario_id == usuario_id
            )

        # ------------------------------------------------------
        # FILTRO POR DIAGNÓSTICO
        # ------------------------------------------------------

        if diagnostico:

            query = query.where(
                Atendimentos.diagnostico.ilike(
                    f"%{diagnostico}%"
                )
            )

        # ------------------------------------------------------
        # FILTRO POR DATA
        # ------------------------------------------------------

        if data is not None:

            query = query.where(
                Atendimentos.data_atendimento == data
            )

        # ------------------------------------------------------
        # ORDENAÇÃO
        # ------------------------------------------------------

        campos_ordenacao = {
            "id": Atendimentos.id,
            "data_atendimento": (
                Atendimentos.data_atendimento
            ),
            "usuario_id": Atendimentos.usuario_id,
            "animal_id": Atendimentos.animal_id,
            "diagnostico": Atendimentos.diagnostico,
            "status": Atendimentos.status
        }

        campo = campos_ordenacao.get(
            sort_by,
            Atendimentos.data_atendimento
        )

        if order.lower() == "desc":

            query = query.order_by(
                desc(campo)
            )

        else:

            query = query.order_by(
                asc(campo)
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
    # LISTAR HISTÓRICO DO ANIMAL
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
            .order_by(
                Atendimentos.data_atendimento.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return self.session.scalars(
            query
        ).all()

    # ==========================================================
    # CRIAR
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

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

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

    # ==========================================================
    # DELETAR
    #
    # O Service bloqueia essa operação porque o histórico
    # dos atendimentos deve ser preservado.
    # ==========================================================

    def deletar(
        self,
        atendimento: Atendimentos
    ) -> None:

        try:

            self.session.delete(
                atendimento
            )

            self.session.commit()

        except Exception:

            self.session.rollback()

            raise

