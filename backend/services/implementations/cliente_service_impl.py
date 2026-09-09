from fastapi import HTTPException

from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios
from backend.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate
)
from backend.repositories.cliente_repository import ClienteRepository


class ClienteServiceImpl:
    """Regras de negócio dos clientes."""

    def __init__(
        self,
        repository: ClienteRepository,
        usuario_logado: Usuarios
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # NORMALIZAÇÕES
    # ==========================================================

    def normalizar_nome(self, nome: str):

        if not nome:
            return ""

        return " ".join(
            nome.strip().split()
        ).title()

    def normalizar_email(self, email: str):

        if not email:
            return ""

        return email.strip().lower()

    def normalizar_cpf(self, cpf: str):

        if not cpf:
            return ""

        return (
            cpf
            .replace(".", "")
            .replace("-", "")
            .strip()
        )

    def normalizar_telefone(self, telefone: str):

        if not telefone:
            return ""

        return (
            telefone
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

    # ==========================================================
    # PERFIL
    # ==========================================================

    def obter_perfil(self):

        perfil = self.usuario_logado.perfil

        if hasattr(perfil, "nome"):
            return perfil.nome

        return perfil

    # ==========================================================
    # CONTROLE DE ACESSO
    # ==========================================================

    def validar_acesso_cliente(
        self,
        cliente: Clientes
    ):

        perfil = self.obter_perfil()

        if perfil in [
            "Administrador",
            "Veterinário"
        ]:
            return

        if perfil == "Cliente":

            if (
                cliente.usuario_id
                != self.usuario_logado.id
            ):
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Você não possui acesso "
                        "a este cliente."
                    )
                )

            return

        raise HTTPException(
            status_code=403,
            detail="Perfil sem permissão."
        )

    # ==========================================================
    # BUSCAR POR ID
    # ==========================================================

    def buscar_por_id(self, id: int):

        cliente = self.repository.buscar_por_id(id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )

        self.validar_acesso_cliente(cliente)

        return cliente

    # ==========================================================
    # BUSCAR POR CPF
    # ==========================================================

    def buscar_por_cpf(self, cpf: str):

        cpf = self.normalizar_cpf(cpf)

        return self.repository.buscar_por_cpf(cpf)

    # ==========================================================
    # BUSCAR POR EMAIL
    # ==========================================================

    def buscar_por_email(self, email: str):

        email = self.normalizar_email(email)

        return self.repository.buscar_por_email(email)

    # ==========================================================
    # BUSCAR POR USUÁRIO
    # ==========================================================

    def buscar_por_usuario(self):

        return self.repository.buscar_por_usuario_id(
            self.usuario_logado.id
        )

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    def validar_nome(self, nome: str):

        nome = self.normalizar_nome(nome)

        if len(nome) < 3:
            raise HTTPException(
                status_code=400,
                detail="Nome inválido."
            )

    def validar_email(self, email: str):

        email = self.normalizar_email(email)

        if (
            "@" not in email
            or "." not in email.split("@")[-1]
        ):
            raise HTTPException(
                status_code=400,
                detail="Email inválido."
            )

    def validar_telefone(self, telefone: str):

        telefone = self.normalizar_telefone(
            telefone
        )

        if (
            not telefone.isdigit()
            or len(telefone) not in [10, 11]
        ):
            raise HTTPException(
                status_code=400,
                detail="Telefone inválido."
            )

    def validar_cpf(self, cpf: str):

        cpf = self.normalizar_cpf(cpf)

        if (
            len(cpf) != 11
            or not cpf.isdigit()
            or cpf == cpf[0] * 11
        ):
            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )

        soma = sum(
            int(cpf[i]) * (10 - i)
            for i in range(9)
        )

        resto = soma % 11

        digito1 = (
            0
            if resto < 2
            else 11 - resto
        )

        soma = sum(
            int(cpf[i]) * (11 - i)
            for i in range(10)
        )

        resto = soma % 11

        digito2 = (
            0
            if resto < 2
            else 11 - resto
        )

        if (
            int(cpf[9]) != digito1
            or int(cpf[10]) != digito2
        ):
            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )

    # ==========================================================
    # CRIAR
    # ==========================================================

    def criar(
        self,
        cliente: ClienteCreate
    ):

        perfil = self.obter_perfil()

        if perfil not in [
            "Cliente",
            "Administrador"
        ]:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Sem permissão para "
                    "cadastrar cliente."
                )
            )

        usuario = (
            self.repository.buscar_usuario_por_id(
                self.usuario_logado.id
            )
        )

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        nome = self.normalizar_nome(
            cliente.nome
        )

        cpf = self.normalizar_cpf(
            cliente.cpf
        )

        email = self.normalizar_email(
            cliente.email
        )

        telefone = self.normalizar_telefone(
            cliente.telefone
        )

        self.validar_nome(nome)
        self.validar_cpf(cpf)
        self.validar_email(email)
        self.validar_telefone(telefone)

        if self.repository.buscar_por_cpf(cpf):

            raise HTTPException(
                status_code=409,
                detail="CPF já cadastrado."
            )

        if self.repository.buscar_por_email(email):

            raise HTTPException(
                status_code=409,
                detail="Email já cadastrado."
            )

        if self.repository.buscar_por_usuario_id(
            usuario.id
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Usuário já possui cadastro "
                    "de cliente."
                )
            )

        novo = Clientes(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
            endereco=cliente.endereco.strip(),
            usuario_id=usuario.id
        )

        try:
            return self.repository.criar(novo)

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar cliente."
            )

    # ==========================================================
    # LISTAR
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        cpf: str | None = None,
        email: str | None = None,
        sort_by: str = "nome",
        order: str = "asc"
    ):

        if skip < 0:
            skip = 0

        if limit <= 0:
            limit = 10

        if limit > 100:
            limit = 100

        perfil = self.obter_perfil()

        usuario_id = None

        if perfil == "Cliente":
            usuario_id = self.usuario_logado.id

        return self.repository.listar(
            skip=skip,
            limit=limit,
            nome=(
                nome.strip()
                if nome
                else None
            ),
            cpf=(
                self.normalizar_cpf(cpf)
                if cpf
                else None
            ),
            email=(
                self.normalizar_email(email)
                if email
                else None
            ),
            usuario_id=usuario_id,
            sort_by=sort_by,
            order=order
        )

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

    def atualizar(
        self,
        id: int,
        cliente: ClienteUpdate
    ):

        db = self.buscar_por_id(id)

        dados = cliente.model_dump(
            exclude_unset=True
        )

        if "nome" in dados:

            nome = self.normalizar_nome(
                dados["nome"]
            )

            self.validar_nome(nome)

            db.nome = nome

        if "cpf" in dados:

            cpf = self.normalizar_cpf(
                dados["cpf"]
            )

            self.validar_cpf(cpf)

            existente = (
                self.repository.buscar_por_cpf(cpf)
            )

            if (
                existente
                and existente.id != db.id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="CPF já cadastrado."
                )

            db.cpf = cpf

        if "email" in dados:

            email = self.normalizar_email(
                dados["email"]
            )

            self.validar_email(email)

            existente = (
                self.repository.buscar_por_email(
                    email
                )
            )

            if (
                existente
                and existente.id != db.id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="Email já cadastrado."
                )

            db.email = email

        if "telefone" in dados:

            telefone = self.normalizar_telefone(
                dados["telefone"]
            )

            self.validar_telefone(telefone)

            db.telefone = telefone

        if "endereco" in dados:

            db.endereco = (
                dados["endereco"].strip()
            )

        try:
            return self.repository.atualizar(db)

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar cliente."
            )

    # ==========================================================
    # DELETAR
    # ==========================================================

    def deletar(self, id: int):

        cliente = self.buscar_por_id(id)

        if self.repository.possui_animais(
            cliente.id
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Não é possível excluir "
                    "um cliente que possui "
                    "animais cadastrados."
                )
            )

        if self.repository.possui_atendimentos(
            cliente.id
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Não é possível excluir "
                    "cliente com histórico "
                    "veterinário."
                )
            )

        if self.repository.possui_carrinhos(
            cliente.id
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Não é possível excluir "
                    "cliente que possui compras."
                )
            )

        try:
            self.repository.deletar(cliente)

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao excluir cliente."
            )