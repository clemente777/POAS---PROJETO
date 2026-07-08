from sqlalchemy import select
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
    def listar(self):
        return self.session.scalars(select(Usuarios)).all()

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