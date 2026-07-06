from pydantic import BaseModel, EmailStr


# =========================
# CREATE
# =========================
class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str


# =========================
# UPDATE
# =========================
class ClienteUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None
    endereco: str | None = None


# =========================
# RESPONSE
# =========================
class ClienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    endereco: str