from pydantic import BaseModel


# =========================
# CREATE
# =========================
class CarrinhoCreate(BaseModel):
    cliente_id: int


# =========================
# UPDATE
# =========================
class CarrinhoUpdate(BaseModel):
    cliente_id: int | None = None


# =========================
# RESPONSE
# =========================
class CarrinhoResponse(BaseModel):
    id: int
    cliente_id: int