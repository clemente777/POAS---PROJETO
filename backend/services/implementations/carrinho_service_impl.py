from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.carrinho_model import Carrinhos
from backend.schemas.carrinho_schema import CarrinhoCreate, CarrinhoUpdate


class CarrinhoServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, carrinho: CarrinhoCreate):

        db = Carrinhos(**carrinho.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

    # LIST
    def listar(self):
        return self.session.scalars(select(Carrinhos)).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Carrinhos).where(Carrinhos.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, carrinho: CarrinhoUpdate):

        db = self.session.scalars(
            select(Carrinhos).where(Carrinhos.id == id)
        ).first()

        if not db:
            return None

        dados = carrinho.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Carrinhos).where(Carrinhos.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True