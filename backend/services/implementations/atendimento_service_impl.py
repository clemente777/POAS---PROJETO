from sqlalchemy import select, asc, desc
from datetime import datetime
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
    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        usuario_id: int | None = None,
        diagnostico: str | None = None,
        data: datetime | None = None,
        sort_by: str = "data_atendimento",
        order: str = "asc",
    ):

        query = select(Atendimentos)

        # ==========================
        # FILTROS
        # ==========================

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
                    f"%{diagnostico}%"
                )
            )

        if data:
            query = query.where(
                Atendimentos.data_atendimento == data
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Atendimentos.id,
            "data_atendimento": Atendimentos.data_atendimento,
            "diagnostico": Atendimentos.diagnostico,
            "usuario_id": Atendimentos.usuario_id,
            "animal_id": Atendimentos.animal_id,
        }

        coluna = campos.get(
            sort_by,
            Atendimentos.data_atendimento
        )

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