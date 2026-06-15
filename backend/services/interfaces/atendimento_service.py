from abc import ABC, abstractmethod

class AtendimentoService(ABC):

    @abstractmethod
    def listar_atendimentos(self):
        pass

    @abstractmethod
    def buscar_atendimento_por_id(self, id):
        pass

    @abstractmethod
    def criar_atendimento(self, atendimento):
        pass

    @abstractmethod
    def atualizar_atendimento(self, id, atendimento):
        pass

    @abstractmethod
    def deletar_atendimento(self, id):
        pass