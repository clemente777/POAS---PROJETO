from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.models.animal_model import Animais
    from backend.models.usuario_model import Usuarios



class Agendamentos(Base):

    __tablename__ = "agendamentos"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )


    data_agendamento: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )


    descricao: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Pendente"
    )


    animal_id: Mapped[int] = mapped_column(
        ForeignKey(
            "animais.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    veterinario_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "usuarios.id"
        ),
        nullable=True
    )


    animal: Mapped["Animais"] = relationship(
        "Animais",
        back_populates="agendamentos"
    )


    veterinario: Mapped["Usuarios"] = relationship(
        "Usuarios",
        foreign_keys="Agendamentos.veterinario_id"
    )