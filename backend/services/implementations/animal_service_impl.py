from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.animal_model import Animais
from backend.schemas.animal_schema import AnimalCreate, AnimalUpdate


class AnimalServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, animal: AnimalCreate):

        db = Animais(**animal.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db

    # LIST
    def listar(self):
        return self.session.scalars(select(Animais)).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Animais).where(Animais.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, animal: AnimalUpdate):

        db = self.session.scalars(
            select(Animais).where(Animais.id == id)
        ).first()

        if not db:
            return None

        dados = animal.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Animais).where(Animais.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True