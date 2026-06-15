from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel


class UsuarioCreate(SQLModel):
    nome: str
    email: EmailStr
    senha_hash: str


class UsuarioUpdate(SQLModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha_hash: str | None = None


class UsuarioResponse(SQLModel):
    id: int
    nome: str
    email: EmailStr
    criado_em: datetime