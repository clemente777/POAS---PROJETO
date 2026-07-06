from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.item_carrinho_model import ItensCarrinho
from backend.schemas.item_carrinho_schema import ItemCarrinhoCreate, ItemCarrinhoUpdate


class ItemCarrinhoServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, item: ItemCarrinhoCreate):

        db = ItensCarrinho(**item.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

    # LIST
    def listar(self):
        return self.session.scalars(select(ItensCarrinho)).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(ItensCarrinho).where(ItensCarrinho.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, item: ItemCarrinhoUpdate):

        db = self.session.scalars(
            select(ItensCarrinho).where(ItensCarrinho.id == id)
        ).first()

        if not db:
            return None

        dados = item.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(ItensCarrinho).where(ItensCarrinho.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True