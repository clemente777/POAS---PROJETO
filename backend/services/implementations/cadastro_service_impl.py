from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes

from backend.schemas.cadastro_schema import CadastroCreate


senha_context = PasswordHash.recommended()


class CadastroServiceImpl:

    """
    ==========================================================
                    SERVICE DE CADASTRO
    ==========================================================

    Responsável pelo cadastro público do sistema.

    Regras:

    • Cria Usuário e Cliente em uma única transação.
    • Todo cadastro público possui perfil Cliente.
    • Email deve ser único.
    • CPF deve ser único.
    • CPF válido.
    • Telefone válido.
    • Nome válido.
    • Senha mínima de 6 caracteres.
    • Caso ocorra qualquer erro, toda operação é desfeita.
    """

    def __init__(
        self,
        session: Session
    ):

        self.session = session

    # ==========================================================
    # CADASTRO
    # ==========================================================

    def cadastrar(
        self,
        dados: CadastroCreate
    ):

        try:

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

            self.validar_nome(nome)
            self.validar_email(email)
            self.validar_cpf(cpf)
            self.validar_telefone(telefone)
            self.validar_senha(dados.senha)

            if not endereco:

                raise HTTPException(
                    status_code=400,
                    detail="Endereço obrigatório."
                )
                        # ==========================================================
            # VERIFICAR EMAIL
            # ==========================================================

            usuario_existente = self.session.scalar(

                select(Usuarios)

                .where(
                    Usuarios.email == email
                )

            )

            if usuario_existente:

                raise HTTPException(
                    status_code=409,
                    detail="Email já cadastrado."
                )


            # ==========================================================
            # VERIFICAR CPF
            # ==========================================================

            cliente_existente = self.session.scalar(

                select(Clientes)

                .where(
                    Clientes.cpf == cpf
                )

            )

            if cliente_existente:

                raise HTTPException(
                    status_code=409,
                    detail="CPF já cadastrado."
                )


            # ==========================================================
            # CRIAR USUÁRIO
            # ==========================================================

            usuario = Usuarios(

                nome=nome,

                email=email,

                senha_hash=senha_context.hash(
                    dados.senha
                ),

                perfil="Cliente"

            )


            self.session.add(usuario)


            # gera o ID do usuário sem fazer commit
            self.session.flush()


            # ==========================================================
            # CRIAR CLIENTE
            # ==========================================================

            cliente = Clientes(

                nome=nome,

                cpf=cpf,

                telefone=telefone,

                email=email,

                endereco=endereco,

                usuario_id=usuario.id

            )


            self.session.add(cliente)


            # ==========================================================
            # SALVAR TUDO
            # ==========================================================

            self.session.commit()

            self.session.refresh(usuario)

            self.session.refresh(cliente)


            return usuario, cliente


        except HTTPException:

            self.session.rollback()

            raise


        except Exception as e:

            self.session.rollback()

            print("Erro no cadastro:", e)

            raise HTTPException(
                status_code=500,
                detail="Erro ao realizar cadastro."
            )
        # ==========================================================
    # NORMALIZAÇÕES
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


    def normalizar_email(
        self,
        email: str
    ):

        if not email:

            return ""

        return email.strip().lower()


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
    # VALIDAÇÕES
    # ==========================================================

    def validar_nome(
        self,
        nome: str
    ):

        if len(nome) < 3:

            raise HTTPException(
                status_code=400,
                detail="Nome deve possuir pelo menos 3 caracteres."
            )


    def validar_email(
        self,
        email: str
    ):

        if "@" not in email:

            raise HTTPException(
                status_code=400,
                detail="Email inválido."
            )


        if "." not in email.split("@")[-1]:

            raise HTTPException(
                status_code=400,
                detail="Email inválido."
            )


    def validar_senha(
        self,
        senha: str
    ):

        if len(senha) < 6:

            raise HTTPException(
                status_code=400,
                detail="A senha deve possuir no mínimo 6 caracteres."
            )


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


    def validar_cpf(
        self,
        cpf: str
    ):

        if len(cpf) != 11:

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )


        if cpf == cpf[0] * 11:

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

            or

            int(cpf[10]) != digito2

        ):

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )