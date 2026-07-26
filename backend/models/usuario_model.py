from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.atendimento_model import Atendimentos
    from backend.models.cliente_model import Clientes

class Usuarios(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    perfil: Mapped[str] = mapped_column(String(30), default="Cliente", nullable=False)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    atendimentos: Mapped[list["Atendimentos"]] = relationship(
        back_populates="usuario",
        lazy="selectin"
    )
    cliente: Mapped["Clientes"] = relationship(
    back_populates="usuario",
    uselist=False
)
    