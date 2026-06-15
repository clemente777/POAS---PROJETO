from backend.models.models import Atendimentos
from backend.services.interfaces.atendimento_service import (
    AtendimentoService
)


class AtendimentoServiceImpl(
    AtendimentoService
):

    def __init__(self, session):
        self.session = session

    def listar_atendimentos(self):
        return self.session.query(
            Atendimentos
        ).all()

    def buscar_atendimento_por_id(
        self,
        id
    ):
        return self.session.query(
            Atendimentos
        ).get(id)

    def criar_atendimento(
        self,
        atendimento
    ):
        self.session.add(atendimento)
        self.session.commit()
        self.session.refresh(atendimento)

        return atendimento

    def atualizar_atendimento(
        self,
        id,
        atendimento
    ):

        atendimento_db = self.session.query(
            Atendimentos
        ).get(id)

        if not atendimento_db:
            return None

        self.session.query(
            Atendimentos
        ).filter(
            Atendimentos.id == id
        ).update(
            atendimento.model_dump()
        )

        self.session.commit()

        return atendimento

    def deletar_atendimento(
        self,
        id
    ):

        atendimento = self.session.query(
            Atendimentos
        ).get(id)

        if not atendimento:
            return False

        self.session.delete(atendimento)
        self.session.commit()

        return True