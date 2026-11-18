from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy.exc import SQLAlchemyError

from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios
from backend.repositories.cliente_repository import ClienteRepository
from backend.schemas.cliente_schema import ClienteCreate, ClienteUpdate

senha_context = PasswordHash.recommended()


class ClienteServiceImpl:
    """Regras de negócio dos clientes."""

    def __init__(
        self,
        repository: ClienteRepository,
        usuario_logado: Usuarios,
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # NORMALIZAÇÕES
    # ==========================================================

    def normalizar_nome(self, nome: str):
        return " ".join(nome.strip().split()).title() if nome else ""

    def normalizar_email(self, email: str):
        return email.strip().lower() if email else ""

    def normalizar_cpf(self, cpf: str):
        return (
            cpf.replace(".", "")
            .replace("-", "")
            .strip()
            if cpf
            else ""
        )

    def normalizar_telefone(self, telefone: str):
        if not telefone:
            return ""

        return "".join(
            caractere
            for caractere in telefone
            if caractere.isdigit()
        )

    def obter_perfil(self):
        perfil = self.usuario_logado.perfil

        if hasattr(perfil, "nome"):
            return perfil.nome

        return perfil

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    def validar_nome(self, nome: str):
        if len(nome) < 3 or len(nome) > 100:
            raise HTTPException(
                status_code=400,
                detail="Nome inválido.",
            )

    def validar_email(self, email: str):
        if "@" not in email or "." not in email.split("@")[-1]:
            raise HTTPException(
                status_code=400,
                detail="E-mail inválido.",
            )

    def validar_telefone(self, telefone: str):
        if not telefone.isdigit() or len(telefone) not in (10, 11):
            raise HTTPException(
                status_code=400,
                detail="Telefone inválido. Informe DDD e número.",
            )

    def validar_cpf(self, cpf: str):
        if (
            len(cpf) != 11
            or not cpf.isdigit()
            or cpf == cpf[0] * 11
        ):
            raise HTTPException(
                status_code=400,
                detail="CPF inválido.",
            )

        soma = sum(
            int(cpf[i]) * (10 - i)
            for i in range(9)
        )

        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        soma = sum(
            int(cpf[i]) * (11 - i)
            for i in range(10)
        )

        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        if (
            int(cpf[9]) != digito1
            or int(cpf[10]) != digito2
        ):
            raise HTTPException(
                status_code=400,
                detail="CPF inválido.",
            )

    def validar_endereco(self, endereco: str):
        if not endereco or not endereco.strip():
            raise HTTPException(
                status_code=400,
                detail="Endereço obrigatório.",
            )

        if len(endereco.strip()) > 255:
            raise HTTPException(
                status_code=400,
                detail="Endereço deve ter no máximo 255 caracteres.",
            )

    # ==========================================================
    # CONTROLE DE ACESSO
    # ==========================================================

    def validar_acesso_cliente(self, cliente: Clientes):
        perfil = self.obter_perfil()

        if perfil in ("Administrador", "Veterinário"):
            return

        if perfil == "Cliente":
            if cliente.usuario_id != self.usuario_logado.id:
                raise HTTPException(
                    status_code=403,
                    detail="Você não possui acesso a este cliente.",
                )
            return

        raise HTTPException(
            status_code=403,
            detail="Perfil sem permissão.",
        )

    # ==========================================================
    # BUSCAR
    # ==========================================================

    def buscar_por_id(self, id: int):
        cliente = self.repository.buscar_por_id(id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado.",
            )

        self.validar_acesso_cliente(cliente)

        return cliente

    def buscar_por_cpf(self, cpf: str):
        return self.repository.buscar_por_cpf(
            self.normalizar_cpf(cpf)
        )

    def buscar_por_email(self, email: str):
        return self.repository.buscar_por_email(
            self.normalizar_email(email)
        )

    def buscar_por_usuario(self):
        return self.repository.buscar_por_usuario_id(
            self.usuario_logado.id
        )

    # ==========================================================
    # CRIAR
    # ==========================================================

    def criar(self, cliente: ClienteCreate):
        perfil = self.obter_perfil()

        nome = self.normalizar_nome(cliente.nome)
        cpf = self.normalizar_cpf(cliente.cpf)
        email = self.normalizar_email(cliente.email)
        telefone = self.normalizar_telefone(cliente.telefone)
        endereco = cliente.endereco.strip()

        self.validar_nome(nome)
        self.validar_cpf(cpf)
        self.validar_email(email)
        self.validar_telefone(telefone)
        self.validar_endereco(endereco)

        if self.repository.buscar_por_cpf(cpf):
            raise HTTPException(
                status_code=409,
                detail="CPF já cadastrado.",
            )

        if self.repository.buscar_por_email(email):
            raise HTTPException(
                status_code=409,
                detail="E-mail já cadastrado para outro cliente.",
            )

        # ------------------------------------------------------
        # ADMINISTRADOR: CRIA USUÁRIO E CLIENTE
        # ------------------------------------------------------

        if perfil == "Administrador":
            if not cliente.senha:
                raise HTTPException(
                    status_code=400,
                    detail="Informe a senha inicial do cliente.",
                )

            if len(cliente.senha) < 6:
                raise HTTPException(
                    status_code=400,
                    detail="A senha deve possuir no mínimo 6 caracteres.",
                )

            if self.repository.buscar_usuario_por_email(email):
                raise HTTPException(
                    status_code=409,
                    detail="E-mail já cadastrado como usuário.",
                )

            novo_usuario = Usuarios(
                nome=nome,
                email=email,
                senha_hash=senha_context.hash(cliente.senha),
                perfil="Cliente",
            )

            novo_cliente = Clientes(
                nome=nome,
                cpf=cpf,
                telefone=telefone,
                email=email,
                endereco=endereco,
            )

            try:
                return self.repository.criar_com_usuario(
                    novo_usuario,
                    novo_cliente,
                )

            except SQLAlchemyError as erro:
                raise HTTPException(
                    status_code=500,
                    detail="Erro ao criar usuário e cliente.",
                ) from erro

        # ------------------------------------------------------
        # CLIENTE: CRIA SEU PRÓPRIO CADASTRO
        # ------------------------------------------------------

        if perfil == "Cliente":
            usuario = self.repository.buscar_usuario_por_id(
                self.usuario_logado.id
            )

            if not usuario:
                raise HTTPException(
                    status_code=404,
                    detail="Usuário não encontrado.",
                )

            if usuario.perfil != "Cliente":
                raise HTTPException(
                    status_code=403,
                    detail="Somente clientes podem criar este cadastro.",
                )

            if self.repository.buscar_por_usuario_id(usuario.id):
                raise HTTPException(
                    status_code=409,
                    detail="Este usuário já possui cadastro de cliente.",
                )

            usuario_email = self.repository.buscar_usuario_por_email(email)

            if usuario_email and usuario_email.id != usuario.id:
                raise HTTPException(
                    status_code=409,
                    detail="E-mail já cadastrado.",
                )

            novo = Clientes(
                nome=nome,
                cpf=cpf,
                telefone=telefone,
                email=email,
                endereco=endereco,
                usuario_id=usuario.id,
            )

            usuario.nome = nome
            usuario.email = email

            try:
                return self.repository.criar_cliente_com_usuario_existente(novo,usuario,)

            except SQLAlchemyError as erro:
                raise HTTPException(
                    status_code=500,
                    detail="Erro ao criar cliente.",
                ) from erro

        raise HTTPException(
            status_code=403,
            detail="Sem permissão para cadastrar cliente.",
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
        order: str = "asc",
    ):
        skip = max(skip, 0)
        limit = min(max(limit, 1), 100)

        perfil = self.obter_perfil()
        usuario_id = None

        if perfil == "Cliente":
            usuario_id = self.usuario_logado.id

        return self.repository.listar(
            skip=skip,
            limit=limit,
            nome=nome.strip() if nome else None,
            cpf=self.normalizar_cpf(cpf) if cpf else None,
            email=self.normalizar_email(email) if email else None,
            usuario_id=usuario_id,
            sort_by=sort_by,
            order=order,
        )

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

    def atualizar(self, id: int, cliente: ClienteUpdate):
        db = self.buscar_por_id(id)
        perfil = self.obter_perfil()

        dados = cliente.model_dump(exclude_unset=True)

        if not dados:
            raise HTTPException(
                status_code=400,
                detail="Nenhum dado foi enviado para atualização.",
            )

        # ------------------------------------------------------
        # ADMINISTRADOR: SOMENTE TELEFONE E ENDEREÇO
        # ------------------------------------------------------

        if perfil == "Administrador":
            campos_permitidos = {"telefone", "endereco"}
            campos_proibidos = set(dados) - campos_permitidos

            if campos_proibidos:
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Administrador só pode alterar telefone e endereço."
                    ),
                )

        elif perfil != "Cliente":
            raise HTTPException(
                status_code=403,
                detail="Perfil sem permissão para atualizar clientes.",
            )

        usuario = self.repository.buscar_usuario_por_id(
            db.usuario_id
        )

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Conta de acesso do cliente não encontrada.",
            )

        if "nome" in dados:
            if dados["nome"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="Nome obrigatório.",
                )

            nome = self.normalizar_nome(dados["nome"])
            self.validar_nome(nome)

            db.nome = nome
            usuario.nome = nome

        if "cpf" in dados:
            if dados["cpf"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="CPF obrigatório.",
                )

            cpf = self.normalizar_cpf(dados["cpf"])
            self.validar_cpf(cpf)

            existente = self.repository.buscar_por_cpf(cpf)

            if existente and existente.id != db.id:
                raise HTTPException(
                    status_code=409,
                    detail="CPF já cadastrado.",
                )

            db.cpf = cpf

        if "email" in dados:
            if dados["email"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="E-mail obrigatório.",
                )

            email = self.normalizar_email(str(dados["email"]))
            self.validar_email(email)

            cliente_existente = self.repository.buscar_por_email(email)
            usuario_existente = self.repository.buscar_usuario_por_email(email)

            if cliente_existente and cliente_existente.id != db.id:
                raise HTTPException(
                    status_code=409,
                    detail="E-mail já cadastrado.",
                )

            if usuario_existente and usuario_existente.id != usuario.id:
                raise HTTPException(
                    status_code=409,
                    detail="E-mail já cadastrado por outro usuário.",
                )

            db.email = email
            usuario.email = email

        if "telefone" in dados:
            if dados["telefone"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="Telefone obrigatório.",
                )

            telefone = self.normalizar_telefone(dados["telefone"])
            self.validar_telefone(telefone)
            db.telefone = telefone

        if "endereco" in dados:
            if dados["endereco"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="Endereço obrigatório.",
                )

            endereco = dados["endereco"].strip()
            self.validar_endereco(endereco)
            db.endereco = endereco

        try:
            return self.repository.atualizar_com_usuario(
                db,
                usuario,
            )

        except SQLAlchemyError as erro:
            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar cliente.",
            ) from erro

    # ==========================================================
    # EXCLUSÃO BLOQUEADA
    # ==========================================================

    def deletar(self, id: int):
        raise HTTPException(
            status_code=403,
            detail="A exclusão de clientes não está disponível.",
        )