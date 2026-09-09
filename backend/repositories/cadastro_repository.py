from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes


class CadastroRepository:
    """
    Repository responsável pelo acesso ao banco de dados
    durante o cadastro público.

    Responsabilidades:

    - Verificar email existente.
    - Verificar CPF existente.
    - Criar usuário.
    - Criar cliente.
    - Controlar a transação de cadastro.
    """

    def __init__(
        self,
        session: Session
    ):
        self.session = session

    # ==========================================================
    # BUSCAR USUÁRIO POR EMAIL
    # ==========================================================

    def buscar_usuario_por_email(
        self,
        email: str
    ) -> Usuarios | None:

        return self.session.scalar(
            select(Usuarios)
            .where(
                Usuarios.email == email
            )
        )

    # ==========================================================
    # BUSCAR CLIENTE POR CPF
    # ==========================================================

    def buscar_cliente_por_cpf(
        self,
        cpf: str
    ) -> Clientes | None:

        return self.session.scalar(
            select(Clientes)
            .where(
                Clientes.cpf == cpf
            )
        )

    # ==========================================================
    # CRIAR USUÁRIO
    # ==========================================================

    def criar_usuario(
        self,
        usuario: Usuarios
    ) -> Usuarios:

        self.session.add(usuario)

        # O flush gera o ID do usuário sem finalizar
        # a transação.

        self.session.flush()

        return usuario

    # ==========================================================
    # CRIAR CLIENTE
    # ==========================================================

    def criar_cliente(
        self,
        cliente: Clientes
    ) -> Clientes:

        self.session.add(cliente)

        return cliente

    # ==========================================================
    # FINALIZAR CADASTRO
    # ==========================================================

    def finalizar_cadastro(
        self,
        usuario: Usuarios,
        cliente: Clientes
    ):

        try:

            self.session.commit()

            self.session.refresh(
                usuario
            )

            self.session.refresh(
                cliente
            )

            return usuario, cliente

        except Exception:

            self.session.rollback()

            raise

    # ==========================================================
    # DESFAZER TRANSAÇÃO
    # ==========================================================

    def rollback(self):

        self.session.rollback()

