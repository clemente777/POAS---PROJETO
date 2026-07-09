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