from pydantic import BaseModel, EmailStr, ConfigDict


# CREATE
class CarrinhoCreate(BaseModel):
    cliente_id: int


# UPDATE
class CarrinhoUpdate(BaseModel):
    cliente_id: int | None = None


# RESPONSE
class CarrinhoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int


class CompraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mensagem: str
    valor_total: float
    quantidade_itens: int