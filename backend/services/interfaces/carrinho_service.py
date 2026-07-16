from abc import ABC, abstractmethod


class CarrinhoService(ABC):

    @abstractmethod
    def listar_carrinhos(self):
        pass


    @abstractmethod
    def criar_carrinho(self, carrinho):
        pass


    @abstractmethod
    def deletar_carrinho(self, id):
        pass


    @abstractmethod
    def finalizar_compra(self, id):
        pass