from abc import ABC, abstractmethod

class ClienteService(ABC):

    @abstractmethod
    def listar_clientes(self):
        pass

    @abstractmethod
    def buscar_cliente_por_id(self, id):
        pass

    @abstractmethod
    def criar_cliente(self, cliente):
        pass

    @abstractmethod
    def atualizar_cliente(self, id, cliente):
        pass

    @abstractmethod
    def deletar_cliente(self, id):
        pass