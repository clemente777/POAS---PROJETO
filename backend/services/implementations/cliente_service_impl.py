from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.cliente_model import Clientes
from backend.schemas.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, cliente: ClienteCreate):

        db = Clientes(**cliente.model_dump())

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
        cpf: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):

        query = select(Clientes)

        # ==========================
        # FILTROS
        # ==========================

        if nome:
            query = query.where(
                Clientes.nome.ilike(f"%{nome}%")
            )

        if cpf:
            query = query.where(
                Clientes.cpf.ilike(f"%{cpf}%")
            )

        if telefone:
            query = query.where(
                Clientes.telefone.ilike(f"%{telefone}%")
            )

        if email:
            query = query.where(
                Clientes.email.ilike(f"%{email}%")
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Clientes.id,
            "nome": Clientes.nome,
            "cpf": Clientes.cpf,
            "telefone": Clientes.telefone,
            "email": Clientes.email,
        }

        coluna = campos.get(sort_by, Clientes.id)

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
        return self.session.scalars(
            select(Clientes).where(Clientes.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, cliente: ClienteUpdate):

        db = self.session.scalars(
            select(Clientes).where(Clientes.id == id)
        ).first()

        if not db:
            return None

        dados = cliente.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Clientes).where(Clientes.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True