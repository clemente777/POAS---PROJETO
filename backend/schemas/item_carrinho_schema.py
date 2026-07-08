from pydantic import BaseModel, ConfigDict



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
    model_config = ConfigDict(from_attributes=True)

    id: int
    carrinho_id: int
    produto_id: int
    quantidade: int