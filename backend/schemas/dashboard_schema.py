from pydantic import BaseModel, ConfigDict


class DashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuarios: int
    clientes: int
    animais: int
    agendamentos: int
    atendimentos: int
    produtos: int
    carrinhos: int
    itens_carrinho: int