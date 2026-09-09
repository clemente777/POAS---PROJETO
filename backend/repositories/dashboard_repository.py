from datetime import datetime, date, timedelta

from sqlalchemy import (
    select,
    func,
    desc,
    asc
)
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
    Repository responsável exclusivamente pelas consultas
    utilizadas pelo Dashboard.

    O Service não realiza consultas diretamente no banco.

    Responsabilidades deste Repository:
    - Contagens
    - Estatísticas
    - Filtros
    - Consultas de agenda
    - Consultas de atendimentos
    - Consultas de vacinas
    - Consultas específicas do veterinário
    - Consultas específicas do cliente
    """

    def __init__(self, session: Session):
        self.session = session

    # ==================================================
    # MÉTODOS GERAIS
    # ==================================================

    def total(self, modelo):
        """
        Retorna a quantidade total de registros
        de um determinado modelo.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(modelo)
        ) or 0

    # ==================================================
    # USUÁRIOS POR PERFIL
    # ==================================================

    def usuarios_por_perfil(self, perfil: str):
        """
        Retorna a quantidade de usuários de determinado perfil.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Usuarios)
            .where(
                Usuarios.perfil == perfil
            )
        ) or 0

    # ==================================================
    # ANIMAIS POR ESPÉCIE
    # ==================================================

    def animais_por_especie(self):
        """
        Retorna a quantidade de animais agrupada por espécie.

        Resultado:
        - especie
        - quantidade
        """

        return self.session.execute(
            select(
                Animais.especie.label("especie"),
                func.count(
                    Animais.id
                ).label("quantidade")
            )
            .group_by(
                Animais.especie
            )
            .order_by(
                asc(Animais.especie)
            )
        ).all()

    # ==================================================
    # ANIMAL MAIS VELHO
    # ==================================================

    def animal_mais_velho(self):
        """
        Retorna o animal com maior idade.
        """

        return self.session.scalar(
            select(Animais)
            .order_by(
                desc(Animais.idade)
            )
            .limit(1)
        )

    # ==================================================
    # MÉDIA DE IDADE DOS ANIMAIS
    # ==================================================

    def media_idade_animais(self):
        """
        Retorna a média da idade dos animais.
        """

        return self.session.scalar(
            select(
                func.avg(Animais.idade)
            )
        ) or 0

    # ==================================================
    # CLIENTE COM MAIS ANIMAIS
    # ==================================================

    def cliente_com_mais_animais(self):
        """
        Retorna o cliente que possui a maior quantidade
        de animais.

        Resultado:
        - nome
        - quantidade
        """

        resultado = self.session.execute(
            select(
                Clientes.nome.label("nome"),
                func.count(
                    Animais.id
                ).label("quantidade")
            )
            .join(
                Animais,
                Animais.cliente_id == Clientes.id
            )
            .group_by(
                Clientes.id,
                Clientes.nome
            )
            .order_by(
                desc(
                    func.count(Animais.id)
                )
            )
            .limit(1)
        ).first()

        return resultado

    # ==================================================
    # AGENDAMENTOS DA SEMANA
    # ==================================================

    def agendamentos_semana(self):
        """
        Retorna a quantidade de agendamentos por dia
        da semana atual.

        Resultado:
        - dia
        - quantidade
        """

        hoje = date.today()

        inicio_semana = hoje - timedelta(
            days=hoje.weekday()
        )

        fim_semana = inicio_semana + timedelta(
            days=6
        )

        resultado = self.session.execute(
            select(
                func.date(
                    Agendamentos.data_agendamento
                ).label("dia"),
                func.count(
                    Agendamentos.id
                ).label("quantidade")
            )
            .where(
                func.date(
                    Agendamentos.data_agendamento
                ).between(
                    inicio_semana,
                    fim_semana
                )
            )
            .group_by(
                func.date(
                    Agendamentos.data_agendamento
                )
            )
            .order_by(
                asc(
                    func.date(
                        Agendamentos.data_agendamento
                    )
                )
            )
        ).all()

        return resultado

    # ==================================================
    # PRÓXIMAS DOSES
    # ==================================================

    def proximas_doses(self):
        """
        Retorna a quantidade de próximas doses
        de vacinas cadastradas.
        """

        agora = datetime.now()

        return self.session.scalar(
            select(func.count())
            .select_from(AplicacoesVacina)
            .where(
                AplicacoesVacina.proxima_dose.is_not(None),
                AplicacoesVacina.proxima_dose >= agora
            )
        ) or 0

    # ==================================================
    # VALOR TOTAL DO ESTOQUE
    # ==================================================

    def valor_estoque(self):
        """
        Calcula o valor total do estoque.

        Fórmula:
        preço × quantidade em estoque
        """

        valor = self.session.scalar(
            select(
                func.sum(
                    Produtos.preco *
                    Produtos.estoque
                )
            )
        )

        return valor or 0

    # ==================================================
    # ESTOQUE BAIXO
    # ==================================================

    def estoque_baixo(self):
        """
        Retorna a quantidade de produtos considerados
        com estoque baixo.

        Considera estoque maior que 0 e menor ou igual a 5.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Produtos)
            .where(
                Produtos.estoque > 0,
                Produtos.estoque <= 5
            )
        ) or 0

    # ==================================================
    # PRODUTOS SEM ESTOQUE
    # ==================================================

    def produtos_sem_estoque(self):
        """
        Retorna a quantidade de produtos sem estoque.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Produtos)
            .where(
                Produtos.estoque <= 0
            )
        ) or 0

    # ==================================================
    # PRODUTO MAIS CARO
    # ==================================================

    def produto_mais_caro(self):
        """
        Retorna o produto com maior preço.
        """

        return self.session.scalar(
            select(Produtos)
            .order_by(
                desc(Produtos.preco)
            )
            .limit(1)
        )

    # ==================================================
    # PRODUTO MAIS BARATO
    # ==================================================

    def produto_mais_barato(self):
        """
        Retorna o produto com menor preço.
        """

        return self.session.scalar(
            select(Produtos)
            .order_by(
                asc(Produtos.preco)
            )
            .limit(1)
        )

    # ==================================================
    # AGENDAMENTOS DE HOJE
    # ==================================================

    def agendamentos_hoje(self):
        """
        Retorna a quantidade de agendamentos para hoje.
        """

        hoje = date.today()

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                func.date(
                    Agendamentos.data_agendamento
                ) == hoje
            )
        ) or 0

    # ==================================================
    # AGENDAMENTOS FUTUROS
    # ==================================================

    def agendamentos_futuros(self):
        """
        Retorna a quantidade de agendamentos futuros.
        """

        agora = datetime.now()

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.data_agendamento > agora
            )
        ) or 0

    # ==================================================
    # AGENDAMENTOS CANCELADOS
    # ==================================================

    def agendamentos_cancelados(self):
        """
        Retorna a quantidade de agendamentos cancelados.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.status == "Cancelado"
            )
        ) or 0

    # ==================================================
    # ATENDIMENTOS DE HOJE
    # ==================================================

    def atendimentos_hoje(self):
        """
        Retorna a quantidade de atendimentos realizados hoje.

        O modelo Atendimentos utiliza o campo:
        data_atendimento
        """

        hoje = date.today()

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .where(
                func.date(
                    Atendimentos.data_atendimento
                ) == hoje
            )
        ) or 0

    # ==================================================
    # ATENDIMENTOS FINALIZADOS
    # ==================================================

    def atendimentos_finalizados(self):
        """
        Retorna a quantidade de atendimentos finalizados.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .where(
                Atendimentos.status == "Finalizado"
            )
        ) or 0

    # ==================================================
    # VACINA MAIS APLICADA
    # ==================================================

    def vacina_mais_aplicada(self):
        """
        Retorna a vacina que possui mais aplicações.

        Resultado:
        - nome
        - quantidade
        """

        return self.session.execute(
            select(
                Vacinas.nome.label("nome"),
                func.count(
                    AplicacoesVacina.id
                ).label("quantidade")
            )
            .join(
                AplicacoesVacina,
                AplicacoesVacina.vacina_id == Vacinas.id
            )
            .group_by(
                Vacinas.id,
                Vacinas.nome
            )
            .order_by(
                desc(
                    func.count(
                        AplicacoesVacina.id
                    )
                )
            )
            .limit(1)
        ).first()

    # ==================================================
    # DASHBOARD VETERINÁRIO
    # ==================================================

    def consultas_hoje_veterinario(
        self,
        veterinario_id: int
    ):
        """
        Quantidade de consultas do veterinário para hoje.
        """

        hoje = date.today()

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.veterinario_id == veterinario_id,
                func.date(
                    Agendamentos.data_agendamento
                ) == hoje
            )
        ) or 0

    # ==================================================

    def proximas_consultas_veterinario(
        self,
        veterinario_id: int
    ):
        """
        Retorna a quantidade de próximas consultas
        do veterinário.
        """

        agora = datetime.now()

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.veterinario_id == veterinario_id,
                Agendamentos.data_agendamento > agora
            )
        ) or 0

    # ==================================================

    def atendimentos_realizados_veterinario(
        self,
        veterinario_id: int
    ):
        """
        Retorna a quantidade de atendimentos realizados
        pelo veterinário.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .where(
                Atendimentos.usuario_id == veterinario_id,
                Atendimentos.status == "Finalizado"
            )
        ) or 0

    # ==================================================

    def animais_atendidos_veterinario(
        self,
        veterinario_id: int
    ):
        """
        Retorna a quantidade de animais distintos
        atendidos pelo veterinário.
        """

        return self.session.scalar(
            select(
                func.count(
                    func.distinct(
                        Atendimentos.animal_id
                    )
                )
            )
            .select_from(Atendimentos)
            .where(
                Atendimentos.usuario_id == veterinario_id
            )
        ) or 0

    # ==================================================

    def vacinas_aplicadas_veterinario(
        self,
        veterinario_id: int
    ):
        """
        Retorna a quantidade de vacinas aplicadas
        pelo veterinário.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(AplicacoesVacina)
            .where(
                AplicacoesVacina.veterinario_id
                == veterinario_id
            )
        ) or 0

    # ==================================================
    # DASHBOARD CLIENTE
    # ==================================================

    def cliente_por_usuario_id(
        self,
        usuario_id: int
    ):
        """
        Busca o cliente associado ao usuário logado.
        """

        return self.session.scalar(
            select(Clientes)
            .where(
                Clientes.usuario_id == usuario_id
            )
        )

    # ==================================================

    def animais_do_cliente(
        self,
        cliente_id: int
    ):
        """
        Retorna todos os animais pertencentes ao cliente.
        """

        return self.session.scalars(
            select(Animais)
            .where(
                Animais.cliente_id == cliente_id
            )
            .order_by(
                asc(Animais.nome)
            )
        ).all()

    # ==================================================

    def consultas_agendadas_cliente(
        self,
        cliente_id: int
    ):
        """
        Retorna a quantidade de consultas futuras
        do cliente.
        """

        agora = datetime.now()

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .join(
                Animais,
                Agendamentos.animal_id == Animais.id
            )
            .where(
                Animais.cliente_id == cliente_id,
                Agendamentos.data_agendamento > agora,
                Agendamentos.status != "Cancelado"
            )
        ) or 0

    # ==================================================

    def proxima_consulta_cliente(
        self,
        cliente_id: int
    ):
        """
        Retorna a próxima consulta do cliente.

        O resultado possui:
        - data_agendamento
        - descricao
        - animal_nome
        """

        agora = datetime.now()

        resultado = self.session.execute(
            select(
                Agendamentos.data_agendamento,
                Agendamentos.descricao,
                Animais.nome.label("animal_nome")
            )
            .join(
                Animais,
                Agendamentos.animal_id == Animais.id
            )
            .where(
                Animais.cliente_id == cliente_id,
                Agendamentos.data_agendamento > agora,
                Agendamentos.status != "Cancelado"
            )
            .order_by(
                asc(
                    Agendamentos.data_agendamento
                )
            )
            .limit(1)
        ).first()

        return resultado

    # ==================================================

    def atendimentos_realizados_cliente(
        self,
        cliente_id: int
    ):
        """
        Retorna a quantidade de atendimentos realizados
        nos animais do cliente.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Atendimentos)
            .join(
                Animais,
                Atendimentos.animal_id == Animais.id
            )
            .where(
                Animais.cliente_id == cliente_id,
                Atendimentos.status == "Finalizado"
            )
        ) or 0

    # ==================================================

    def total_carrinhos_cliente(
        self,
        cliente_id: int
    ):
        """
        Retorna a quantidade de carrinhos/compras
        do cliente.
        """

        return self.session.scalar(
            select(func.count())
            .select_from(Carrinhos)
            .where(
                Carrinhos.cliente_id == cliente_id
            )
        ) or 0

    # ==================================================

    def valor_total_compras_cliente(
        self,
        cliente_id: int
    ):
        """
        Calcula o valor total das compras do cliente.

        Soma:
        preço do produto × quantidade.
        """

        resultado = self.session.scalar(
            select(
                func.sum(
                    Produtos.preco *
                    ItensCarrinho.quantidade
                )
            )
            .select_from(ItensCarrinho)
            .join(
                Produtos,
                ItensCarrinho.produto_id == Produtos.id
            )
            .join(
                Carrinhos,
                ItensCarrinho.carrinho_id == Carrinhos.id
            )
            .where(
                Carrinhos.cliente_id == cliente_id
            )
        )

        return resultado or 0

    # ==================================================

    def proximas_doses_cliente(
        self,
        cliente_id: int
    ):
        """
        Retorna a quantidade de próximas doses de vacina
        dos animais pertencentes ao cliente.
        """

        agora = datetime.now()

        return self.session.scalar(
            select(func.count())
            .select_from(AplicacoesVacina)
            .join(
                Animais,
                AplicacoesVacina.animal_id == Animais.id
            )
            .where(
                Animais.cliente_id == cliente_id,
                AplicacoesVacina.proxima_dose.is_not(None),
                AplicacoesVacina.proxima_dose >= agora
            )
        ) or 0

