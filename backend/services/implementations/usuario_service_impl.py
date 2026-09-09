from fastapi import HTTPException
from pwdlib import PasswordHash

from backend.models.usuario_model import Usuarios
from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioAdminCreate
)
from backend.repositories.usuario_repository import (
    UsuarioRepository
)


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
        usuario_logado: Usuarios | None = None
    ):
        self.repository = repository
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

        return " ".join(
            nome.strip().split()
        ).title()

    def normalizar_perfil(self, perfil: str):

        if not perfil:
            raise HTTPException(
                status_code=400,
                detail="Perfil obrigatório."
            )

        perfil = (
            perfil
            .strip()
            .lower()
        )

        perfis = {
            "administrador": "Administrador",
            "admin": "Administrador",
            "veterinario": "Veterinário",
            "veterinário": "Veterinário",
            "vet": "Veterinário",
            "cliente": "Cliente"
        }

        if perfil not in perfis:
            raise HTTPException(
                status_code=400,
                detail="Perfil inválido."
            )

        return perfis[perfil]

    # ==========================================================
    # CONTROLE DE ACESSO
    # ==========================================================

    def validar_usuario_logado(self):

        if not self.usuario_logado:
            raise HTTPException(
                status_code=401,
                detail="Usuário não autenticado."
            )

    def validar_acesso_usuario(
        self,
        usuario_db: Usuarios
    ):

        self.validar_usuario_logado()

        perfil = self.usuario_logado.perfil

        if perfil == "Administrador":
            return

        if perfil == "Cliente":

            if usuario_db.id != self.usuario_logado.id:
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Você não possui acesso "
                        "a este usuário."
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

        usuario = self.repository.buscar_por_id(id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        self.validar_acesso_usuario(usuario)

        return usuario

    # ==========================================================
    # BUSCAR POR EMAIL
    # ==========================================================

    def buscar_por_email(self, email: str):

        email = self.normalizar_email(email)

        return self.repository.buscar_por_email(
            email
        )

    # ==========================================================
    # CRIAR USUÁRIO PÚBLICO
    # ==========================================================

    def criar(
        self,
        usuario: UsuarioCreate
    ):

        """
        Cadastro público.

        Sempre cria um usuário com perfil Cliente.
        """

        nome = self.normalizar_nome(
            usuario.nome
        )

        email = self.normalizar_email(
            usuario.email
        )

        if not nome:
            raise HTTPException(
                status_code=400,
                detail="Nome obrigatório."
            )

        if len(usuario.senha) < 6:
            raise HTTPException(
                status_code=400,
                detail=(
                    "A senha deve possuir "
                    "mínimo 6 caracteres."
                )
            )

        if self.repository.buscar_por_email(email):

            raise HTTPException(
                status_code=409,
                detail="Email já cadastrado."
            )

        novo_usuario = Usuarios(
            nome=nome,
            email=email,
            senha_hash=senha_context.hash(
                usuario.senha
            ),
            perfil="Cliente"
        )

        try:
            return self.repository.criar(
                novo_usuario
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar usuário."
            )

    # ==========================================================
    # CRIAR USUÁRIO POR ADMINISTRADOR
    # ==========================================================

    def criar_por_admin(
        self,
        usuario: UsuarioAdminCreate
    ):

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
                detail=(
                    "Somente Administrador "
                    "pode criar usuários."
                )
            )

        nome = self.normalizar_nome(
            usuario.nome
        )

        email = self.normalizar_email(
            usuario.email
        )

        perfil = self.normalizar_perfil(
            usuario.perfil
        )

        if not nome:
            raise HTTPException(
                status_code=400,
                detail="Nome obrigatório."
            )

        if len(usuario.senha) < 6:
            raise HTTPException(
                status_code=400,
                detail=(
                    "A senha deve possuir "
                    "mínimo 6 caracteres."
                )
            )

        if self.repository.buscar_por_email(email):

            raise HTTPException(
                status_code=409,
                detail="Email já cadastrado."
            )

        novo_usuario = Usuarios(
            nome=nome,
            email=email,
            senha_hash=senha_context.hash(
                usuario.senha
            ),
            perfil=perfil
        )

        try:
            return self.repository.criar(
                novo_usuario
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar usuário."
            )

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
        order: str = "asc"
    ):

        self.validar_usuario_logado()

        if self.usuario_logado.perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail=(
                    "Somente Administrador "
                    "pode listar usuários."
                )
            )

        if skip < 0:
            skip = 0

        if limit <= 0:
            limit = 10

        if limit > 100:
            limit = 100

        perfil_normalizado = None

        if perfil:
            perfil_normalizado = (
                self.normalizar_perfil(perfil)
            )

        return self.repository.listar(
            skip=skip,
            limit=limit,
            nome=(
                nome.strip()
                if nome
                else None
            ),
            email=(
                self.normalizar_email(email)
                if email
                else None
            ),
            perfil=perfil_normalizado,
            sort_by=sort_by,
            order=order
        )

    # ==========================================================
    # ATUALIZAR USUÁRIO
    # ==========================================================

    def atualizar(
        self,
        id: int,
        usuario: UsuarioUpdate
    ):

        usuario_db = self.repository.buscar_por_id(
            id
        )

        if not usuario_db:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        self.validar_acesso_usuario(
            usuario_db
        )

        dados = usuario.model_dump(
            exclude_unset=True
        )

        # ------------------------------------------------------
        # CLIENTE NÃO PODE ALTERAR PERFIL
        # ------------------------------------------------------

        if (
            "perfil" in dados
            and self.usuario_logado.perfil
            != "Administrador"
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Somente Administrador "
                    "pode alterar perfil."
                )
            )

        # ------------------------------------------------------
        # NOME
        # ------------------------------------------------------

        if "nome" in dados:

            nome = self.normalizar_nome(
                dados["nome"]
            )

            if not nome:
                raise HTTPException(
                    status_code=400,
                    detail="Nome obrigatório."
                )

            usuario_db.nome = nome

        # ------------------------------------------------------
        # EMAIL
        # ------------------------------------------------------

        if "email" in dados:

            email = self.normalizar_email(
                dados["email"]
            )

            if not email:
                raise HTTPException(
                    status_code=400,
                    detail="Email obrigatório."
                )

            existente = (
                self.repository.buscar_por_email(
                    email
                )
            )

            if (
                existente
                and existente.id != usuario_db.id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="Email já cadastrado."
                )

            usuario_db.email = email

        # ------------------------------------------------------
        # SENHA
        # ------------------------------------------------------

        if "senha" in dados:

            if len(dados["senha"]) < 6:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "A senha deve possuir "
                        "no mínimo 6 caracteres."
                    )
                )

            usuario_db.senha_hash = (
                senha_context.hash(
                    dados["senha"]
                )
            )

        # ------------------------------------------------------
        # PERFIL
        # ------------------------------------------------------

        if "perfil" in dados:

            if (
                self.usuario_logado.perfil
                != "Administrador"
            ):
                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Somente Administrador "
                        "pode alterar perfil."
                    )
                )

            usuario_db.perfil = (
                self.normalizar_perfil(
                    dados["perfil"]
                )
            )

        try:
            return self.repository.atualizar(
                usuario_db
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar usuário."
            )

    # ==========================================================
    # DELETAR USUÁRIO
    # ==========================================================

    def deletar(self, id: int):

        usuario_db = self.repository.buscar_por_id(
            id
        )

        if not usuario_db:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        self.validar_usuario_logado()

        if self.usuario_logado.perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail=(
                    "Somente Administrador "
                    "pode excluir usuários."
                )
            )

        # ------------------------------------------------------
        # IMPEDIR AUTOEXCLUSÃO
        # ------------------------------------------------------

        if usuario_db.id == self.usuario_logado.id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Administrador não pode "
                    "excluir o próprio usuário."
                )
            )

        try:
            self.repository.deletar(
                usuario_db
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro ao excluir usuário."
            )

