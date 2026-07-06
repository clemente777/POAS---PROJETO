from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.cliente_model import Clientes
from backend.schemas.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, cliente: ClienteCreate):

        db = Clientes(**cliente.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

    # LIST
    def listar(self):
        return self.session.scalars(select(Clientes)).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Clientes).where(Clientes.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, cliente: ClienteUpdate):

        db = self.session.scalars(
            select(Clientes).where(Clientes.id == id)
        ).first()

        if not db:
            return None

        dados = cliente.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Clientes).where(Clientes.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True