from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.produto_model import Produtos
from backend.models.usuario_model import Usuarios

from backend.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoUpdate
)


class ProdutoServiceImpl:

    """
    Service responsável pelas regras
    de negócio dos produtos.

    Regras:

    - Apenas Administrador cadastra produto.
    - Apenas Administrador altera produto.
    - Apenas Administrador exclui produto.
    - Nome não pode duplicar.
    - Preço deve ser maior que zero.
    - Estoque não pode ser negativo.
    - Produto usado em carrinho não pode ser excluído.
    """


    def __init__(
        self,
        session: Session,
        usuario_logado: Usuarios
    ):

        self.session = session
        self.usuario_logado = usuario_logado



    # ==================================================
    # PERMISSÃO
    # ==================================================

    def validar_admin(self):

        perfil = None


        if self.usuario_logado.perfil:

            if hasattr(
                self.usuario_logado.perfil,
                "nome"
            ):

                perfil = self.usuario_logado.perfil

            else:

                perfil = self.usuario_logado.perfil


        if perfil != "Administrador":

            raise HTTPException(
                status_code=403,
                detail=
                "Apenas administrador pode gerenciar produtos."
            )



    # ==================================================
    # BUSCAS
    # ==================================================


    def buscar_por_id(
        self,
        id: int
    ):

        produto = self.session.scalar(

            select(Produtos)
            .where(
                Produtos.id == id
            )

        )


        if not produto:

            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )


        return produto



    def buscar_por_nome(
        self,
        nome: str
    ):

        return self.session.scalar(

            select(Produtos)
            .where(
                Produtos.nome == nome
            )

        )



    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================


    def normalizar_nome(
        self,
        nome: str
    ):

        return nome.strip().title()



    # ==================================================
    # VALIDAÇÕES
    # ==================================================


    def validar_nome(
        self,
        nome: str
    ):


        if not nome or not nome.strip():

            raise HTTPException(
                status_code=400,
                detail="Nome do produto obrigatório."
            )


        if len(nome.strip()) < 3:

            raise HTTPException(
                status_code=400,
                detail=
                "Nome deve possuir no mínimo 3 caracteres."
            )



    def validar_preco(
        self,
        preco: float
    ):

        if preco <= 0:

            raise HTTPException(
                status_code=400,
                detail=
                "Preço deve ser maior que zero."
            )



    def validar_estoque(
        self,
        estoque: int
    ):

        if estoque < 0:

            raise HTTPException(
                status_code=400,
                detail=
                "Estoque não pode ser negativo."
            )
        # ==================================================
    # CRIAR PRODUTO
    # ==================================================

    def criar(
        self,
        produto: ProdutoCreate
    ):


        self.validar_admin()


        nome = self.normalizar_nome(
            produto.nome
        )


        self.validar_nome(
            nome
        )


        self.validar_preco(
            produto.preco
        )


        self.validar_estoque(
            produto.estoque
        )


        existente = self.buscar_por_nome(
            nome
        )


        if existente:

            raise HTTPException(
                status_code=409,
                detail="Produto já cadastrado."
            )



        dados = produto.model_dump()


        dados["nome"] = nome



        novo_produto = Produtos(

            **dados

        )


        try:


            self.session.add(
                novo_produto
            )


            self.session.commit()


            self.session.refresh(
                novo_produto
            )


            return novo_produto



        except Exception:


            self.session.rollback()


            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao cadastrar produto."

            )



    # ==================================================
    # LISTAR PRODUTOS
    # ==================================================


    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        descricao: str | None = None,
        preco_min: float | None = None,
        preco_max: float | None = None,
        estoque_min: int | None = None,
        estoque_max: int | None = None,
        em_estoque: bool | None = None,
        sort_by: str = "nome",
        order: str = "asc"
    ):



        query = select(
            Produtos
        )



        # ==============================
        # FILTROS
        # ==============================


        if nome:

            query = query.where(

                Produtos.nome.ilike(
                    f"%{nome.strip()}%"
                )

            )



        if descricao:

            query = query.where(

                Produtos.descricao.ilike(
                    f"%{descricao.strip()}%"
                )

            )



        if preco_min is not None:

            query = query.where(

                Produtos.preco >= preco_min

            )



        if preco_max is not None:

            query = query.where(

                Produtos.preco <= preco_max

            )



        if estoque_min is not None:

            query = query.where(

                Produtos.estoque >= estoque_min

            )



        if estoque_max is not None:

            query = query.where(

                Produtos.estoque <= estoque_max

            )



        if em_estoque is True:

            query = query.where(

                Produtos.estoque > 0

            )



        if em_estoque is False:

            query = query.where(

                Produtos.estoque == 0

            )



        # ==============================
        # ORDENAÇÃO
        # ==============================


        campos = {

            "id":
            Produtos.id,


            "nome":
            Produtos.nome,


            "descricao":
            Produtos.descricao,


            "preco":
            Produtos.preco,


            "estoque":
            Produtos.estoque

        }



        coluna = campos.get(

            sort_by,

            Produtos.nome

        )



        if order.lower() == "desc":


            query = query.order_by(

                desc(coluna)

            )


        else:


            query = query.order_by(

                asc(coluna)

            )



        # ==============================
        # PAGINAÇÃO
        # ==============================


        if skip < 0:

            skip = 0



        if limit <= 0:

            limit = 10



        if limit > 100:

            limit = 100



        query = (

            query

            .offset(skip)

            .limit(limit)

        )



        return self.session.scalars(

            query

        ).all()
    
        # ==================================================
    # ATUALIZAR PRODUTO
    # ==================================================

    def atualizar(
        self,
        id: int,
        produto: ProdutoUpdate
    ):


        self.validar_admin()



        db = self.buscar_por_id(
            id
        )



        dados = produto.model_dump(
            exclude_unset=True
        )



        # ==============================
        # VALIDAR NOME
        # ==============================


        if "nome" in dados:


            nome = self.normalizar_nome(

                dados["nome"]

            )


            self.validar_nome(

                nome

            )



            existente = self.buscar_por_nome(

                nome

            )


            if existente and existente.id != id:


                raise HTTPException(

                    status_code=409,

                    detail=
                    "Produto já cadastrado."

                )



            dados["nome"] = nome




        # ==============================
        # VALIDAR PREÇO
        # ==============================


        if "preco" in dados:


            self.validar_preco(

                dados["preco"]

            )




        # ==============================
        # VALIDAR ESTOQUE
        # ==============================


        if "estoque" in dados:


            self.validar_estoque(

                dados["estoque"]

            )




        try:


            for campo, valor in dados.items():


                setattr(

                    db,

                    campo,

                    valor

                )



            self.session.commit()


            self.session.refresh(

                db

            )



            return db



        except Exception:


            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao atualizar produto."

            )





    # ==================================================
    # DELETAR PRODUTO
    # ==================================================

    def deletar(
        self,
        id: int
    ):


        self.validar_admin()



        produto = self.buscar_por_id(

            id

        )



        if hasattr(produto, "itens_carrinho"):


            if produto.itens_carrinho:


                raise HTTPException(

                    status_code=409,

                    detail=
                    "Produto possui registros no carrinho e não pode ser excluído."

                )



        try:


            self.session.delete(

                produto

            )


            self.session.commit()



            return True



        except Exception:


            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao excluir produto."

            )