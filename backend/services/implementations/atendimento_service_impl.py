from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.atendimento_model import Atendimentos
from backend.schemas.atendimento_schema import AtendimentoCreate, AtendimentoUpdate


class AtendimentoServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, atendimento: AtendimentoCreate):

        db = Atendimentos(**atendimento.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

    # LIST
    def listar(self):
        return self.session.scalars(select(Atendimentos)).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Atendimentos).where(Atendimentos.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, atendimento: AtendimentoUpdate):

        db = self.session.scalars(
            select(Atendimentos).where(Atendimentos.id == id)
        ).first()

        if not db:
            return None

        dados = atendimento.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Atendimentos).where(Atendimentos.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True