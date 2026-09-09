from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session

from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.carrinho_model import Carrinhos
from backend.models.produto_model import Produtos
from backend.models.cliente_model import Clientes


class ItemCarrinhoRepository:

    def __init__(self, session: Session):
        self.session = session

    # ==================================================
    # BUSCAR ITEM POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        return self.session.scalar(
            select(ItensCarrinho)
            .where(ItensCarrinho.id == id)
        )

    # ==================================================
    # BUSCAR CARRINHO POR ID
    # ==================================================

    def buscar_carrinho(
        self,
        carrinho_id: int
    ):
        return self.session.scalar(
            select(Carrinhos)
            .where(Carrinhos.id == carrinho_id)
        )

    # ==================================================
    # BUSCAR PRODUTO POR ID
    # ==================================================

    def buscar_produto(
        self,
        produto_id: int
    ):
        return self.session.scalar(
            select(Produtos)
            .where(Produtos.id == produto_id)
        )

    # ==================================================
    # BUSCAR CLIENTE POR USUÁRIO
    # ==================================================

    def buscar_cliente_por_usuario_id(
        self,
        usuario_id: int
    ):
        return self.session.scalar(
            select(Clientes)
            .where(Clientes.usuario_id == usuario_id)
        )

    # ==================================================
    # BUSCAR ITEM EXISTENTE
    # ==================================================

    def buscar_item_existente(
        self,
        carrinho_id: int,
        produto_id: int
    ):
        return self.session.scalar(
            select(ItensCarrinho)
            .where(
                ItensCarrinho.carrinho_id == carrinho_id
            )
            .where(
                ItensCarrinho.produto_id == produto_id
            )
        )

    # ==================================================
    # LISTAR ITENS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        carrinho_id: int | None = None,
        produto_id: int | None = None,
        quantidade_min: int | None = None,
        quantidade_max: int | None = None,
        usuario_id: int | None = None,
        somente_proprio_cliente: bool = False,
        sort_by: str = "id",
        order: str = "asc"
    ):
        query = select(ItensCarrinho)

        # --------------------------------------------------
        # CLIENTE SÓ PODE VER OS PRÓPRIOS ITENS
        # --------------------------------------------------

        if somente_proprio_cliente:
            query = (
                query
                .join(
                    Carrinhos,
                    Carrinhos.id == ItensCarrinho.carrinho_id
                )
                .join(
                    Clientes,
                    Clientes.id == Carrinhos.cliente_id
                )
                .where(
                    Clientes.usuario_id == usuario_id
                )
            )

        # --------------------------------------------------
        # FILTRO POR CARRINHO
        # --------------------------------------------------

        if carrinho_id is not None:
            query = query.where(
                ItensCarrinho.carrinho_id == carrinho_id
            )

        # --------------------------------------------------
        # FILTRO POR PRODUTO
        # --------------------------------------------------

        if produto_id is not None:
            query = query.where(
                ItensCarrinho.produto_id == produto_id
            )

        # --------------------------------------------------
        # FILTRO POR QUANTIDADE MÍNIMA
        # --------------------------------------------------

        if quantidade_min is not None:
            query = query.where(
                ItensCarrinho.quantidade >= quantidade_min
            )

        # --------------------------------------------------
        # FILTRO POR QUANTIDADE MÁXIMA
        # --------------------------------------------------

        if quantidade_max is not None:
            query = query.where(
                ItensCarrinho.quantidade <= quantidade_max
            )

        # --------------------------------------------------
        # CAMPOS PERMITIDOS PARA ORDENAÇÃO
        # --------------------------------------------------

        campos = {
            "id": ItensCarrinho.id,
            "quantidade": ItensCarrinho.quantidade
        }

        coluna = campos.get(
            sort_by,
            ItensCarrinho.id
        )

        if order.lower() == "desc":
            query = query.order_by(
                desc(coluna)
            )
        else:
            query = query.order_by(
                asc(coluna)
            )

        # --------------------------------------------------
        # PAGINAÇÃO
        # --------------------------------------------------

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

        return self.session.scalars(query).all()

    # ==================================================
    # CRIAR ITEM
    # ==================================================

    def criar(
        self,
        item: ItensCarrinho
    ):
        self.session.add(item)

        self.session.commit()

        self.session.refresh(item)

        return item

    # ==================================================
    # ATUALIZAR ITEM
    # ==================================================

    def atualizar(
        self,
        item: ItensCarrinho
    ):
        self.session.commit()

        self.session.refresh(item)

        return item

    # ==================================================
    # DELETAR ITEM
    # ==================================================

    def deletar(
        self,
        item: ItensCarrinho
    ):
        self.session.delete(item)

        self.session.commit()

        return True

    # ==================================================
    # ROLLBACK
    # ==================================================

    def rollback(self):
        self.session.rollback()
