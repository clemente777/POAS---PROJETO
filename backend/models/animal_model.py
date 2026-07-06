from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.cliente_model import Clientes
    from backend.models.agendamento_model import Agendamentos
    from backend.models.atendimento_model import Atendimentos


class Animais(Base):
    __tablename__ = "animais"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    especie: Mapped[str] = mapped_column(String(100), nullable=False)
    raca: Mapped[str] = mapped_column(String(100), nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False
    )

    cliente: Mapped["Clientes"] = relationship(back_populates="animais")
    agendamentos: Mapped[list["Agendamentos"]] = relationship(back_populates="animal")
    atendimentos: Mapped[list["Atendimentos"]] = relationship(back_populates="animal")