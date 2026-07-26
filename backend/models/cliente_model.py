from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.models.animal_model import Animais
    from backend.models.carrinho_model import Carrinhos
    from backend.models.usuario_model import Usuarios



class Clientes(Base):

    __tablename__ = "clientes"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )


    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
        unique=True
    )


    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    cpf: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        index=True,
        nullable=False
    )


    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )


    endereco: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )



    # RELAÇÃO COM USUÁRIO

    usuario: Mapped["Usuarios"] = relationship(
        back_populates="cliente"
    )



    animais: Mapped[list["Animais"]] = relationship(
        back_populates="cliente",
        lazy="selectin",
        cascade="save-update, merge"
    )


    carrinhos: Mapped[list["Carrinhos"]] = relationship(
        back_populates="cliente",
        lazy="selectin"
    )