from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Pedidos(Base):
    """
    Compra finalizada. Guarda o histórico que o carrinho
    não mantém (o carrinho é esvaziado ao finalizar).
    """

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    data_compra: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    valor_total: Mapped[float] = mapped_column(Float, nullable=False)

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False
    )

    cliente = relationship("Clientes")

    itens: Mapped[list["ItensPedido"]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class ItensPedido(Base):
    """
    Item de uma compra. Nome e preço são copiados no momento
    da compra, então o histórico não muda se o produto for
    editado ou removido depois.
    """

    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False
    )

    produto_id: Mapped[int | None] = mapped_column(
        ForeignKey("produtos.id", ondelete="SET NULL"),
        nullable=True
    )

    nome_produto: Mapped[str] = mapped_column(String(100), nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)

    pedido: Mapped["Pedidos"] = relationship(back_populates="itens")
