from sqlalchemy import asc, desc, select
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.agendamento_model import Agendamentos
from backend.schemas.agendamento_schema import AgendamentoCreate, AgendamentoUpdate


class AgendamentoServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, agendamento: AgendamentoCreate):

        db = Agendamentos(
            **agendamento.model_dump(),
            status="Pendente"
        )

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

   

# LIST
    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        status: str | None = None,
        descricao: str | None = None,
        data: datetime | None = None,
        sort_by: str = "data_agendamento",
        order: str = "asc",
    ):

        query = select(Agendamentos)

        # ==========================
        # FILTROS
        # ==========================

        if animal_id is not None:
            query = query.where(
                Agendamentos.animal_id == animal_id
            )

        if status:
            query = query.where(
                Agendamentos.status.ilike(f"%{status}%")
            )

        if descricao:
            query = query.where(
                Agendamentos.descricao.ilike(f"%{descricao}%")
            )

        if data:
            query = query.where(
                Agendamentos.data_agendamento == data
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Agendamentos.id,
            "data_agendamento": Agendamentos.data_agendamento,
            "status": Agendamentos.status,
            "descricao": Agendamentos.descricao,
            "animal_id": Agendamentos.animal_id,
        }

        coluna = campos.get(sort_by, Agendamentos.data_agendamento)

        if order.lower() == "desc":
            query = query.order_by(desc(coluna))
        else:
            query = query.order_by(asc(coluna))

        # ==========================
        # PAGINAÇÃO
        # ==========================

        query = query.offset(skip).limit(limit)

        return self.session.scalars(query).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Agendamentos).where(Agendamentos.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, agendamento: AgendamentoUpdate):

        db = self.session.scalars(
            select(Agendamentos).where(Agendamentos.id == id)
        ).first()

        if not db:
            return None

        dados = agendamento.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Agendamentos).where(Agendamentos.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True