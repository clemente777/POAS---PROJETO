from sqlmodel import SQLModel


class ItemCarrinhoCreate(SQLModel):
    carrinho_id: int
    produto_id: int
    quantidade: int


class ItemCarrinhoUpdate(SQLModel):
    quantidade: int | None = None


class ItemCarrinhoResponse(SQLModel):
    id: int
    carrinho_id: int
    produto_id: int
    quantidade: int