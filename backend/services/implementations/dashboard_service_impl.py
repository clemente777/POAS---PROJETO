from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes
from backend.models.animal_model import Animais
from backend.models.agendamento_model import Agendamentos
from backend.models.atendimento_model import Atendimentos
from backend.models.produto_model import Produtos
from backend.models.carrinho_model import Carrinhos
from backend.models.item_carrinho_model import ItensCarrinho


class DashboardServiceImpl:

    def __init__(self, session: Session):
        self.session = session


    def dashboard(self):
        """
        Retorna os principais dados
        do sistema para o dashboard.
        """

        return {
            "usuarios": self.session.scalar(
                select(func.count())
                .select_from(Usuarios)
            ),

            "clientes": self.session.scalar(
                select(func.count())
                .select_from(Clientes)
            ),

            "animais": self.session.scalar(
                select(func.count())
                .select_from(Animais)
            ),

            "agendamentos": self.session.scalar(
                select(func.count())
                .select_from(Agendamentos)
            ),

            "atendimentos": self.session.scalar(
                select(func.count())
                .select_from(Atendimentos)
            ),

            "produtos": self.session.scalar(
                select(func.count())
                .select_from(Produtos)
            ),

            "carrinhos": self.session.scalar(
                select(func.count())
                .select_from(Carrinhos)
            ),

            "itens_carrinho": self.session.scalar(
                select(func.count())
                .select_from(ItensCarrinho)
            )
        }