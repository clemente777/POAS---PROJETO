from sqlalchemy import asc, desc, select
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
    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        especie: str | None = None,
        raca: str | None = None,
        idade: int | None = None,
        cliente_id: int | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):

        query = select(Animais)

        # ==========================
        # FILTROS
        # ==========================

        if nome:
            query = query.where(
                Animais.nome.ilike(f"%{nome}%")
            )

        if especie:
            query = query.where(
                Animais.especie.ilike(f"%{especie}%")
            )

        if raca:
            query = query.where(
                Animais.raca.ilike(f"%{raca}%")
            )

        if idade is not None:
            query = query.where(
                Animais.idade == idade
            )

        if cliente_id is not None:
            query = query.where(
                Animais.cliente_id == cliente_id
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Animais.id,
            "nome": Animais.nome,
            "especie": Animais.especie,
            "raca": Animais.raca,
            "idade": Animais.idade,
            "cliente_id": Animais.cliente_id,
        }

        coluna = campos.get(sort_by, Animais.id)

        if order.lower() == "desc":
            query = query.order_by(desc(coluna))
        else:
            query = query.order_by(asc(coluna))

        # ==========================
        # PAGINAÇÃO
        # ==========================

        query = query.offset(skip).limit(limit)

        return self.session.scalars(query).all()
            
        # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(                select(Animais).where(Animais.id == id)
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