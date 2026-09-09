from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.produto_model import Produtos


class ProdutoRepository:

    def __init__(self, session: Session):
        self.session = session

    # ==================================================
    # BUSCAR PRODUTO POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        return self.session.scalar(
            select(Produtos)
            .where(
                Produtos.id == id
            )
        )

    # ==================================================
    # BUSCAR PRODUTO POR NOME
    # ==================================================

    def buscar_por_nome(
        self,
        nome: str
    ):
        return self.session.scalar(
            select(Produtos)
            .where(
                Produtos.nome == nome
            )
        )

    # ==================================================
    # LISTAR PRODUTOS
    # ==================================================

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
        order: str = "asc"
    ):
        query = select(
            Produtos
        )

        # ==================================================
        # FILTRO POR NOME
        # ==================================================

        if nome:
            query = query.where(
                Produtos.nome.ilike(
                    f"%{nome.strip()}%"
                )
            )

        # ==================================================
        # FILTRO POR DESCRIÇÃO
        # ==================================================

        if descricao:
            query = query.where(
                Produtos.descricao.ilike(
                    f"%{descricao.strip()}%"
                )
            )

        # ==================================================
        # FILTRO DE PREÇO MÍNIMO
        # ==================================================

        if preco_min is not None:
            query = query.where(
                Produtos.preco >= preco_min
            )

        # ==================================================
        # FILTRO DE PREÇO MÁXIMO
        # ==================================================

        if preco_max is not None:
            query = query.where(
                Produtos.preco <= preco_max
            )

        # ==================================================
        # FILTRO DE ESTOQUE MÍNIMO
        # ==================================================

        if estoque_min is not None:
            query = query.where(
                Produtos.estoque >= estoque_min
            )

        # ==================================================
        # FILTRO DE ESTOQUE MÁXIMO
        # ==================================================

        if estoque_max is not None:
            query = query.where(
                Produtos.estoque <= estoque_max
            )

        # ==================================================
        # FILTRO DE PRODUTOS EM ESTOQUE
        # ==================================================

        if em_estoque is True:
            query = query.where(
                Produtos.estoque > 0
            )

        # ==================================================
        # FILTRO DE PRODUTOS SEM ESTOQUE
        # ==================================================

        if em_estoque is False:
            query = query.where(
                Produtos.estoque == 0
            )

        # ==================================================
        # ORDENAÇÃO
        # ==================================================

        campos = {
            "id": Produtos.id,
            "nome": Produtos.nome,
            "descricao": Produtos.descricao,
            "preco": Produtos.preco,
            "estoque": Produtos.estoque
        }

        coluna = campos.get(
            sort_by,
            Produtos.nome
        )

        if order.lower() == "desc":
            query = query.order_by(
                desc(coluna)
            )
        else:
            query = query.order_by(
                asc(coluna)
            )

        # ==================================================
        # PAGINAÇÃO
        # ==================================================

        if skip < 0:
            skip = 0

        if limit <= 0:
            limit = 10

        if limit > 100:
            limit = 100

        query = (
            query
            .offset(skip)
            .limit(limit)
        )

        return self.session.scalars(
            query
        ).all()

    # ==================================================
    # CRIAR PRODUTO
    # ==================================================

    def criar(
        self,
        produto: Produtos
    ):
        self.session.add(
            produto
        )

        self.session.commit()

        self.session.refresh(
            produto
        )

        return produto

    # ==================================================
    # ATUALIZAR PRODUTO
    # ==================================================

    def atualizar(
        self,
        produto: Produtos
    ):
        self.session.commit()

        self.session.refresh(
            produto
        )

        return produto

    # ==================================================
    # DELETAR PRODUTO
    # ==================================================

    def deletar(
        self,
        produto: Produtos
    ):
        self.session.delete(
            produto
        )

        self.session.commit()

        return True

    # ==================================================
    # ROLLBACK
    # ==================================================

    def rollback(self):
        self.session.rollback()

