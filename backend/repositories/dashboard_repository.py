from datetime import date, datetime

from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session

from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes
from backend.models.animal_model import Animais
from backend.models.agendamento_model import Agendamentos
from backend.models.atendimento_model import Atendimentos
from backend.models.produto_model import Produtos
from backend.models.carrinho_model import Carrinhos
from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.aplicacao_vacina_model import AplicacoesVacina
from backend.models.vacina_model import Vacinas


class DashboardRepository:
    """
    Responsável exclusivamente pelo acesso a dados do dashboard.
    Não contém regra de negócio nem formatação de resposta —
    isso fica a cargo do DashboardServiceImpl.
    """

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # GENÉRICO
    # ==========================================================

    def total(self, model) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(model)
        ) or 0

    # ==========================================================
    # USUÁRIOS
    # ==========================================================

    def usuarios_por_perfil(self, perfil: str) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Usuarios)
            .where(
                Usuarios.perfil == perfil
            )
        ) or 0

    # ==========================================================
    # ATENDIMENTOS
    # ==========================================================

    def atendimentos_hoje(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .where(
                func.date(Atendimentos.data_atendimento) == date.today()
            )
        ) or 0

    def atendimentos_finalizados(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .where(
                Atendimentos.status == "Finalizado"
            )
        ) or 0

    # ==========================================================
    # ANIMAIS
    # ==========================================================

    def animais_por_especie(self):

        return self.session.execute(
            select(
                Animais.especie,
                func.count(Animais.id).label("quantidade")
            )
            .group_by(Animais.especie)
        ).all()

    def animal_mais_velho(self) -> Animais | None:

        return self.session.scalar(
            select(Animais)
            .order_by(desc(Animais.idade))
            .limit(1)
        )

    def media_idade_animais(self) -> float | None:

        return self.session.scalar(
            select(func.avg(Animais.idade))
        )

    def animais_do_cliente(self, cliente_id: int) -> list[Animais]:

        return self.session.scalars(
            select(Animais)
            .where(Animais.cliente_id == cliente_id)
        ).all()

    # ==========================================================
    # CLIENTES
    # ==========================================================

    def cliente_com_mais_animais(self):

        return self.session.execute(
            select(
                Clientes.nome,
                func.count(Animais.id).label("quantidade")
            )
            .join(
                Animais,
                Animais.cliente_id == Clientes.id
            )
            .group_by(Clientes.id)
            .order_by(desc("quantidade"))
            .limit(1)
        ).first()

    def cliente_por_usuario_id(self, usuario_id: int) -> Clientes | None:

        return self.session.scalar(
            select(Clientes)
            .where(Clientes.usuario_id == usuario_id)
        )

    # ==========================================================
    # ESTOQUE / PRODUTOS
    # ==========================================================

    def valor_estoque(self) -> float:

        return self.session.scalar(
            select(
                func.sum(Produtos.preco * Produtos.estoque)
            )
        ) or 0

    def estoque_baixo(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Produtos)
            .where(Produtos.estoque <= 5)
        ) or 0

    def produtos_sem_estoque(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Produtos)
            .where(Produtos.estoque == 0)
        ) or 0

    def produto_mais_caro(self) -> Produtos | None:

        return self.session.scalar(
            select(Produtos)
            .order_by(desc(Produtos.preco))
            .limit(1)
        )

    def produto_mais_barato(self) -> Produtos | None:

        return self.session.scalar(
            select(Produtos)
            .order_by(Produtos.preco)
            .limit(1)
        )

    # ==========================================================
    # AGENDA
    # ==========================================================

    def agendamentos_hoje(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                func.date(Agendamentos.data_agendamento) == date.today()
            )
        ) or 0

    def agendamentos_futuros(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.data_agendamento >= date.today()
            )
        ) or 0

    def agendamentos_cancelados(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.status == "Cancelado"
            )
        ) or 0

    def agendamentos_semana(self):

        return self.session.execute(
            select(
                func.date(Agendamentos.data_agendamento).label("dia"),
                func.count(Agendamentos.id).label("quantidade")
            )
            .where(
                Agendamentos.data_agendamento >= date.today()
            )
            .group_by(
                func.date(Agendamentos.data_agendamento)
            )
            .order_by(
                func.date(Agendamentos.data_agendamento)
            )
        ).all()

    # ==========================================================
    # VACINAS
    # ==========================================================

    def proximas_doses(self) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(AplicacoesVacina)
            .where(
                AplicacoesVacina.proxima_dose >= date.today()
            )
        ) or 0

    def vacinas_aplicadas_veterinario(self, veterinario_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(AplicacoesVacina)
            .where(
                AplicacoesVacina.veterinario_id == veterinario_id
            )
        ) or 0

    def vacina_mais_aplicada(self):

        return self.session.execute(
            select(
                Vacinas.nome,
                func.count(AplicacoesVacina.id).label("quantidade")
            )
            .join(
                AplicacoesVacina,
                AplicacoesVacina.vacina_id == Vacinas.id
            )
            .group_by(Vacinas.id)
            .order_by(desc("quantidade"))
            .limit(1)
        ).first()

    def proximas_doses_cliente(self, cliente_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(AplicacoesVacina)
            .join(
                Animais,
                Animais.id == AplicacoesVacina.animal_id
            )
            .where(
                Animais.cliente_id == cliente_id,
                AplicacoesVacina.proxima_dose >= datetime.now()
            )
        ) or 0

    # ==========================================================
    # VETERINÁRIO
    # ==========================================================

    def consultas_hoje_veterinario(self, veterinario_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.veterinario_id == veterinario_id,
                func.date(Agendamentos.data_agendamento) == date.today()
            )
        ) or 0

    def proximas_consultas_veterinario(self, veterinario_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.veterinario_id == veterinario_id,
                Agendamentos.data_agendamento >= datetime.now()
            )
        ) or 0

    def atendimentos_realizados_veterinario(self, veterinario_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .where(
                Atendimentos.usuario_id == veterinario_id
            )
        ) or 0

    def animais_atendidos_veterinario(self, veterinario_id: int) -> int:

        return self.session.scalar(
            select(
                func.count(func.distinct(Atendimentos.animal_id))
            )
            .where(
                Atendimentos.usuario_id == veterinario_id
            )
        ) or 0

    # ==========================================================
    # CLIENTE
    # ==========================================================

    def consultas_agendadas_cliente(self, cliente_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .join(
                Animais,
                Animais.id == Agendamentos.animal_id
            )
            .where(
                Animais.cliente_id == cliente_id,
                Agendamentos.data_agendamento >= datetime.now(),
                Agendamentos.status != "Cancelado"
            )
        ) or 0

    def proxima_consulta_cliente(self, cliente_id: int):

        return self.session.execute(
            select(
                Agendamentos.data_agendamento,
                Agendamentos.descricao,
                Animais.nome.label("animal_nome")
            )
            .join(
                Animais,
                Animais.id == Agendamentos.animal_id
            )
            .where(
                Animais.cliente_id == cliente_id,
                Agendamentos.data_agendamento >= datetime.now(),
                Agendamentos.status != "Cancelado"
            )
            .order_by(Agendamentos.data_agendamento)
            .limit(1)
        ).first()

    def atendimentos_realizados_cliente(self, cliente_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .join(
                Animais,
                Animais.id == Atendimentos.animal_id
            )
            .where(
                Animais.cliente_id == cliente_id
            )
        ) or 0

    def total_carrinhos_cliente(self, cliente_id: int) -> int:

        return self.session.scalar(
            select(func.count())
            .select_from(Carrinhos)
            .where(
                Carrinhos.cliente_id == cliente_id
            )
        ) or 0

    def valor_total_compras_cliente(self, cliente_id: int) -> float:

        return self.session.scalar(
            select(
                func.coalesce(
                    func.sum(Produtos.preco * ItensCarrinho.quantidade),
                    0
                )
            )
            .select_from(ItensCarrinho)
            .join(
                Carrinhos,
                Carrinhos.id == ItensCarrinho.carrinho_id
            )
            .join(
                Produtos,
                Produtos.id == ItensCarrinho.produto_id
            )
            .where(
                Carrinhos.cliente_id == cliente_id
            )
        ) or 0