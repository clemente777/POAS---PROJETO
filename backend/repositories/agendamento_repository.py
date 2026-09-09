from datetime import datetime

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.agendamento_model import Agendamentos
from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios


class AgendamentoRepository:
    """Acesso ao banco de dados dos agendamentos."""

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # BUSCAR AGENDAMENTO POR ID
    # ==========================================================

    def buscar_por_id(self, agendamento_id: int):

        return self.session.scalar(
            select(Agendamentos).where(
                Agendamentos.id == agendamento_id
            )
        )

    # ==========================================================
    # BUSCAR ANIMAL POR ID
    # ==========================================================

    def buscar_animal(self, animal_id: int):

        return self.session.scalar(
            select(Animais).where(
                Animais.id == animal_id
            )
        )

    # ==========================================================
    # BUSCAR CLIENTE PELO USUÁRIO
    # ==========================================================

    def buscar_cliente_por_usuario_id(
        self,
        usuario_id: int
    ):

        return self.session.scalar(
            select(Clientes).where(
                Clientes.usuario_id == usuario_id
            )
        )

    # ==========================================================
    # BUSCAR VETERINÁRIO POR ID
    # ==========================================================

    def buscar_veterinario_por_id(
        self,
        veterinario_id: int
    ):

        return self.session.scalar(
            select(Usuarios).where(
                Usuarios.id == veterinario_id
            )
        )

    # ==========================================================
    # VERIFICAR CONFLITO DE HORÁRIO
    # ==========================================================

    def buscar_conflito_horario(
        self,
        animal_id: int,
        data: datetime,
        agendamento_id: int | None = None
    ):

        query = select(
            Agendamentos
        ).where(
            Agendamentos.animal_id == animal_id,
            Agendamentos.data_agendamento == data,
            Agendamentos.status != "Cancelado"
        )

        if agendamento_id is not None:

            query = query.where(
                Agendamentos.id != agendamento_id
            )

        return self.session.scalar(query)

    # ==========================================================
    # LISTAR AGENDAMENTOS
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        status: str | None = None,
        descricao: str | None = None,
        data: datetime | None = None,
        cliente_id: int | None = None,
        sort_by: str = "data_agendamento",
        order: str = "asc"
    ):

        query = select(Agendamentos)

        # ------------------------------------------------------
        # FILTRO POR CLIENTE
        # ------------------------------------------------------

        if cliente_id is not None:

            query = (
                query
                .join(
                    Animais,
                    Agendamentos.animal_id == Animais.id
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
                Agendamentos.animal_id == animal_id
            )

        # ------------------------------------------------------
        # FILTRO POR STATUS
        # ------------------------------------------------------

        if status is not None:

            query = query.where(
                Agendamentos.status == status
            )

        # ------------------------------------------------------
        # FILTRO POR DESCRIÇÃO
        # ------------------------------------------------------

        if descricao:

            query = query.where(
                Agendamentos.descricao.ilike(
                    f"%{descricao.strip()}%"
                )
            )

        # ------------------------------------------------------
        # FILTRO POR DATA
        # ------------------------------------------------------

        if data is not None:

            query = query.where(
                Agendamentos.data_agendamento == data
            )

        # ------------------------------------------------------
        # ORDENAÇÃO
        # ------------------------------------------------------

        campos = {
            "id": Agendamentos.id,
            "data_agendamento": (
                Agendamentos.data_agendamento
            ),
            "descricao": Agendamentos.descricao,
            "status": Agendamentos.status,
            "animal_id": Agendamentos.animal_id
        }

        coluna = campos.get(
            sort_by,
            Agendamentos.data_agendamento
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

    def criar(
        self,
        agendamento: Agendamentos
    ):

        try:

            self.session.add(
                agendamento
            )

            self.session.commit()

            self.session.refresh(
                agendamento
            )

            return agendamento

        except Exception:

            self.session.rollback()

            raise

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

    def atualizar(
        self,
        agendamento: Agendamentos
    ):

        try:

            self.session.commit()

            self.session.refresh(
                agendamento
            )

            return agendamento

        except Exception:

            self.session.rollback()

            raise

    # ==========================================================
    # CANCELAR
    # ==========================================================

    def cancelar(
        self,
        agendamento: Agendamentos
    ):

        try:

            self.session.commit()

            self.session.refresh(
                agendamento
            )

            return agendamento

        except Exception:

            self.session.rollback()

            raise

    # ==========================================================
    # DELETAR
    #
    # O método existe no Repository porque ele é responsável
    # pelo acesso ao banco.
    #
    # A regra de negócio que bloqueia a exclusão permanece
    # no Service.
    # ==========================================================

    def deletar(
        self,
        agendamento: Agendamentos
    ):

        try:

            self.session.delete(
                agendamento
            )

            self.session.commit()

        except Exception:

            self.session.rollback()

            raise

