from typing import Optional, List, Dict, Any

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

        model_config = ConfigDict(
            from_attributes=True
        )


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

        vacina_mais_aplicada: Optional[VacinaDashboard]



        # ==========================
        # ESTOQUE
        # ==========================

        valor_total_estoque: float

        estoque_baixo: int

        produtos_sem_estoque: int



        # ==========================
        # PRODUTOS
        # ==========================

        produto_mais_caro: Optional[ProdutoDashboard]

        produto_mais_barato: Optional[ProdutoDashboard]



        # ==========================
        # ANIMAIS
        # ==========================

        animal_mais_velho: Optional[AnimalDashboard]

        media_idade_animais: float

        animais_por_especie: Dict[str, int]



        # ==========================
        # CLIENTES
        # ==========================

        cliente_com_mais_animais: Optional[ClienteAnimaisDashboard]



        # ==========================
        # AGENDA
        # ==========================

        agendamentos_hoje: int

        agendamentos_futuros: int

        agendamentos_cancelados: int

        agendamentos_semana: List[Dict[str, Any]]



        # ==========================
        # ATENDIMENTOS
        # ==========================


        atendimentos_hoje: int

        atendimentos_finalizados: int
        
from pydantic import BaseModel


class DashboardVeterinarioResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    # compartilhados
    animais: int

    clientes: int

    agendamentos: int

    vacinas: int

    aplicacoes_vacina: int

    animais_por_especie: Dict[str, int]

    animal_mais_velho: Optional[AnimalDashboard]

    media_idade_animais: float

    cliente_com_mais_animais: Optional[ClienteAnimaisDashboard]

    agendamentos_semana: List[Dict[str, Any]]

    # exclusivos do veterinário
    consultas_hoje: int

    proximas_consultas: int

    atendimentos_realizados: int

    animais_atendidos: int

    vacinas_aplicadas: int

    proximas_doses: int