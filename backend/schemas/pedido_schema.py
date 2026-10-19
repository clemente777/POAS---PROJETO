from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemPedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int | None
    nome_produto: str
    preco_unitario: float
    quantidade: int


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    data_compra: datetime
    valor_total: float
    itens: list[ItemPedidoResponse]
