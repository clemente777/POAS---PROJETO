from datetime import datetime

from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session

from backend.models.carrinho_model import Carrinhos
from backend.models.cliente_model import Clientes


class CarrinhoRepository:
    """
    Repository responsável exclusivamente pelo acesso
    ao banco de dados relacionado aos carrinhos.

    O Repository é responsável por:
    - Consultas
    - Inclusões
    - Atualizações
    - Exclusões
    - Commit
    - Rollback
    - Refresh
    - Operações de estoque relacionadas à finalização
      da compra
    """

    def __init__(self, session: Session):
        self.session = session

    # ==================================================
    # BUSCAR CARRINHO POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        return self.session.scalar(
            select(Carrinhos).where(
                Carrinhos.id == id
            )
        )

    # ==================================================
    # BUSCAR CARRINHO POR CLIENTE
    # ==================================================

    def buscar_por_cliente(
        self,
        cliente_id: int
    ):
        return self.session.scalar(
            select(Carrinhos).where(
                Carrinhos.cliente_id == cliente_id
            )
        )

    # ==================================================
    # BUSCAR CLIENTE
    # ==================================================

    def buscar_cliente(
        self,
        cliente_id: int
    ):
        return self.session.scalar(
            select(Clientes).where(
                Clientes.id == cliente_id
            )
        )

    # ==================================================
    # LISTAR CARRINHOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        cliente_id: int | None = None,
        data_criacao: datetime | None = None,
        usuario_id: int | None = None,
        somente_proprio_cliente: bool = False,
        sort_by: str = "data_criacao",
        order: str = "desc"
    ):
        query = select(Carrinhos)

        # --------------------------------------------------
        # FILTRO DO CLIENTE LOGADO
        # --------------------------------------------------

        if somente_proprio_cliente and usuario_id is not None:

            query = (
                query
                .join(
                    Clientes,
                    Carrinhos.cliente_id == Clientes.id
                )
                .where(
                    Clientes.usuario_id == usuario_id
                )
            )

        # --------------------------------------------------
        # FILTRO POR CLIENTE
        # --------------------------------------------------

        elif cliente_id is not None:

            query = query.where(
                Carrinhos.cliente_id == cliente_id
            )

        # --------------------------------------------------
        # FILTRO POR DATA
        # --------------------------------------------------

        if data_criacao is not None:

            query = query.where(
                Carrinhos.data_criacao == data_criacao
            )

        # --------------------------------------------------
        # CAMPOS PERMITIDOS PARA ORDENAÇÃO
        # --------------------------------------------------

        campos = {
            "id": Carrinhos.id,
            "cliente_id": Carrinhos.cliente_id,
            "data_criacao": Carrinhos.data_criacao
        }

        coluna = campos.get(
            sort_by,
            Carrinhos.data_criacao
        )

        # --------------------------------------------------
        # ORDEM
        # --------------------------------------------------

        if order.lower() == "asc":

            query = query.order_by(
                asc(coluna)
            )

        else:

            query = query.order_by(
                desc(coluna)
            )

        # --------------------------------------------------
        # PAGINAÇÃO
        # --------------------------------------------------

        query = (
            query
            .offset(skip)
            .limit(limit)
        )

        return self.session.scalars(
            query
        ).all()

    # ==================================================
    # CRIAR
    # ==================================================

    def criar(
        self,
        carrinho: Carrinhos
    ):
        try:

            self.session.add(
                carrinho
            )

            self.session.commit()

            self.session.refresh(
                carrinho
            )

            return carrinho

        except Exception:

            self.session.rollback()

            raise

    # ==================================================
    # ATUALIZAR
    # ==================================================

    def atualizar(
        self,
        carrinho: Carrinhos
    ):
        try:

            self.session.commit()

            self.session.refresh(
                carrinho
            )

            return carrinho

        except Exception:

            self.session.rollback()

            raise

    # ==================================================
    # DELETAR
    # ==================================================

    def deletar(
        self,
        carrinho: Carrinhos
    ):
        try:

            self.session.delete(
                carrinho
            )

            self.session.commit()

            return True

        except Exception:

            self.session.rollback()

            raise

    # ==================================================
    # FINALIZAR COMPRA
    # ==================================================

    def finalizar_compra(
        self,
        carrinho: Carrinhos
    ):
        """
        Executa a operação de finalização da compra.

        Responsabilidades do Repository:
        - Atualizar estoque dos produtos
        - Remover os itens do carrinho
        - Confirmar a transação
        - Desfazer a transação em caso de erro

        As validações de negócio permanecem no Service.
        """

        try:

            valor_total = 0
            quantidade_itens = 0

            # --------------------------------------------------
            # ATUALIZAR ESTOQUE E CALCULAR TOTAL
            # --------------------------------------------------

            for item in list(carrinho.itens):

                produto = item.produto

                produto.estoque -= item.quantidade

                valor_total += (
                    produto.preco *
                    item.quantidade
                )

                quantidade_itens += (
                    item.quantidade
                )

            # --------------------------------------------------
            # REMOVER ITENS DO CARRINHO
            # --------------------------------------------------

            for item in list(carrinho.itens):

                self.session.delete(
                    item
                )

            # --------------------------------------------------
            # CONFIRMAR TRANSAÇÃO
            # --------------------------------------------------

            self.session.commit()

            return {
                "mensagem":
                    "Compra finalizada com sucesso.",

                "valor_total":
                    valor_total,

                "quantidade_itens":
                    quantidade_itens
            }

        except Exception:

            self.session.rollback()

            raise

    # ==================================================
    # ROLLBACK
    # ==================================================

    def rollback(self):
        """
        Desfaz a transação atual.

        Usado pelo Service quando ocorre uma
        HTTPException durante uma operação.
        """

        self.session.rollback()