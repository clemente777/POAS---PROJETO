from sqlmodel import SQLModel


class CarrinhoCreate(SQLModel):
    cliente_id: int


class CarrinhoUpdate(SQLModel):
    cliente_id: int | None = None


class CarrinhoResponse(SQLModel):
    id: int
    cliente_id: int