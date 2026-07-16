from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.usuario_model import Usuarios
from backend.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from pwdlib import PasswordHash


senha_context = PasswordHash.recommended()


class UsuarioServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, usuario: UsuarioCreate):

        db = Usuarios(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=senha_context.hash(usuario.senha)
        )

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
        email: str | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):

        query = select(Usuarios)

        # ==========================
        # FILTROS
        # ==========================

        if nome:
            query = query.where(
                Usuarios.nome.ilike(f"%{nome}%")
            )

        if email:
            query = query.where(
                Usuarios.email.ilike(f"%{email}%")
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Usuarios.id,
            "nome": Usuarios.nome,
            "email": Usuarios.email,
            "criado_em": Usuarios.criado_em,
        }

        coluna = campos.get(sort_by, Usuarios.id)

        if order.lower() == "desc":
            query = query.order_by(desc(coluna))
        else:
            query = query.order_by(asc(coluna))

        # ==========================
        # PAGINAÇÃO
        # ==========================

        query = query.offset(skip).limit(limit)

        return self.session.scalars(query).all()

    # GET
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Usuarios).where(Usuarios.id == id)
        ).first()
    
    # GET BY EMAIL (LOGIN)
    def buscar_por_email(self, email: str):

        return self.session.scalars(
            select(Usuarios).where(Usuarios.email == email)
        ).first()
    
    # UPDATE
    def atualizar(self, id: int, usuario: UsuarioUpdate):

        db = self.session.scalars(
            select(Usuarios).where(Usuarios.id == id)
        ).first()

        if not db:
            return None

        dados = usuario.model_dump(exclude_unset=True)

        if "senha" in dados:
            db.senha_hash = senha_context.hash(dados["senha"])
            del dados["senha"]

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Usuarios).where(Usuarios.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True