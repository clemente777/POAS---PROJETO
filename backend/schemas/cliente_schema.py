from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str = Field(min_length=1, max_length=255)
    senha: str | None = Field(default=None, min_length=6)


class ClienteUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    endereco: str | None = Field(default=None, max_length=255)


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str