from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.cliente_model import Clientes
    from backend.models.item_carrinho_model import ItensCarrinho


class Carrinhos(Base):
    __tablename__ = "carrinhos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False
    )

    cliente: Mapped["Clientes"] = relationship(back_populates="carrinhos")

    itens: Mapped[list["ItensCarrinho"]] = relationship(back_populates="carrinho")