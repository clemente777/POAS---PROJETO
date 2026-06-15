from pydantic import EmailStr
from sqlmodel import SQLModel


class ClienteCreate(SQLModel):
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str


class ClienteUpdate(SQLModel):
    nome: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    endereco: str | None = None


class ClienteResponse(SQLModel):
    id: int
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str   