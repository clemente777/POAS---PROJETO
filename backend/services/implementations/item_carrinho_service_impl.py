from sqlalchemy import select, asc, desc
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
    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        carrinho_id: int | None = None,
        produto_id: int | None = None,
        quantidade_min: int | None = None,
        quantidade_max: int | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):

        query = select(ItensCarrinho)

        # ==========================
        # FILTROS
        # ==========================

        if carrinho_id is not None:
            query = query.where(
                ItensCarrinho.carrinho_id == carrinho_id
            )

        if produto_id is not None:
            query = query.where(
                ItensCarrinho.produto_id == produto_id
            )

        if quantidade_min is not None:
            query = query.where(
                ItensCarrinho.quantidade >= quantidade_min
            )

        if quantidade_max is not None:
            query = query.where(
                ItensCarrinho.quantidade <= quantidade_max
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": ItensCarrinho.id,
            "quantidade": ItensCarrinho.quantidade,
            "produto_id": ItensCarrinho.produto_id,
            "carrinho_id": ItensCarrinho.carrinho_id,
        }

        coluna = campos.get(
            sort_by,
            ItensCarrinho.id
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