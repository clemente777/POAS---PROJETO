from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel,Field

class Usuarios(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, nullable=False, unique=True)
    senha_hash: str = Field(default=None, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.now)

