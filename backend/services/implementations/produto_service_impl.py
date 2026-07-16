from sqlalchemy import asc, desc, select
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
    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        descricao: str | None = None,
        preco_min: float | None = None,
        preco_max: float | None = None,
        estoque_min: int | None = None,
        estoque_max: int | None = None,
        em_estoque: bool | None = None,
        sort_by: str = "nome",
        order: str = "asc",
    ):

        query = select(Produtos)

        # ==========================
        # FILTROS
        # ==========================

        if nome:
            query = query.where(
                Produtos.nome.ilike(f"%{nome}%")
            )

        if descricao:
            query = query.where(
                Produtos.descricao.ilike(f"%{descricao}%")
            )

        if preco_min is not None:
            query = query.where(
                Produtos.preco >= preco_min
            )

        if preco_max is not None:
            query = query.where(
                Produtos.preco <= preco_max
            )

        if estoque_min is not None:
            query = query.where(
                Produtos.estoque >= estoque_min
            )

        if estoque_max is not None:
            query = query.where(
                Produtos.estoque <= estoque_max
            )

        if em_estoque:
            query = query.where(
                Produtos.estoque > 0
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Produtos.id,
            "nome": Produtos.nome,
            "descricao": Produtos.descricao,
            "preco": Produtos.preco,
            "estoque": Produtos.estoque,
        }

        coluna = campos.get(sort_by, Produtos.nome)

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