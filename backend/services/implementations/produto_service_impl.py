from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.produto_model import Produtos
from backend.schemas.produto_schema import ProdutoCreate, ProdutoUpdate


class ProdutoServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, produto: ProdutoCreate):

        db = Produtos(**produto.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

    # LIST
    def listar(self):
        return self.session.scalars(select(Produtos)).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Produtos).where(Produtos.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, produto: ProdutoUpdate):

        db = self.session.scalars(
            select(Produtos).where(Produtos.id == id)
        ).first()

        if not db:
            return None

        dados = produto.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Produtos).where(Produtos.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True