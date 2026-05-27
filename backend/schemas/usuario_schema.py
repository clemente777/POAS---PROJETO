from pydantic import BaseModel
from typing import Optional, List


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None


class AnimalResponse(BaseModel):
    id: int
    nome_popular: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    animais: List[AnimalResponse] = []