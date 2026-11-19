from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy.exc import SQLAlchemyError

from backend.models.usuario_model import Usuarios
from backend.repositories.cliente_repository import ClienteRepository
from backend.repositories.usuario_repository import UsuarioRepository
from backend.schemas.cliente_schema import ClienteUpdate
from backend.schemas.perfil_schema import PerfilUpdate
from backend.schemas.usuario_schema import (
    UsuarioAdminCreate,
    UsuarioCreate,
    UsuarioUpdate,
)
from backend.services.implementations.cliente_service_impl import ClienteServiceImpl

senha_context = PasswordHash.recommended()


class UsuarioServiceImpl:
    """
    Regras de negócio dos usuários.

    Perfis:

    Administrador:
        - Controle total.

    Veterinário:
        - Não gerencia usuários.

    Cliente:
        - Gerencia apenas sua própria conta.

    Regras:

    • Cadastro público cria Cliente.
    • Apenas Administrador cria outros perfis.
    • Email único.
    • Senha criptografada.
    • Perfil protegido.
    """

    def __init__(
        self,
        repository: UsuarioRepository,
        cliente_repository: ClienteRepository,
        usuario_logado: Usuarios | None = None,
    ):
        self.repository = repository
        self.cliente_repository = cliente_repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================

    def normalizar_email(self, email: str):

        if not email:
            return ""

        return email.strip().lower()

    def normalizar_nome(self, nome: str):

        if not nome:
            return ""

        return " ".join(nome.strip().split()).title()

    def normalizar_perfil(self, perfil: str):

        if not perfil:
            raise HTTPException(status_code=400, detail="Perfil obrigatório.")

        perfil = perfil.strip().lower()

        perfis = {
            "administrador": "Administrador",
            "admin": "Administrador",
            "veterinario": "Veterinário",
            "veterinário": "Veterinário",
            "vet": "Veterinário",
            "cliente": "Cliente",
        }

        if perfil not in perfis:
            raise HTTPException(status_code=400, detail="Perfil inválido.")

        return perfis[perfil]

    # ==========================================================
    # CONTROLE DE ACESSO
    # ==========================================================

    def validar_usuario_logado(self):

        if not self.usuario_logado:
            raise HTTPException(status_code=401, detail="Usuário não autenticado.")

    def validar_acesso_usuario(self, usuario_db: Usuarios):

        self.validar_usuario_logado()

        perfil = self.usuario_logado.perfil

        if perfil == "Administrador":
            return

        if perfil == "Cliente":
            if usuario_db.id != self.usuario_logado.id:
                raise HTTPException(
                    status_code=403,
                    detail="Você não possui acesso a este usuário.",
                )

            return

        raise HTTPException(status_code=403, detail="Perfil sem permissão.")

    # ==========================================================
    # BUSCAR POR ID
    # ==========================================================

    def buscar_por_id(self, id: int):

        usuario = self.repository.buscar_por_id(id)

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        self.validar_acesso_usuario(usuario)

        return usuario

    # ==========================================================
    # BUSCAR POR EMAIL
    # ==========================================================

    def buscar_por_email(self, email: str):

        email = self.normalizar_email(email)

        return self.repository.buscar_por_email(email)

    # ==========================================================
    # BUSCAR CLIENTE PELO USUÁRIO
    # ==========================================================

    def buscar_cliente_por_usuario_id(self, usuario_id: int):

        return self.cliente_repository.buscar_por_usuario_id(usuario_id)

    # ==========================================================
    # CRIAR USUÁRIO PÚBLICO
    # ==========================================================

    def criar(self, usuario: UsuarioCreate):
        """
        Cadastro público.

        Sempre cria um usuário com perfil Cliente.
        """

        nome = self.normalizar_nome(usuario.nome)

        email = self.normalizar_email(usuario.email)

        if not nome:
            raise HTTPException(status_code=400, detail="Nome obrigatório.")

        if len(usuario.senha) < 6:
            raise HTTPException(
                status_code=400,
                detail="A senha deve possuir mínimo 6 caracteres.",
            )

        if self.repository.buscar_por_email(email):
            raise HTTPException(status_code=409, detail="Email já cadastrado.")

        novo_usuario = Usuarios(
            nome=nome,
            email=email,
            senha_hash=senha_context.hash(usuario.senha),
            perfil="Cliente",
        )

        try:
            return self.repository.criar(novo_usuario)

        except SQLAlchemyError as erro:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar usuário.",
            ) from erro

    # ==========================================================
    # CRIAR USUÁRIO POR ADMINISTRADOR
    # ==========================================================

    def criar_por_admin(self, usuario: UsuarioAdminCreate):
        """
        Criado somente pelo Administrador.

        Permite criar:

        • Administrador
        • Veterinário
        • Cliente
        """

        self.validar_usuario_logado()

        if self.usuario_logado.perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail="Somente Administrador pode criar usuários.",
            )

        nome = self.normalizar_nome(usuario.nome)

        email = self.normalizar_email(usuario.email)

        perfil = self.normalizar_perfil(usuario.perfil)

        if not nome:
            raise HTTPException(status_code=400, detail="Nome obrigatório.")

        if len(usuario.senha) < 6:
            raise HTTPException(
                status_code=400,
                detail="A senha deve possuir mínimo 6 caracteres.",
            )

        if self.repository.buscar_por_email(email):
            raise HTTPException(status_code=409, detail="Email já cadastrado.")

        novo_usuario = Usuarios(
            nome=nome,
            email=email,
            senha_hash=senha_context.hash(usuario.senha),
            perfil=perfil,
        )

        try:
            return self.repository.criar(novo_usuario)

        except SQLAlchemyError as erro:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar usuário.",
            ) from erro

    # ==========================================================
    # LISTAR USUÁRIOS
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        email: str | None = None,
        perfil: str | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):

        self.validar_usuario_logado()

        if self.usuario_logado.perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail="Somente Administrador pode listar usuários.",
            )

        skip = max(skip, 0)

        if limit <= 0:
            limit = 10

        limit = min(limit, 100)

        perfil_normalizado = None

        if perfil:
            perfil_normalizado = self.normalizar_perfil(perfil)

        return self.repository.listar(
            skip=skip,
            limit=limit,
            nome=(nome.strip() if nome else None),
            email=(self.normalizar_email(email) if email else None),
            perfil=perfil_normalizado,
            sort_by=sort_by,
            order=order,
        )

    # ==========================================================
    # ATUALIZAR USUÁRIO
    # ==========================================================

    def atualizar(self, id: int, usuario: UsuarioUpdate):

        usuario_db = self.repository.buscar_por_id(id)

        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        self.validar_acesso_usuario(usuario_db)

        dados = usuario.model_dump(exclude_unset=True)

        # ------------------------------------------------------
        # CLIENTE NÃO PODE ALTERAR PERFIL
        # ------------------------------------------------------

        if "perfil" in dados and self.usuario_logado.perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail="Somente Administrador pode alterar perfil.",
            )

        # ------------------------------------------------------
        # NOME
        # ------------------------------------------------------

        if "nome" in dados:
            nome = self.normalizar_nome(dados["nome"])

            if not nome:
                raise HTTPException(status_code=400, detail="Nome obrigatório.")

            usuario_db.nome = nome

        # ------------------------------------------------------
        # EMAIL
        # ------------------------------------------------------

        if "email" in dados:
            email = self.normalizar_email(dados["email"])

            if not email:
                raise HTTPException(status_code=400, detail="Email obrigatório.")

            existente = self.repository.buscar_por_email(email)

            if existente and existente.id != usuario_db.id:
                raise HTTPException(status_code=409, detail="Email já cadastrado.")

            usuario_db.email = email

        # ------------------------------------------------------
        # SENHA
        # ------------------------------------------------------

        if "senha" in dados:
            if len(dados["senha"]) < 6:
                raise HTTPException(
                    status_code=400,
                    detail="A senha deve possuir no mínimo 6 caracteres.",
                )

            usuario_db.senha_hash = senha_context.hash(dados["senha"])

        # ------------------------------------------------------
        # PERFIL
        # ------------------------------------------------------

        if "perfil" in dados:
            if self.usuario_logado.perfil != "Administrador":
                raise HTTPException(
                    status_code=403,
                    detail="Somente Administrador pode alterar perfil.",
                )

            usuario_db.perfil = self.normalizar_perfil(dados["perfil"])

        try:
            return self.repository.atualizar(usuario_db)

        except SQLAlchemyError as erro:
            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar usuário.",
            ) from erro

    # ==========================================================
    # DELETAR USUÁRIO
    # ==========================================================

    def deletar(self, id: int):

        usuario_db = self.repository.buscar_por_id(id)

        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        self.validar_usuario_logado()

        if self.usuario_logado.perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail="Somente Administrador pode excluir usuários.",
            )

        # ------------------------------------------------------
        # IMPEDIR AUTOEXCLUSÃO
        # ------------------------------------------------------

        if usuario_db.id == self.usuario_logado.id:
            raise HTTPException(
                status_code=400,
                detail="Administrador não pode excluir o próprio usuário.",
            )

        try:
            self.repository.deletar(usuario_db)

        except SQLAlchemyError as erro:
            raise HTTPException(
                status_code=500,
                detail="Erro ao excluir usuário.",
            ) from erro

    def obter_meu_perfil(self):
        if not self.usuario_logado:
            raise HTTPException(
                status_code=401,
                detail="Usuário não autenticado.",
            )

        usuario = self.repository.buscar_por_id(self.usuario_logado.id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado.",
            )

        cliente = None

        if usuario.perfil == "Cliente":
            cliente = self.cliente_repository.buscar_por_usuario_id(usuario.id)

        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "cliente_id": cliente.id if cliente else None,
            "cpf": cliente.cpf if cliente else None,
            "telefone": cliente.telefone if cliente else None,
            "endereco": cliente.endereco if cliente else None,
        }

    def atualizar_meu_perfil(self, dados: PerfilUpdate):
        if not self.usuario_logado:
            raise HTTPException(
                status_code=401,
                detail="Usuário não autenticado.",
            )

        usuario = self.repository.buscar_por_id(self.usuario_logado.id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado.",
            )

        dados_dict = dados.model_dump(exclude_unset=True)

        if not dados_dict:
            raise HTTPException(
                status_code=400,
                detail="Informe pelo menos um campo para atualizar.",
            )

        if usuario.perfil == "Cliente":
            cliente = self.cliente_repository.buscar_por_usuario_id(usuario.id)

            if not cliente:
                raise HTTPException(
                    status_code=404,
                    detail="Cadastro de cliente não encontrado.",
                )

            cliente_dados = ClienteUpdate(**dados_dict)

            cliente_service = ClienteServiceImpl(
                self.cliente_repository,
                usuario,
            )

            cliente_service.atualizar(
                cliente.id,
                cliente_dados,
            )

        else:
            campos_permitidos = {"nome", "email"}

            campos_invalidos = set(dados_dict) - campos_permitidos

            if campos_invalidos:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Administradores e veterinários podem "
                        "alterar somente nome e e-mail."
                    ),
                )

            if "nome" in dados_dict:
                nome = dados_dict["nome"].strip()

                if len(nome) < 3:
                    raise HTTPException(
                        status_code=400,
                        detail="O nome deve possuir pelo menos 3 caracteres.",
                    )

                usuario.nome = nome

            if "email" in dados_dict:
                email = str(dados_dict["email"]).strip().lower()

                usuario_existente = self.repository.buscar_por_email(email)

                if usuario_existente and usuario_existente.id != usuario.id:
                    raise HTTPException(
                        status_code=409,
                        detail="Este e-mail já está cadastrado.",
                    )

                usuario.email = email

            self.repository.atualizar(usuario)

        return self.obter_meu_perfil()

    def alterar_minha_senha(self, senha_atual: str, nova_senha: str):
        if not self.usuario_logado:
            raise HTTPException(
                status_code=401,
                detail="Usuário não autenticado.",
            )

        usuario = self.repository.buscar_por_id(self.usuario_logado.id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado.",
            )

        password_hash = PasswordHash.recommended()

        if not password_hash.verify(
            senha_atual,
            usuario.senha_hash,
        ):
            raise HTTPException(
                status_code=400,
                detail="A senha atual está incorreta.",
            )

        if senha_atual == nova_senha:
            raise HTTPException(
                status_code=400,
                detail="A nova senha deve ser diferente da senha atual.",
            )

        usuario.senha_hash = password_hash.hash(nova_senha)

        self.repository.atualizar(usuario)

        return {"mensagem": "Senha alterada com sucesso."}
