from sqlmodel import SQLModel


class ProdutoCreate(SQLModel):
    nome: str
    descricao: str
    preco: float
    estoque: int


class ProdutoUpdate(SQLModel):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    estoque: int | None = None


class ProdutoResponse(SQLModel):
    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int