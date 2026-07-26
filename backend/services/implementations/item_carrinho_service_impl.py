from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session

from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.carrinho_model import Carrinhos
from backend.models.produto_model import Produtos
from backend.models.cliente_model import Clientes

from backend.schemas.item_carrinho_schema import (
    ItemCarrinhoCreate,
    ItemCarrinhoUpdate
)


class ItemCarrinhoServiceImpl:


    def __init__(
        self,
        session: Session,
        usuario_logado
    ):

        self.session = session
        self.usuario_logado = usuario_logado



    # ==================================================
    # VALIDAR PROPRIETÁRIO
    # ==================================================

    def validar_proprietario(
        self,
        carrinho: Carrinhos
    ):


        if self.usuario_logado.perfil == "Administrador":
            return


        if not carrinho.cliente:

            raise HTTPException(
                status_code=404,
                detail="Cliente do carrinho não encontrado."
            )


        if carrinho.cliente.usuario_id != self.usuario_logado.id:

            raise HTTPException(
                status_code=403,
                detail="Você não possui permissão para acessar este carrinho."
            )



    # ==================================================
    # BUSCAR ITEM POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):


        item = self.session.scalar(

            select(ItensCarrinho)
            .where(
                ItensCarrinho.id == id
            )

        )


        if not item:

            raise HTTPException(
                status_code=404,
                detail="Item não encontrado."
            )


        self.validar_proprietario(
            item.carrinho
        )


        return item



    # ==================================================
    # BUSCAR CARRINHO
    # ==================================================

    def buscar_carrinho(
        self,
        carrinho_id: int
    ):


        carrinho = self.session.scalar(

            select(Carrinhos)
            .where(
                Carrinhos.id == carrinho_id
            )

        )


        if not carrinho:

            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado"
            )


        self.validar_proprietario(
            carrinho
        )


        return carrinho



    # ==================================================
    # BUSCAR PRODUTO
    # ==================================================

    def buscar_produto(
        self,
        produto_id: int
    ):


        produto = self.session.scalar(

            select(Produtos)
            .where(
                Produtos.id == produto_id
            )

        )


        if not produto:

            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )


        return produto
    
        # ==================================================
    # CRIAR ITEM NO CARRINHO
    # ==================================================

    def criar(
        self,
        item: ItemCarrinhoCreate
    ):

        """
        Adiciona produto ao carrinho.

        Regras:

        - Carrinho precisa existir.
        - Usuário precisa ser dono.
        - Produto precisa existir.
        - Quantidade deve ser positiva.
        - Não pode ultrapassar estoque.
        - Produto repetido soma quantidade.
        """


        if item.quantidade <= 0:

            raise HTTPException(
                status_code=400,
                detail="Quantidade deve ser maior que zero."
            )



        carrinho = self.session.scalar(

            select(Carrinhos)
            .where(
                Carrinhos.id == item.carrinho_id
            )

        )



        if not carrinho:

            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado"
            )



        self.validar_proprietario(
            carrinho
        )



        produto = self.session.scalar(

            select(Produtos)
            .where(
                Produtos.id == item.produto_id
            )

        )



        if not produto:

            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )



        if item.quantidade > produto.estoque:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Quantidade maior que "
                    "estoque disponível."
                )
            )



        item_existente = self.session.scalar(

            select(ItensCarrinho)
            .where(

                ItensCarrinho.carrinho_id
                ==
                item.carrinho_id

            )
            .where(

                ItensCarrinho.produto_id
                ==
                item.produto_id

            )

        )



        if item_existente:


            nova_quantidade = (

                item_existente.quantidade

                +

                item.quantidade

            )



            if nova_quantidade > produto.estoque:


                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade total "
                        "ultrapassa estoque."
                    )
                )



            item_existente.quantidade = nova_quantidade


            self.session.commit()

            self.session.refresh(
                item_existente
            )


            return item_existente





        novo_item = ItensCarrinho(

            **item.model_dump()

        )



        self.session.add(
            novo_item
        )


        self.session.commit()


        self.session.refresh(
            novo_item
        )



        return novo_item







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
        Lista itens permitidos
        pelo usuário logado.
        """



        query = select(
            ItensCarrinho
        )



        # Cliente só vê seus itens

        if self.usuario_logado.perfil != "Administrador":


            query = (

                query

                .join(
                    Carrinhos
                )

                .join(
                    Clientes
                )

                .where(

                    Clientes.usuario_id
                    ==
                    self.usuario_logado.id

                )

            )



        if carrinho_id is not None:


            query = query.where(

                ItensCarrinho.carrinho_id
                ==
                carrinho_id

            )



        if produto_id is not None:


            query = query.where(

                ItensCarrinho.produto_id
                ==
                produto_id

            )



        if quantidade_min is not None:


            query = query.where(

                ItensCarrinho.quantidade
                >=
                quantidade_min

            )



        if quantidade_max is not None:


            query = query.where(

                ItensCarrinho.quantidade
                <=
                quantidade_max

            )



        campos = {

            "id":
            ItensCarrinho.id,


            "quantidade":
            ItensCarrinho.quantidade

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
      
    #------------------------------------------   
    #ATUALIZAR
    #------------------------------------------  
    def atualizar(
    self,
    id: int,
    item: ItemCarrinhoUpdate
):


        item_db = self.buscar_por_id(id)


        dados = item.model_dump(
            exclude_unset=True
        )


        if "quantidade" in dados:


            quantidade = dados["quantidade"]


            if quantidade <= 0:

                raise HTTPException(
                    status_code=400,
                    detail="Quantidade deve ser maior que zero."
                )


            item_db.quantidade = quantidade



        self.session.commit()

        self.session.refresh(
            item_db
        )


        return item_db
    # ==================================================
    # DELETAR ITEM
    # ==================================================

    def deletar(
        self,
        id: int
    ):


        item = self.buscar_por_id(
            id
        )


        self.session.delete(
            item
        )


        self.session.commit()


        return True