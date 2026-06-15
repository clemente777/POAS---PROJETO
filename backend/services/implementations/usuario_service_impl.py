from sqlmodel import Session
from pwdlib import PasswordHash

from backend.models.models import Usuarios
from backend.services.interfaces.usuario_service import UsuarioService

senha_context = PasswordHash.recommended()


class UsuarioServiceImpl(UsuarioService):

    def __init__(self, session: Session):
        self.session = session

    def listar_usuarios(self):
        return self.session.query(
            Usuarios
        ).all()

    def buscar_usuario_por_id(self, id):
        return self.session.query(
            Usuarios
        ).get(id)

    def criar_usuario(self, usuario_schema):

        usuario = Usuarios(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha_hash=senha_context.hash(
                usuario_schema.senha_hash
            )
        )

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario

    def atualizar_usuario(
        self,
        id,
        usuario_schema
    ):

        usuario = self.session.query(
            Usuarios
        ).get(id)

        if not usuario:
            return None

        dados = usuario_schema.model_dump(
            exclude_unset=True
        )

        if "senha_hash" in dados:
            dados["senha_hash"] = senha_context.hash(
                dados["senha_hash"]
            )

        self.session.query(
            Usuarios
        ).filter(
            Usuarios.id == id
        ).update(dados)

        self.session.commit()

        return usuario

    def deletar_usuario(self, id):

        usuario = self.session.query(
            Usuarios
        ).get(id)

        if not usuario:
            return False

        self.session.delete(usuario)
        self.session.commit()

        return True