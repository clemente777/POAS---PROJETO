from fastapi import HTTPException

from backend.models.produto_model import Produtos
from backend.models.usuario_model import Usuarios

from backend.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoUpdate
)

from backend.repositories.produto_repository import (
    ProdutoRepository
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
        repository: ProdutoRepository,
        usuario_logado: Usuarios
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==================================================
    # PERMISSÃO
    # ==================================================

    def validar_admin(self):

        perfil = self.usuario_logado.perfil

        if hasattr(perfil, "nome"):
            perfil = perfil.nome

        if perfil != "Administrador":
            raise HTTPException(
                status_code=403,
                detail=(
                    "Apenas administrador pode "
                    "gerenciar produtos."
                )
            )

    # ==================================================
    # BUSCAR PRODUTO POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):

        produto = self.repository.buscar_por_id(
            id
        )

        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )

        return produto

    # ==================================================
    # BUSCAR PRODUTO POR NOME
    # ==================================================

    def buscar_por_nome(
        self,
        nome: str
    ):

        return self.repository.buscar_por_nome(
            nome
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
    # VALIDAR NOME
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
                detail=(
                    "Nome deve possuir no mínimo "
                    "3 caracteres."
                )
            )

    # ==================================================
    # VALIDAR PREÇO
    # ==================================================

    def validar_preco(
        self,
        preco: float
    ):

        if preco <= 0:
            raise HTTPException(
                status_code=400,
                detail="Preço deve ser maior que zero."
            )

    # ==================================================
    # VALIDAR ESTOQUE
    # ==================================================

    def validar_estoque(
        self,
        estoque: int
    ):

        if estoque < 0:
            raise HTTPException(
                status_code=400,
                detail="Estoque não pode ser negativo."
            )

    # ==================================================
    # CRIAR PRODUTO
    # ==================================================

    def criar(
        self,
        produto: ProdutoCreate
    ):

        self.validar_admin()

        # --------------------------------------------------
        # NORMALIZAR NOME
        # --------------------------------------------------

        nome = self.normalizar_nome(
            produto.nome
        )

        # --------------------------------------------------
        # VALIDAR DADOS
        # --------------------------------------------------

        self.validar_nome(
            nome
        )

        self.validar_preco(
            produto.preco
        )

        self.validar_estoque(
            produto.estoque
        )

        # --------------------------------------------------
        # VERIFICAR DUPLICIDADE
        # --------------------------------------------------

        existente = self.buscar_por_nome(
            nome
        )

        if existente:
            raise HTTPException(
                status_code=409,
                detail="Produto já cadastrado."
            )

        # --------------------------------------------------
        # CRIAR PRODUTO
        # --------------------------------------------------

        dados = produto.model_dump()

        dados["nome"] = nome

        novo_produto = Produtos(
            **dados
        )

        try:
            return self.repository.criar(
                novo_produto
            )

        except Exception:
            self.repository.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao cadastrar produto."
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

        return self.repository.listar(
            skip=skip,
            limit=limit,
            nome=nome,
            descricao=descricao,
            preco_min=preco_min,
            preco_max=preco_max,
            estoque_min=estoque_min,
            estoque_max=estoque_max,
            em_estoque=em_estoque,
            sort_by=sort_by,
            order=order
        )

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

        # --------------------------------------------------
        # VERIFICAR SE EXISTEM DADOS
        # --------------------------------------------------

        if not dados:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Nenhum dado foi informado "
                    "para atualização."
                )
            )

        # --------------------------------------------------
        # VALIDAR NOME
        # --------------------------------------------------

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

            if (
                existente
                and existente.id != id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="Produto já cadastrado."
                )

            dados["nome"] = nome

        # --------------------------------------------------
        # VALIDAR PREÇO
        # --------------------------------------------------

        if "preco" in dados:
            self.validar_preco(
                dados["preco"]
            )

        # --------------------------------------------------
        # VALIDAR ESTOQUE
        # --------------------------------------------------

        if "estoque" in dados:
            self.validar_estoque(
                dados["estoque"]
            )

        # --------------------------------------------------
        # APLICAR ALTERAÇÕES
        # --------------------------------------------------

        for campo, valor in dados.items():
            setattr(
                db,
                campo,
                valor
            )

        try:
            return self.repository.atualizar(
                db
            )

        except Exception:
            self.repository.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar produto."
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

        # --------------------------------------------------
        # VERIFICAR SE O PRODUTO ESTÁ EM ALGUM CARRINHO
        # --------------------------------------------------

        if hasattr(
            produto,
            "itens_carrinho"
        ):

            if produto.itens_carrinho:

                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Produto possui registros "
                        "no carrinho e não pode ser excluído."
                    )
                )

        try:
            return self.repository.deletar(
                produto
            )

        except Exception:
            self.repository.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao excluir produto."
            )
