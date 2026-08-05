from abc import ABC, abstractmethod

from backend.schemas.vacina_schema import (
    VacinaCreate,
    VacinaUpdate
)


class VacinaService(ABC):

    @abstractmethod
    def listar(self):
        pass


    @abstractmethod
    def buscar_por_id(self, vacina_id: int):
        pass


    @abstractmethod
    def cadastrar(self, dados: VacinaCreate):
        pass


    @abstractmethod
    def atualizar(
        self,
        vacina_id: int,
        dados: VacinaUpdate
    ):
        pass


    @abstractmethod
    def deletar(self, vacina_id: int):
        pass