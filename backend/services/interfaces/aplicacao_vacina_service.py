from abc import ABC, abstractmethod


class AplicacaoVacinaService(ABC):


    @abstractmethod
    def listar(self):
        pass


    @abstractmethod
    def buscar_por_id(self, aplicacao_id: int):
        pass


    @abstractmethod
    def aplicar_vacina(self, dados, veterinario_id: int):
        pass


    @abstractmethod
    def atualizar(self, aplicacao_id: int, dados):
        pass


    @abstractmethod
    def deletar(self, aplicacao_id: int):
        pass