from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UsuarioCreate(BaseModel):

    nome: str

    email: EmailStr

    senha: str



class UsuarioAdminCreate(BaseModel):

    nome: str

    email: EmailStr

    senha: str

    perfil: str



class UsuarioUpdate(BaseModel):

    nome: str | None = None

    email: EmailStr | None = None

    senha: str | None = None



class UsuarioResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    nome: str

    email: EmailStr

    perfil: str

    criado_em: datetime