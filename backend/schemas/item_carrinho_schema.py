from pydantic import BaseModel


# =========================
# CREATE
# =========================
class ItemCarrinhoCreate(BaseModel):
    carrinho_id: int
    produto_id: int
    quantidade: int


# =========================
# UPDATE
# =========================
class ItemCarrinhoUpdate(BaseModel):
    quantidade: int | None = None


# =========================
# RESPONSE
# =========================
class ItemCarrinhoResponse(BaseModel):
    id: int
    carrinho_id: int
    produto_id: int
    quantidade: int