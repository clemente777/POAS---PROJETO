from __future__ import annotations

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.item_carrinho_model import ItensCarrinho


class Produtos(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)

    preco: Mapped[float] = mapped_column(Float, nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    itens_carrinho: Mapped[list["ItensCarrinho"]] = relationship(
        back_populates="produto",
        lazy="selectin"
    )
    ativo: Mapped[bool] = mapped_column(
    default=True,
    nullable=False
)   