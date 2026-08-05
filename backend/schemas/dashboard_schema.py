from typing import Optional

from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class ProdutoDashboard(BaseModel):
    nome: str
    preco: float


class AnimalDashboard(BaseModel):
    nome: str
    idade: int


class ClienteAnimaisDashboard(BaseModel):
    nome: str
    quantidade: int



class DashboardResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    usuarios: int

    administradores: int
    veterinarios: int
    clientes_sistema: int

    clientes: int
    animais: int
    agendamentos: int
    atendimentos: int
    produtos: int
    carrinhos: int
    itens_carrinho: int

    valor_total_estoque: float

    estoque_baixo: int

    produtos_sem_estoque: int

    produto_mais_caro: Optional[ProdutoDashboard]

    produto_mais_barato: Optional[ProdutoDashboard]

    animal_mais_velho: Optional[AnimalDashboard]

    media_idade_animais: float

    animais_por_especie: Dict[str, int]
    
    cliente_com_mais_animais: Optional[ClienteAnimaisDashboard]

    agendamentos_hoje: int

    agendamentos_futuros: int
    
    agendamentos_semana: List[Dict[str, Any]]
