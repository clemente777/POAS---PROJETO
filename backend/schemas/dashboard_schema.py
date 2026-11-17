from typing import Any

from pydantic import BaseModel, ConfigDict


class ProdutoDashboard(BaseModel):
    nome: str
    preco: float


class AnimalDashboard(BaseModel):
    nome: str
    idade: int


class ClienteAnimaisDashboard(BaseModel):
    nome: str
    quantidade: int


class VacinaDashboard(BaseModel):
    nome: str
    quantidade: int


class DashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # ==========================
    # USUÁRIOS
    # ==========================

    usuarios: int

    administradores: int

    veterinarios: int

    clientes_sistema: int

    # ==========================
    # CADASTROS
    # ==========================

    clientes: int

    animais: int

    agendamentos: int

    atendimentos: int

    produtos: int

    carrinhos: int

    itens_carrinho: int

    # ==========================
    # VACINAS
    # ==========================

    vacinas: int

    aplicacoes_vacina: int

    proximas_doses: int

    vacina_mais_aplicada: VacinaDashboard | None

    # ==========================
    # ESTOQUE
    # ==========================

    valor_total_estoque: float

    estoque_baixo: int

    produtos_sem_estoque: int

    # ==========================
    # PRODUTOS
    # ==========================

    produto_mais_caro: ProdutoDashboard | None

    produto_mais_barato: ProdutoDashboard | None

    # ==========================
    # ANIMAIS
    # ==========================

    animal_mais_velho: AnimalDashboard | None

    media_idade_animais: float

    animais_por_especie: dict[str, int]

    # ==========================
    # CLIENTES
    # ==========================

    cliente_com_mais_animais: ClienteAnimaisDashboard | None

    # ==========================
    # AGENDA
    # ==========================

    agendamentos_hoje: int

    agendamentos_futuros: int

    agendamentos_cancelados: int

    agendamentos_semana: list[dict[str, Any]]

    # ==========================
    # ATENDIMENTOS
    # ==========================

    atendimentos_hoje: int

    atendimentos_finalizados: int


from pydantic import BaseModel


class DashboardVeterinarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # compartilhados
    animais: int

    clientes: int

    agendamentos: int

    vacinas: int

    aplicacoes_vacina: int

    animais_por_especie: dict[str, int]

    animal_mais_velho: AnimalDashboard | None

    media_idade_animais: float

    cliente_com_mais_animais: ClienteAnimaisDashboard | None

    agendamentos_semana: list[dict[str, Any]]

    # exclusivos do veterinário
    consultas_hoje: int

    proximas_consultas: int

    atendimentos_realizados: int

    animais_atendidos: int

    vacinas_aplicadas: int

    proximas_doses: int


class ProximaConsultaDashboard(BaseModel):
    data: str
    descricao: str
    animal: str


class DashboardClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meus_animais: list[AnimalDashboard]

    total_animais: int

    consultas_agendadas: int

    proxima_consulta: ProximaConsultaDashboard | None

    consultas_realizadas: int

    compras: int

    valor_total_compras: float

    proximas_doses_vacina: int
