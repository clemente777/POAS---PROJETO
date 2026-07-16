from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.carrinho_model import Carrinhos
from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.cliente_model import Clientes

from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoUpdate
)


class CarrinhoServiceImpl:
    """
    Service responsável pelas regras
    de negócio do carrinho.

    Responsabilidades:

    - Criar carrinhos
    - Garantir um carrinho por cliente
    - Buscar carrinhos
    - Atualizar carrinho
    - Finalizar compras
    - Controlar integridade dos dados
    """

    def __init__(
        self,
        session: Session
    ):
        self.session = session


    # ==================================================
    # BUSCAS AUXILIARES
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        """
        Busca um carrinho pelo ID.
        """

        return self.session.scalars(
            select(Carrinhos)
            .where(
                Carrinhos.id == id
            )
        ).first()


    def buscar_por_cliente(
        self,
        cliente_id: int
    ):
        """
        Busca o carrinho de um cliente.

        Regra:

        Cada cliente possui
        apenas um carrinho.
        """

        return self.session.scalars(
            select(Carrinhos)
            .where(
                Carrinhos.cliente_id == cliente_id
            )
        ).first()


    def validar_cliente(
        self,
        cliente_id: int
    ):
        """
        Verifica se o cliente existe.
        """

        cliente = self.session.scalars(
            select(Clientes)
            .where(
                Clientes.id == cliente_id
            )
        ).first()


        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )


    # ==================================================
    # CRIAR CARRINHO
    # ==================================================

    def criar(
        self,
        carrinho: CarrinhoCreate
    ):
        """
        Cria um carrinho.

        Regras:

        1 - Cliente precisa existir

        2 - Cliente não pode possuir
            outro carrinho
        """

        self.validar_cliente(
            carrinho.cliente_id
        )


        carrinho_existente = self.buscar_por_cliente(
            carrinho.cliente_id
        )


        if carrinho_existente:
            raise HTTPException(
                status_code=409,
                detail="Cliente já possui um carrinho."
            )


        db = Carrinhos(
            **carrinho.model_dump()
        )


        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db
    
        # ==================================================
    # LISTAR CARRINHOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        cliente_id: int | None = None,
        data_criacao: datetime | None = None,
        sort_by: str = "data_criacao",
        order: str = "desc",
    ):
        """
        Lista carrinhos.

        Possui:

        - Paginação
        - Filtro por cliente
        - Filtro por data
        - Ordenação
        """

        query = select(Carrinhos)


        if cliente_id is not None:
            query = query.where(
                Carrinhos.cliente_id == cliente_id
            )


        if data_criacao:
            query = query.where(
                Carrinhos.data_criacao == data_criacao
            )


        campos = {
            "id": Carrinhos.id,
            "cliente_id": Carrinhos.cliente_id,
            "data_criacao": Carrinhos.data_criacao
        }


        coluna = campos.get(
            sort_by,
            Carrinhos.data_criacao
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
    # ATUALIZAR CARRINHO
    # ==================================================

    def atualizar(
        self,
        id: int,
        carrinho: CarrinhoUpdate
    ):
        """
        Atualiza informações
        do carrinho.

        Alterações permitidas:

        - cliente_id

        Validação:

        Cliente precisa existir.
        """

        db = self.buscar_por_id(id)


        if not db:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )


        dados = carrinho.model_dump(
            exclude_unset=True
        )


        if "cliente_id" in dados:

            self.validar_cliente(
                dados["cliente_id"]
            )


            outro = self.buscar_por_cliente(
                dados["cliente_id"]
            )


            if outro and outro.id != id:

                raise HTTPException(
                    status_code=409,
                    detail="Cliente já possui carrinho."
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
    # DELETAR CARRINHO
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        """
        Remove um carrinho.

        Regra:

        Carrinho com itens
        não pode ser removido.
        """

        carrinho = self.buscar_por_id(id)


        if not carrinho:

            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )


        if carrinho.itens:

            raise HTTPException(
                status_code=409,
                detail=
                "Carrinho possui produtos. "
                "Remova os itens antes de excluir."
            )


        self.session.delete(carrinho)

        self.session.commit()


        return True
    
        # ==================================================
    # FINALIZAR COMPRA
    # ==================================================

    def finalizar_compra(
        self,
        carrinho_id: int
    ):
        """
        Finaliza uma compra.

        Fluxo:

        Carrinho

            ↓

        Verifica itens

            ↓

        Verifica estoque

            ↓

        Calcula valor

            ↓

        Baixa estoque

            ↓

        Remove itens do carrinho

            ↓

        Retorna resumo
        """

        carrinho = self.buscar_por_id(
            carrinho_id
        )


        if not carrinho:

            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )


        if not carrinho.itens:

            raise HTTPException(
                status_code=400,
                detail="Carrinho vazio."
            )


        valor_total = 0

        quantidade_itens = 0


        try:

            # ==========================================
            # VALIDAR ESTOQUE
            # ==========================================

            for item in carrinho.itens:

                produto = item.produto


                if produto.estoque < item.quantidade:

                    raise HTTPException(
                        status_code=409,
                        detail=
                        f"Estoque insuficiente para {produto.nome}."
                    )


            # ==========================================
            # BAIXAR ESTOQUE
            # ==========================================

            for item in carrinho.itens:

                produto = item.produto


                produto.estoque -= item.quantidade


                valor_total += (
                    produto.preco *
                    item.quantidade
                )


                quantidade_itens += (
                    item.quantidade
                )


            # ==========================================
            # LIMPAR CARRINHO
            # ==========================================

            for item in carrinho.itens:

                self.session.delete(item)


            self.session.commit()


        except HTTPException:

            self.session.rollback()

            raise


        except Exception:

            self.session.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao finalizar compra."
            )


        return {
            "mensagem":
            "Compra finalizada com sucesso.",

            "valor_total":
            valor_total,

            "quantidade_itens":
            quantidade_itens
        }