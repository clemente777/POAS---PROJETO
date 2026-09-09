from fastapi import HTTPException
from pwdlib import PasswordHash

from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes

from backend.schemas.cadastro_schema import CadastroCreate

from backend.repositories.cadastro_repository import (
    CadastroRepository
)


senha_context = PasswordHash.recommended()


class CadastroServiceImpl:
    """
    ==========================================================
                    SERVICE DE CADASTRO
    ==========================================================

    Responsável pelas regras de negócio do cadastro público.

    Regras:

    - Todo cadastro público possui perfil Cliente.
    - Email deve ser único.
    - CPF deve ser único.
    - CPF deve ser válido.
    - Telefone deve ser válido.
    - Nome deve ser válido.
    - Endereço é obrigatório.
    - Senha mínima de 6 caracteres.
    - Usuário e Cliente são criados em uma única transação.
    """

    def __init__(
        self,
        repository: CadastroRepository
    ):

        self.repository = repository

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        dados: CadastroCreate
    ):

        try:

            # --------------------------------------------------
            # NORMALIZAÇÕES
            # --------------------------------------------------

            nome = self.normalizar_nome(
                dados.nome
            )

            email = self.normalizar_email(
                dados.email
            )

            cpf = self.normalizar_cpf(
                dados.cpf
            )

            telefone = self.normalizar_telefone(
                dados.telefone
            )

            endereco = dados.endereco.strip()

            # --------------------------------------------------
            # VALIDAÇÕES
            # --------------------------------------------------

            self.validar_nome(
                nome
            )

            self.validar_email(
                email
            )

            self.validar_cpf(
                cpf
            )

            self.validar_telefone(
                telefone
            )

            self.validar_senha(
                dados.senha
            )

            if not endereco:

                raise HTTPException(
                    status_code=400,
                    detail="Endereço obrigatório."
                )

            # --------------------------------------------------
            # VERIFICAR EMAIL
            # --------------------------------------------------

            usuario_existente = (
                self.repository
                .buscar_usuario_por_email(
                    email
                )
            )

            if usuario_existente:

                raise HTTPException(
                    status_code=409,
                    detail="Email já cadastrado."
                )

            # --------------------------------------------------
            # VERIFICAR CPF
            # --------------------------------------------------

            cliente_existente = (
                self.repository
                .buscar_cliente_por_cpf(
                    cpf
                )
            )

            if cliente_existente:

                raise HTTPException(
                    status_code=409,
                    detail="CPF já cadastrado."
                )

            # --------------------------------------------------
            # CRIAR USUÁRIO
            # --------------------------------------------------

            usuario = Usuarios(
                nome=nome,
                email=email,
                senha_hash=senha_context.hash(
                    dados.senha
                ),
                perfil="Cliente"
            )

            usuario = (
                self.repository
                .criar_usuario(
                    usuario
                )
            )

            # --------------------------------------------------
            # CRIAR CLIENTE
            # --------------------------------------------------

            cliente = Clientes(
                nome=nome,
                cpf=cpf,
                telefone=telefone,
                email=email,
                endereco=endereco,
                usuario_id=usuario.id
            )

            cliente = (
                self.repository
                .criar_cliente(
                    cliente
                )
            )

            # --------------------------------------------------
            # FINALIZAR TRANSAÇÃO
            # --------------------------------------------------

            return (
                self.repository
                .finalizar_cadastro(
                    usuario,
                    cliente
                )
            )

        except HTTPException:

            self.repository.rollback()

            raise

        except Exception as erro:

            self.repository.rollback()

            print(
                "Erro no cadastro:",
                erro
            )

            raise HTTPException(
                status_code=500,
                detail="Erro ao realizar cadastro."
            )

    # ==========================================================
    # NORMALIZAR NOME
    # ==========================================================

    def normalizar_nome(
        self,
        nome: str
    ):

        if not nome:
            return ""

        return " ".join(
            nome.strip().split()
        ).title()

    # ==========================================================
    # NORMALIZAR EMAIL
    # ==========================================================

    def normalizar_email(
        self,
        email: str
    ):

        if not email:
            return ""

        return email.strip().lower()

    # ==========================================================
    # NORMALIZAR CPF
    # ==========================================================

    def normalizar_cpf(
        self,
        cpf: str
    ):

        if not cpf:
            return ""

        return (
            cpf
            .replace(".", "")
            .replace("-", "")
            .strip()
        )

    # ==========================================================
    # NORMALIZAR TELEFONE
    # ==========================================================

    def normalizar_telefone(
        self,
        telefone: str
    ):

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
    # VALIDAR NOME
    # ==========================================================

    def validar_nome(
        self,
        nome: str
    ):

        if len(nome) < 3:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Nome deve possuir pelo menos "
                    "3 caracteres."
                )
            )

    # ==========================================================
    # VALIDAR EMAIL
    # ==========================================================

    def validar_email(
        self,
        email: str
    ):

        if "@" not in email:

            raise HTTPException(
                status_code=400,
                detail="Email inválido."
            )

        parte_dominio = email.split("@")[-1]

        if "." not in parte_dominio:

            raise HTTPException(
                status_code=400,
                detail="Email inválido."
            )

    # ==========================================================
    # VALIDAR SENHA
    # ==========================================================

    def validar_senha(
        self,
        senha: str
    ):

        if len(senha) < 6:

            raise HTTPException(
                status_code=400,
                detail=(
                    "A senha deve possuir no mínimo "
                    "6 caracteres."
                )
            )

    # ==========================================================
    # VALIDAR TELEFONE
    # ==========================================================

    def validar_telefone(
        self,
        telefone: str
    ):

        if not telefone.isdigit():

            raise HTTPException(
                status_code=400,
                detail="Telefone inválido."
            )

        if len(telefone) not in [10, 11]:

            raise HTTPException(
                status_code=400,
                detail="Telefone inválido."
            )

    # ==========================================================
    # VALIDAR CPF
    # ==========================================================

    def validar_cpf(
        self,
        cpf: str
    ):

        # ------------------------------------------------------
        # Quantidade de dígitos
        # ------------------------------------------------------

        if len(cpf) != 11:

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )

        # ------------------------------------------------------
        # Verifica se todos os caracteres são números
        # ------------------------------------------------------

        if not cpf.isdigit():

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )

        # ------------------------------------------------------
        # Verifica CPFs com números repetidos
        # ------------------------------------------------------

        if cpf == cpf[0] * 11:

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )

        # ------------------------------------------------------
        # PRIMEIRO DÍGITO
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # SEGUNDO DÍGITO
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # COMPARAR DÍGITOS
        # ------------------------------------------------------

        if (
            int(cpf[9]) != digito1
            or
            int(cpf[10]) != digito2
        ):

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )

