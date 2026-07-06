from __future__ import annotations

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.carrinho_model import Carrinhos
    from backend.models.produto_model import Produtos


class ItensCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantidade: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    carrinho_id: Mapped[int] = mapped_column(
        ForeignKey("carrinhos.id", ondelete="CASCADE"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id", ondelete="RESTRICT"),
        nullable=False
    )

    carrinho: Mapped["Carrinhos"] = relationship(back_populates="itens")
    produto: Mapped["Produtos"] = relationship(back_populates="itens_carrinho")