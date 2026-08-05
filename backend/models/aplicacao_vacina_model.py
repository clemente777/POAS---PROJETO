from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.database.database import Base


if TYPE_CHECKING:

    from backend.models.animal_model import Animais
    from backend.models.vacina_model import Vacinas
    from backend.models.usuario_model import Usuarios



class AplicacoesVacina(Base):

    __tablename__ = "aplicacoes_vacina"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )


    animal_id: Mapped[int] = mapped_column(
        ForeignKey("animais.id"),
        nullable=False
    )


    vacina_id: Mapped[int] = mapped_column(
        ForeignKey("vacinas.id"),
        nullable=False
    )


    veterinario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )


    data_aplicacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )


    proxima_dose: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


    lote: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )


    observacoes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )


    animal: Mapped["Animais"] = relationship(
        "Animais",
        back_populates="aplicacoes_vacina"
    )


    vacina: Mapped["Vacinas"] = relationship(
        "Vacinas",
        back_populates="aplicacoes_vacina"
    )


    veterinario: Mapped["Usuarios"] = relationship(
        "Usuarios",
        back_populates="aplicacoes_vacina"
    )