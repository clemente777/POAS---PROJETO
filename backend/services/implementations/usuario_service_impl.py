from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from backend.models.usuario_model import Usuarios

from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioAdminCreate
)


senha_context = PasswordHash.recommended()



class UsuarioServiceImpl:
    """
    ==========================================================
                    SERVICE DE USUÁRIOS
    ==========================================================

    Responsável pelas regras de negócio dos usuários.

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
        session: Session
    ):

        self.session = session



    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================


    def normalizar_email(
        self,
        email: str
    ):

        if not email:

            return ""


        return email.strip().lower()



    def normalizar_nome(
        self,
        nome: str
    ):

        if not nome:

            return ""


        return " ".join(
            nome.strip().split()
        ).title()



    def normalizar_perfil(
        self,
        perfil: str
    ):

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

            "administrador":
            "Administrador",

            "admin":
            "Administrador",

            "veterinario":
            "Veterinário",

            "veterinário":
            "Veterinário",

            "vet":
            "Veterinário",

            "cliente":
            "Cliente"

        }


        if perfil not in perfis:

            raise HTTPException(
                status_code=400,
                detail="Perfil inválido."
            )


        return perfis[perfil]
    
        # ==========================================================
    # BUSCAS
    # ==========================================================


    def buscar_por_id(
        self,
        id: int
    ):

        return self.session.scalar(

            select(Usuarios)
            .where(
                Usuarios.id == id
            )

        )



    def buscar_por_email(
        self,
        email: str
    ):

        email = self.normalizar_email(
            email
        )


        return self.session.scalar(

            select(Usuarios)
            .where(
                Usuarios.email == email
            )

        )



    # ==========================================================
    # CONTROLE DE PERMISSÃO
    # ==========================================================


    def validar_acesso_usuario(
        self,
        usuario_db: Usuarios,
        usuario_logado: Usuarios
    ):

        """
        Regras:

        Administrador:
            acesso total.

        Cliente:
            somente própria conta.

        Veterinário:
            sem acesso.
        """


        if usuario_logado.perfil == "Administrador":

            return True



        if usuario_logado.perfil == "Cliente":


            if usuario_db.id != usuario_logado.id:


                raise HTTPException(

                    status_code=403,

                    detail=(
                        "Você não possui "
                        "acesso a este usuário."
                    )

                )


            return True



        raise HTTPException(

            status_code=403,

            detail="Perfil sem permissão."

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

        Sempre cria:

        Cliente
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



        if self.buscar_por_email(email):

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



        self.session.add(
            novo_usuario
        )


        self.session.commit()


        self.session.refresh(
            novo_usuario
        )


        return novo_usuario
    
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



        if self.buscar_por_email(email):

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



        self.session.add(
            novo_usuario
        )


        self.session.commit()


        self.session.refresh(
            novo_usuario
        )


        return novo_usuario





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

        """
        Lista usuários.

        Apenas Administrador.

        Recursos:

        • Paginação
        • Filtros
        • Ordenação
        """


        limit = min(
            limit,
            100
        )


        query = select(
            Usuarios
        )



        if nome:

            query = query.where(

                Usuarios.nome.ilike(

                    f"%{nome}%"

                )

            )



        if email:

            query = query.where(

                Usuarios.email.ilike(

                    f"%{email}%"

                )

            )



        if perfil:

            perfil = self.normalizar_perfil(
                perfil
            )


            query = query.where(

                Usuarios.perfil == perfil

            )



        campos = {


            "id":

            Usuarios.id,


            "nome":

            Usuarios.nome,


            "email":

            Usuarios.email,


            "perfil":

            Usuarios.perfil,


            "criado_em":

            Usuarios.criado_em

        }



        coluna = campos.get(

            sort_by,

            Usuarios.id

        )



        if order.lower() == "desc":


            query = query.order_by(

                desc(coluna)

            )

        else:


            query = query.order_by(

                asc(coluna)

            )



        query = (

            query

            .offset(skip)

            .limit(limit)

        )



        return self.session.scalars(
            query
        ).all()
        
        # ==========================================================
    # ATUALIZAR USUÁRIO
    # ==========================================================

    def atualizar(
        self,
        id: int,
        usuario: UsuarioUpdate,
        usuario_logado: Usuarios
    ):
        """
        Atualiza usuário.

        Regras:

        • Administrador pode alterar qualquer usuário.
        • Usuário comum não altera perfil.
        • Cliente não altera outro usuário.
        • Email continua único.
        • Senha é sempre criptografada.
        """


        usuario_db = self.buscar_por_id(id)


        if not usuario_db:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )



        # ======================================================
        # CONTROLE DE PERMISSÃO
        # ======================================================

        if usuario_logado.perfil != "Administrador":


            if usuario_db.id != usuario_logado.id:

                raise HTTPException(
                    status_code=403,
                    detail="Você não pode alterar outro usuário."
                )



            dados = usuario.model_dump(
                exclude_unset=True
            )


            if "perfil" in dados:

                raise HTTPException(
                    status_code=403,
                    detail="Você não pode alterar seu perfil."
                )

        else:

            dados = usuario.model_dump(
                exclude_unset=True
            )



        # ======================================================
        # NOME
        # ======================================================

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



        # ======================================================
        # EMAIL
        # ======================================================

        if "email" in dados:

            email = self.normalizar_email(
                dados["email"]
            )


            existente = self.buscar_por_email(
                email
            )


            if existente and existente.id != id:

                raise HTTPException(
                    status_code=409,
                    detail="Email já cadastrado."
                )


            usuario_db.email = email



        # ======================================================
        # SENHA
        # ======================================================

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



        # ======================================================
        # PERFIL
        # ======================================================

        if "perfil" in dados:


            if usuario_logado.perfil != "Administrador":

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



        self.session.commit()


        self.session.refresh(
            usuario_db
        )


        return usuario_db






    # ==========================================================
    # DELETAR USUÁRIO
    # ==========================================================

    def deletar(
        self,
        id: int,
        usuario_logado: Usuarios
    ):
        """
        Remove usuário.

        Regras:

        • Apenas Administrador exclui usuários.
        • Não permite excluir a si mesmo.
        • Usuário precisa existir.
        """


        usuario_db = self.buscar_por_id(
            id
        )


        if not usuario_db:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )



        # ======================================================
        # IMPEDIR AUTOEXCLUSÃO
        # ======================================================

        if usuario_db.id == usuario_logado.id:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Administrador não pode "
                    "excluir o próprio usuário."
                )
            )



        self.session.delete(
            usuario_db
        )


        self.session.commit()



        return {
            "message":
            "Usuário removido com sucesso."
        }