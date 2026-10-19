from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from backend.models.cliente_model import Clientes
from backend.models.pedido_model import Pedidos


class PedidoRepository:
    """
    Acesso a dados das compras (pedidos).

    Esta camada só conversa com o banco:
    nenhuma regra de negócio ou de permissão fica aqui.
    """

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # CLIENTE
    # ==========================================================

    def buscar_cliente_por_usuario_id(
        self,
        usuario_id: int
    ) -> Clientes | None:

        return self.session.scalar(
            select(Clientes)
            .where(
                Clientes.usuario_id == usuario_id
            )
        )

    # ==========================================================
    # PEDIDO
    # ==========================================================

    def buscar_por_id(
        self,
        pedido_id: int
    ) -> Pedidos | None:

        return self.session.scalar(
            select(Pedidos)
            .where(
                Pedidos.id == pedido_id
            )
        )

    def listar(
        self,
        skip: int = 0,
        limite: int = 10,
        cliente_id: int | None = None
    ) -> list[Pedidos]:

        query = select(Pedidos)

        # Filtro por cliente
        if cliente_id is not None:

            query = query.where(
                Pedidos.cliente_id == cliente_id
            )

        # Mais recentes primeiro
        query = (
            query
            .order_by(
                desc(Pedidos.data_compra),
                desc(Pedidos.id)
            )
            .offset(skip)
            .limit(limite)
        )

        return self.session.scalars(
            query
        ).all()

    # ==========================================================
    # PERSISTÊNCIA
    # ==========================================================

    def adicionar(
        self,
        pedido: Pedidos
    ) -> Pedidos:
        """
        Adiciona o pedido à sessão e faz flush
        (para o id ficar disponível), SEM commit.

        Quem finaliza a compra (CarrinhoServiceImpl)
        controla a transação: baixa de estoque,
        registro do pedido e limpeza do carrinho
        são confirmados juntos, ou nenhum deles.
        """

        self.session.add(pedido)
        self.session.flush()

        return pedido
