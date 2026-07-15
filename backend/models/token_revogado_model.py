from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.database import Base


class TokenRevogado(Base):
    __tablename__ = "tokens_revogados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(600), nullable=False, unique=True)
    expira_em: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    revogado_em: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),nullable=False)