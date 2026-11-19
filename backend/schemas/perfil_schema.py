from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PerfilUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = None

    # Campos exclusivos do perfil Cliente
    cpf: str | None = None
    telefone: str | None = None
    endereco: str | None = Field(default=None, max_length=255)


class SenhaUpdate(BaseModel):
    senha_atual: str = Field(min_length=1)
    nova_senha: str = Field(min_length=6)


class PerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: str

    cliente_id: int | None = None
    cpf: str | None = None
    telefone: str | None = None
    endereco: str | None = None
