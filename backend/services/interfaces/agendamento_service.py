from abc import ABC, abstractmethod

class AgendamentoService(ABC):

    @abstractmethod
    def listar_agendamentos(self):
        pass

    @abstractmethod
    def buscar_agendamento_por_id(self, id):
        pass

    @abstractmethod
    def criar_agendamento(self, agendamento):
        pass

    @abstractmethod
    def atualizar_agendamento(self, id, agendamento):
        pass

    @abstractmethod
    def deletar_agendamento(self, id):
        pass