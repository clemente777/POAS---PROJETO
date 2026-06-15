from backend.models.models import Agendamentos
from backend.services.interfaces.agendamento_service import AgendamentoService

class AgendamentoServiceImpl(AgendamentoService):

    def __init__(self, session):
        self.session = session

    def listar_agendamentos(self):
        return self.session.query(
            Agendamentos
        ).all()

    def buscar_agendamento_por_id(self, id):
        return self.session.query(
            Agendamentos
        ).get(id)

    def criar_agendamento(self, agendamento):
        self.session.add(agendamento)
        self.session.commit()
        self.session.refresh(agendamento)
        return agendamento

    def atualizar_agendamento(self, id, agendamento):

        self.session.query(
            Agendamentos
        ).filter(
            Agendamentos.id == id
        ).update(
            agendamento.model_dump()
        )

        self.session.commit()

        return agendamento

    def deletar_agendamento(self, id):

        agendamento = self.session.query(
            Agendamentos
        ).get(id)

        if not agendamento:
            return False

        self.session.delete(agendamento)
        self.session.commit()

        return True