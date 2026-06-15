from abc import ABC, abstractmethod


class ItemCarrinhoService(ABC):

    @abstractmethod
    def listar_itens(self):
        pass

    @abstractmethod
    def adicionar_item(self, item):
        pass

    @abstractmethod
    def remover_item(self, id):
        pass