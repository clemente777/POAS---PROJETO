from abc import ABC, abstractmethod

class ProdutoService(ABC):

    @abstractmethod
    def listar_produtos(self):
        pass

    @abstractmethod
    def buscar_produto_por_id(self, id):
        pass

    @abstractmethod
    def criar_produto(self, produto):
        pass

    @abstractmethod
    def atualizar_produto(self, id, produto):
        pass

    @abstractmethod
    def deletar_produto(self, id):
        pass