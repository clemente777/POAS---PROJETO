from sqlmodel import Session
from backend.models.models import Animais

class AnimalServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    def listar_animais(self):
        return self.session.query(Animais).all()

    def buscar_animal_por_id(self, id):
        return self.session.query(Animais).get(id)

    def criar_animal(self, animal):
        self.session.add(animal)
        self.session.commit()
        self.session.refresh(animal)
        return animal

    def atualizar_animal(self, id, animal):
        self.session.query(Animais).filter(
            Animais.id == id
        ).update(animal.model_dump(exclude_unset=True))

        self.session.commit()

    def deletar_animal(self, id):
        animal = self.session.query(Animais).get(id)

        if animal:
            self.session.delete(animal)
            self.session.commit()
            return True

        return False