from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session

from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.carrinho_model import Carrinhos
from backend.models.produto_model import Produtos

from backend.schemas.item_carrinho_schema import (
    ItemCarrinhoCreate,
    ItemCarrinhoUpdate
)


class ItemCarrinhoServiceImpl:

    def __init__(
        self,
        session: Session
    ):
        self.session = session


    # ==================================================
    # BUSCAR ITEM POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        """
        Busca um item do carrinho pelo ID.
        """

        return self.session.scalars(
            select(ItensCarrinho)
            .where(ItensCarrinho.id == id)
        ).first()


    # ==================================================
    # CRIAR ITEM NO CARRINHO
    # ==================================================

    def criar(
        self,
        item: ItemCarrinhoCreate
    ):
        """
        Adiciona um produto ao carrinho.

        Regras:

        1 - Carrinho precisa existir
        2 - Produto precisa existir
        3 - Quantidade deve ser maior que zero
        4 - Não pode ultrapassar estoque
        5 - Produto repetido soma quantidade
        """


        if item.quantidade <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantidade deve ser maior que zero."
            )


        carrinho = self.session.scalars(
            select(Carrinhos)
            .where(Carrinhos.id == item.carrinho_id)
        ).first()


        if not carrinho:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )


        produto = self.session.scalars(
            select(Produtos)
            .where(Produtos.id == item.produto_id)
        ).first()


        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )


        if item.quantidade > produto.estoque:
            raise HTTPException(
                status_code=400,
                detail="Quantidade maior que estoque disponível."
            )


        existente = self.session.scalars(
            select(ItensCarrinho)
            .where(
                ItensCarrinho.carrinho_id == item.carrinho_id
            )
            .where(
                ItensCarrinho.produto_id == item.produto_id
            )
        ).first()


        if existente:

            nova_quantidade = (
                existente.quantidade +
                item.quantidade
            )


            if nova_quantidade > produto.estoque:
                raise HTTPException(
                    status_code=400,
                    detail="Quantidade total ultrapassa estoque."
                )


            existente.quantidade = nova_quantidade

            self.session.commit()
            self.session.refresh(existente)

            return existente


        db = ItensCarrinho(
            **item.model_dump()
        )


        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)

        return db


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
        sort_by: str = "id",
        order: str = "asc"
    ):
        """
        Lista itens do carrinho.

        Possui:

        - filtros
        - ordenação
        - paginação
        """


        query = select(ItensCarrinho)

        if quantidade_min is not None:

            query = query.where(
                ItensCarrinho.quantidade >= quantidade_min
            )


        if quantidade_max is not None:

            query = query.where(
                ItensCarrinho.quantidade <= quantidade_max
            )
        if carrinho_id is not None:

            query = query.where(
                ItensCarrinho.carrinho_id == carrinho_id
            )


        if produto_id is not None:

            query = query.where(
                ItensCarrinho.produto_id == produto_id
            )


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


        query = (
            query
            .offset(skip)
            .limit(limit)
        )


        return self.session.scalars(query).all()


    # ==================================================
    # ATUALIZAR QUANTIDADE
    # ==================================================

    def atualizar(
        self,
        id: int,
        item: ItemCarrinhoUpdate
    ):
        """
        Atualiza quantidade do produto.
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Item não encontrado."
            )


        dados = item.model_dump(
            exclude_unset=True
        )


        if "quantidade" in dados:

            if dados["quantidade"] <= 0:

                raise HTTPException(
                    status_code=400,
                    detail="Quantidade inválida."
                )


            produto = db.produto


            if dados["quantidade"] > produto.estoque:

                raise HTTPException(
                    status_code=400,
                    detail="Quantidade maior que estoque."
                )


        for campo, valor in dados.items():

            setattr(
                db,
                campo,
                valor
            )


        self.session.commit()

        self.session.refresh(db)

        return db


    # ==================================================
    # DELETAR ITEM
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        """
        Remove um produto do carrinho.
        """


        item = self.buscar_por_id(id)


        if not item:

            raise HTTPException(
                status_code=404,
                detail="Item não encontrado."
            )


        self.session.delete(item)

        self.session.commit()


        return True