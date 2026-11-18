from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.animal_model import Animais
from backend.models.atendimento_model import Atendimentos
from backend.models.carrinho_model import Carrinhos
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios


class ClienteRepository:
    """Acesso ao banco de dados dos clientes."""

    def __init__(self, session: Session):
        self.session = session

    def buscar_por_id(self, cliente_id: int):
        return self.session.scalar(
            select(Clientes).where(Clientes.id == cliente_id)
        )

    def buscar_por_cpf(self, cpf: str):
        return self.session.scalar(
            select(Clientes).where(Clientes.cpf == cpf)
        )

    def buscar_por_email(self, email: str):
        return self.session.scalar(
            select(Clientes).where(Clientes.email == email)
        )

    def buscar_por_usuario_id(self, usuario_id: int):
        return self.session.scalar(
            select(Clientes).where(Clientes.usuario_id == usuario_id)
        )

    def buscar_usuario_por_id(self, usuario_id: int):
        return self.session.scalar(
            select(Usuarios).where(Usuarios.id == usuario_id)
        )

    def buscar_usuario_por_email(self, email: str):
        return self.session.scalar(
            select(Usuarios).where(Usuarios.email == email)
        )

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        cpf: str | None = None,
        email: str | None = None,
        usuario_id: int | None = None,
        sort_by: str = "nome",
        order: str = "asc",
    ):
        query = select(Clientes)

        if usuario_id is not None:
            query = query.where(Clientes.usuario_id == usuario_id)

        if nome:
            query = query.where(
                Clientes.nome.ilike(f"%{nome.strip()}%")
            )

        if cpf:
            query = query.where(Clientes.cpf == cpf)

        if email:
            query = query.where(
                Clientes.email.ilike(f"%{email.strip()}%")
            )

        campos = {
            "id": Clientes.id,
            "nome": Clientes.nome,
            "cpf": Clientes.cpf,
            "email": Clientes.email,
        }

        coluna = campos.get(sort_by, Clientes.nome)

        if order.lower() == "desc":
            query = query.order_by(desc(coluna))
        else:
            query = query.order_by(asc(coluna))

        return self.session.scalars(
            query.offset(skip).limit(limit)
        ).all()

    # ==========================================================
    # CADASTRO ATÔMICO DE USUÁRIO + CLIENTE
    # ==========================================================

    def criar_com_usuario(
        self,
        usuario: Usuarios,
        cliente: Clientes,
    ):
        try:
            self.session.add(usuario)
            self.session.flush()

            cliente.usuario_id = usuario.id

            self.session.add(cliente)
            self.session.flush()

            self.session.commit()
            self.session.refresh(cliente)

            return cliente

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # CRIAR CLIENTE DE USUÁRIO JÁ EXISTENTE
    # ==========================================================

    def criar(self, cliente: Clientes):
        try:
            self.session.add(cliente)
            self.session.commit()
            self.session.refresh(cliente)

            return cliente

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # ATUALIZAR CLIENTE E USUÁRIO NA MESMA TRANSAÇÃO
    # ==========================================================

    def atualizar_com_usuario(
        self,
        cliente: Clientes,
        usuario: Usuarios,
    ):
        try:
            self.session.commit()
            self.session.refresh(cliente)
            self.session.refresh(usuario)

            return cliente

        except Exception:
            self.session.rollback()
            raise

    def atualizar(self, cliente: Clientes):
        try:
            self.session.commit()
            self.session.refresh(cliente)

            return cliente

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # VERIFICAÇÕES DE VÍNCULOS
    # ==========================================================

    def possui_animais(self, cliente_id: int):
        return self.session.scalar(
            select(Animais).where(
                Animais.cliente_id == cliente_id
            )
        )

    def possui_atendimentos(self, cliente_id: int):
        return self.session.scalar(
            select(Atendimentos)
            .join(
                Animais,
                Atendimentos.animal_id == Animais.id,
            )
            .where(Animais.cliente_id == cliente_id)
        )

    def possui_carrinhos(self, cliente_id: int):
        return self.session.scalar(
            select(Carrinhos).where(
                Carrinhos.cliente_id == cliente_id
            )
        )
    def criar_cliente_com_usuario_existente(
    self,
        cliente: Clientes,
        usuario: Usuarios,
    ):
        try:
            self.session.add(cliente)
            self.session.flush()

            self.session.commit()
            self.session.refresh(cliente)
            self.session.refresh(usuario)

            return cliente

        except Exception:
            self.session.rollback()
            raise