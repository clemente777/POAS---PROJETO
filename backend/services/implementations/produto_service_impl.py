from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.produto_model import Produtos

from backend.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoUpdate
)


class ProdutoServiceImpl:
    """
    Service responsável pelas regras de negócio
    dos produtos.

    Responsabilidades:

    - Validar cadastro de produtos
    - Controlar preços
    - Controlar estoque
    - Evitar produtos duplicados
    - Atualizar produtos com segurança
    - Realizar buscas e filtros
    """

    def __init__(
        self,
        session: Session
    ):
        """
        Recebe a sessão do banco.
        """

        self.session = session


    # ==================================================
    # BUSCAS
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        """
        Busca produto pelo ID.
        """

        return self.session.scalars(
            select(Produtos)
            .where(Produtos.id == id)
        ).first()


    def buscar_por_nome(
        self,
        nome: str
    ):
        """
        Busca produto pelo nome.
        """

        return self.session.scalars(
            select(Produtos)
            .where(
                Produtos.nome.ilike(nome)
            )
        ).first()


    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    def normalizar_nome(
        self,
        nome: str
    ):
        """
        Remove espaços extras do nome.
        """

        return nome.strip()


    # ==================================================
    # VALIDAÇÕES
    # ==================================================

    def validar_nome(
        self,
        nome: str
    ):
        """
        Valida nome do produto.
        """

        if not nome.strip():

            raise HTTPException(
                status_code=400,
                detail="Nome do produto é obrigatório."
            )


    def validar_preco(
        self,
        preco: float
    ):
        """
        Valida preço do produto.
        """

        if preco <= 0:

            raise HTTPException(
                status_code=400,
                detail="Preço deve ser maior que zero."
            )


    def validar_estoque(
        self,
        estoque: int
    ):
        """
        Valida quantidade em estoque.
        """

        if estoque < 0:

            raise HTTPException(
                status_code=400,
                detail="Estoque não pode ser negativo."
            )


    def verificar_estoque_baixo(
        self,
        estoque: int
    ):
        """
        Retorna True quando o estoque
        está igual ou menor que 5.
        """

        return estoque <= 5


    # ==================================================
    # CRIAR PRODUTO
    # ==================================================

    def criar(
        self,
        produto: ProdutoCreate
    ):
        """
        Cria um novo produto.

        Regras:

        - Nome obrigatório
        - Nome normalizado
        - Produto não duplicado
        - Preço válido
        - Estoque válido
        """


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


        produto_existente = self.buscar_por_nome(
            nome
        )


        if produto_existente:

            raise HTTPException(
                status_code=409,
                detail="Produto já cadastrado."
            )


        dados = produto.model_dump()


        dados["nome"] = nome


        db = Produtos(
            **dados
        )


        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db
    
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
        order: str = "asc",
    ):
        """
        Lista produtos cadastrados.

        Possui:

        - Paginação
        - Filtros
        - Ordenação
        """


        query = select(Produtos)


        # ==================================================
        # FILTROS
        # ==================================================

        if nome:

            query = query.where(
                Produtos.nome.ilike(
                    f"%{nome}%"
                )
            )


        if descricao:

            query = query.where(
                Produtos.descricao.ilike(
                    f"%{descricao}%"
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


        if em_estoque:

            query = query.where(
                Produtos.estoque > 0
            )


        # ==================================================
        # ORDENAÇÃO
        # ==================================================

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


        # ==================================================
        # PAGINAÇÃO
        # ==================================================

        query = (
            query
            .offset(skip)
            .limit(limit)
        )


        return self.session.scalars(query).all()



    # ==================================================
    # ATUALIZAR PRODUTO
    # ==================================================

    def atualizar(
        self,
        id: int,
        produto: ProdutoUpdate
    ):
        """
        Atualiza um produto.

        Permite alteração parcial.
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )


        dados = produto.model_dump(
            exclude_unset=True
        )


        # ==================================================
        # VALIDAR NOME
        # ==================================================

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
                    detail="Produto já cadastrado."
                )


            dados["nome"] = nome


        # ==================================================
        # VALIDAR PREÇO
        # ==================================================

        if "preco" in dados:

            self.validar_preco(
                dados["preco"]
            )


        # ==================================================
        # VALIDAR ESTOQUE
        # ==================================================

        if "estoque" in dados:

            self.validar_estoque(
                dados["estoque"]
            )


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
    # DELETAR PRODUTO
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        """
        Remove um produto.

        Regra:

        Produto usado em carrinho
        não pode ser removido.
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )


        if db.itens_carrinho:

            raise HTTPException(
                status_code=409,
                detail="Produto possui registros no carrinho."
            )


        self.session.delete(db)

        self.session.commit()


        return True