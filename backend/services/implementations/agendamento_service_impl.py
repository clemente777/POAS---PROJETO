from sqlalchemy import select
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
    def listar(self):
        return self.session.scalars(select(Agendamentos)).all()

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