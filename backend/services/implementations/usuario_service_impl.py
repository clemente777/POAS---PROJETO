from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from backend.models.usuario_model import Usuarios
from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate
)


senha_context = PasswordHash.recommended()


class UsuarioServiceImpl:
    """
    Service responsável pelas regras de negócio
    dos usuários.

    Responsabilidades:

    - Validar cadastro
    - Criptografar senhas
    - Evitar emails duplicados
    - Buscar usuários
    - Atualizar dados
    - Remover usuários
    """

    def __init__(self, session: Session):
        """
        Recebe a sessão do banco.

        A sessão será utilizada para:

        - Consultas
        - Inserções
        - Atualizações
        - Exclusões
        """

        self.session = session


    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    def normalizar_email(self, email: str):
        """
        Padroniza o email.

        Exemplo:

        Entrada:

        JOAO@EMAIL.COM


        Saída:

        joao@email.com
        """

        if not email:
            return ""

        return email.lower().strip()



    # ==================================================
    # BUSCAS
    # ==================================================

    def buscar_por_id(self, id: int):
        """
        Busca usuário pelo ID.

        Retorna:

        Usuário encontrado

        ou

        None caso não exista.
        """

        return self.session.scalars(
            select(Usuarios)
            .where(
                Usuarios.id == id
            )
        ).first()



    def buscar_por_email(self, email: str):
        """
        Busca usuário pelo email.

        Usado para:

        - Login
        - Impedir emails duplicados
        """

        email = self.normalizar_email(email)

        return self.session.scalars(
            select(Usuarios)
            .where(
                Usuarios.email == email
            )
        ).first()



    # ==================================================
    # CRIAR USUÁRIO
    # ==================================================

    def criar(self, usuario: UsuarioCreate):
        """
        Cria um novo usuário.

        Regras:

        1 - Nome obrigatório

        2 - Email obrigatório

        3 - Senha mínima de 6 caracteres

        4 - Email não pode repetir

        5 - Senha deve ser armazenada criptografada
        """


        # Normalizar email

        email = self.normalizar_email(
            usuario.email
        )


        # Validar nome

        if not usuario.nome.strip():

            raise HTTPException(
                status_code=400,
                detail="Nome é obrigatório."
            )


        # Validar senha

        if len(usuario.senha) < 6:

            raise HTTPException(
                status_code=400,
                detail="A senha deve possuir no mínimo 6 caracteres."
            )


        # Verificar email existente

        usuario_existente = self.buscar_por_email(
            email
        )


        if usuario_existente:

            raise HTTPException(
                status_code=409,
                detail="Email já cadastrado."
            )


        # Criar usuário

        db = Usuarios(
            nome=usuario.nome.strip(),
            email=email,
            senha_hash=senha_context.hash(
                usuario.senha
            )
        )


        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db



    # ==================================================
    # LISTAR USUÁRIOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        email: str | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):
        """
        Lista usuários.

        Recursos:

        - Paginação
        - Filtro por nome
        - Filtro por email
        - Ordenação
        """


        query = select(Usuarios)


        # Filtro por nome

        if nome:

            query = query.where(
                Usuarios.nome.ilike(
                    f"%{nome}%"
                )
            )


        # Filtro por email

        if email:

            query = query.where(
                Usuarios.email.ilike(
                    f"%{email}%"
                )
            )


        # Campos permitidos para ordenar

        campos = {

            "id": Usuarios.id,

            "nome": Usuarios.nome,

            "email": Usuarios.email,

            "criado_em": Usuarios.criado_em

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


        # Paginação

        query = (
            query
            .offset(skip)
            .limit(limit)
        )


        return self.session.scalars(
            query
        ).all()
    
        # ==================================================
    # ATUALIZAR USUÁRIO
    # ==================================================

    def atualizar(
        self,
        id: int,
        usuario: UsuarioUpdate
    ):
        """
        Atualiza um usuário existente.

        Permite atualização parcial.

        Exemplo:

        Entrada:

        {
            "nome":"João"
        }


        Apenas o nome será alterado.

        Os outros campos permanecem iguais.
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )


        # Pega somente os campos enviados

        dados = usuario.model_dump(
            exclude_unset=True
        )


        # ==================================================
        # VALIDAR NOME
        # ==================================================

        if "nome" in dados:

            if not dados["nome"].strip():

                raise HTTPException(
                    status_code=400,
                    detail="Nome é obrigatório."
                )


            dados["nome"] = dados["nome"].strip()



        # ==================================================
        # VALIDAR EMAIL
        # ==================================================

        if "email" in dados:


            email = self.normalizar_email(
                dados["email"]
            )


            usuario_existente = self.buscar_por_email(
                email
            )


            if usuario_existente and usuario_existente.id != id:

                raise HTTPException(
                    status_code=409,
                    detail="Email já cadastrado."
                )


            dados["email"] = email



        # ==================================================
        # VALIDAR SENHA
        # ==================================================

        if "senha" in dados:


            if len(dados["senha"]) < 4:

                raise HTTPException(
                    status_code=400,
                    detail=
                    "A senha deve possuir no mínimo 6 caracteres."
                )


            """
            A senha nunca é salva
            diretamente no banco.

            Exemplo:

            Entrada:

            123456


            Banco:

            $argon2id$v=19$...
            """


            db.senha_hash = senha_context.hash(
                dados["senha"]
            )


            # Remove senha normal
            # para não tentar salvar
            # no banco

            del dados["senha"]



        # ==================================================
        # APLICAR ALTERAÇÕES
        # ==================================================

        for campo, valor in dados.items():

            setattr(
                db,
                campo,
                valor
            )


        self.session.commit()

        self.session.refresh(db)


        return db




    # ==================================================
    # DELETAR USUÁRIO
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        """
        Remove um usuário.

        Regras:

        1 - Usuário precisa existir

        2 - Caso exista,
            remove do banco
        """


        db = self.buscar_por_id(
            id
        )


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )


        self.session.delete(
            db
        )


        self.session.commit()


        return {
            "message":
            "Usuário removido com sucesso."
        }