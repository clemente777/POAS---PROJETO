from abc import ABC, abstractmethod

class UsuarioService(ABC):

    @abstractmethod
    def listar_usuarios(self):
        pass

    @abstractmethod
    def buscar_usuario(self, id: int):
        pass

    @abstractmethod
    def criar_usuario(self, usuario):
        pass

    @abstractmethod
    def atualizar_usuario(self, id: int, usuario):
        pass

    @abstractmethod
    def deletar_usuario(self, id: int):
        pass