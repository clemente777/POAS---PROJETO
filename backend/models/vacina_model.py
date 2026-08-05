from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


if TYPE_CHECKING:

    from backend.models.aplicacao_vacina_model import AplicacoesVacina



class Vacinas(Base):

    __tablename__ = "vacinas"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )


    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )


    fabricante: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    quantidade_doses: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    intervalo_dias: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    descricao: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True
    )


    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


    aplicacoes_vacina: Mapped[list["AplicacoesVacina"]] = relationship(

        "AplicacoesVacina",

        back_populates="vacina",

        lazy="selectin"

    )