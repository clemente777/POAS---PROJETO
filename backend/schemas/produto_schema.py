from pydantic import BaseModel, ConfigDict


# CREATE
class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    estoque: int


# UPDATE
class ProdutoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    estoque: int | None = None


# RESPONSE
class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int
from pydantic import BaseModel, EmailStr, ConfigDict


# CREATE
class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str


# UPDATE
class ClienteUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    endereco: str | None = None


# RESPONSE
class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str