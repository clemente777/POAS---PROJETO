from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.animal_model import Animais
    from backend.models.usuario_model import Usuarios


class Atendimentos(Base):
    __tablename__ = "atendimentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    data_atendimento: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    diagnostico: Mapped[str] = mapped_column(String(500), nullable=False)
    observacoes: Mapped[str] = mapped_column(String(1000), default="")

    animal_id: Mapped[int] = mapped_column(
        ForeignKey("animais.id", ondelete="CASCADE"),
        nullable=False
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True
    )

    animal: Mapped["Animais"] = relationship(
    "Animais",
    back_populates="atendimentos"
)
    usuario: Mapped["Usuarios"] = relationship(back_populates="atendimentos")