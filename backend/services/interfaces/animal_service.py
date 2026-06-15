from abc import ABC, abstractmethod

class AnimalService(ABC):

    @abstractmethod
    def listar_animais(self):
        pass

    @abstractmethod
    def buscar_animal_por_id(self, id):
        pass

    @abstractmethod
    def criar_animal(self, animal):
        pass

    @abstractmethod
    def atualizar_animal(self, id, animal):
        pass

    @abstractmethod
    def deletar_animal(self, id):
        pass