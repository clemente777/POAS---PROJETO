from fastapi import HTTPException

from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.carrinho_model import Carrinhos
from backend.models.usuario_model import Usuarios

from backend.schemas.item_carrinho_schema import (
    ItemCarrinhoCreate,
    ItemCarrinhoUpdate
)

from backend.repositories.item_carrinho_repository import (
    ItemCarrinhoRepository
)


class ItemCarrinhoServiceImpl:

    def __init__(
        self,
        repository: ItemCarrinhoRepository,
        usuario_logado: Usuarios
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==================================================
    # VALIDAR PERFIL
    # ==================================================

    def validar_perfil_permitido(self):
        if self.usuario_logado.perfil not in [
            "Administrador",
            "Cliente"
        ]:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Apenas clientes e administradores "
                    "podem acessar os itens do carrinho."
                )
            )

    # ==================================================
    # VALIDAR PROPRIETÁRIO
    # ==================================================

    def validar_proprietario(
        self,
        carrinho: Carrinhos
    ):
        # Administrador pode acessar qualquer carrinho
        if self.usuario_logado.perfil == "Administrador":
            return

        # Cliente precisa ter um carrinho associado
        if not carrinho.cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente do carrinho não encontrado."
            )

        # Cliente só pode acessar o próprio carrinho
        if (
            carrinho.cliente.usuario_id
            != self.usuario_logado.id
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Você não possui permissão para "
                    "acessar este carrinho."
                )
            )

    # ==================================================
    # BUSCAR ITEM POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        self.validar_perfil_permitido()

        item = self.repository.buscar_por_id(id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item não encontrado."
            )

        self.validar_proprietario(
            item.carrinho
        )

        return item

    # ==================================================
    # BUSCAR CARRINHO
    # ==================================================

    def buscar_carrinho(
        self,
        carrinho_id: int
    ):
        self.validar_perfil_permitido()

        carrinho = self.repository.buscar_carrinho(
            carrinho_id
        )

        if not carrinho:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )

        self.validar_proprietario(
            carrinho
        )

        return carrinho

    # ==================================================
    # BUSCAR PRODUTO
    # ==================================================

    def buscar_produto(
        self,
        produto_id: int
    ):
        produto = self.repository.buscar_produto(
            produto_id
        )

        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )

        return produto

    # ==================================================
    # CRIAR ITEM NO CARRINHO
    # ==================================================

    def criar(
        self,
        item: ItemCarrinhoCreate
    ):
        """
        Adiciona um produto ao carrinho.

        Regras:
        - Apenas Cliente e Administrador podem adicionar.
        - O carrinho precisa existir.
        - O usuário precisa ter permissão sobre o carrinho.
        - O produto precisa existir.
        - A quantidade deve ser maior que zero.
        - A quantidade não pode ultrapassar o estoque.
        - Se o produto já estiver no carrinho,
          a quantidade será somada.
        """

        self.validar_perfil_permitido()

        # --------------------------------------------------
        # VALIDAR QUANTIDADE
        # --------------------------------------------------

        if item.quantidade <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantidade deve ser maior que zero."
            )

        # --------------------------------------------------
        # BUSCAR CARRINHO
        # --------------------------------------------------

        carrinho = self.buscar_carrinho(
            item.carrinho_id
        )

        # --------------------------------------------------
        # BUSCAR PRODUTO
        # --------------------------------------------------

        produto = self.buscar_produto(
            item.produto_id
        )

        # --------------------------------------------------
        # VALIDAR ESTOQUE
        # --------------------------------------------------

        if item.quantidade > produto.estoque:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Quantidade maior que "
                    "estoque disponível."
                )
            )

        # --------------------------------------------------
        # VERIFICAR SE O PRODUTO JÁ ESTÁ NO CARRINHO
        # --------------------------------------------------

        item_existente = (
            self.repository.buscar_item_existente(
                carrinho_id=item.carrinho_id,
                produto_id=item.produto_id
            )
        )

        # --------------------------------------------------
        # PRODUTO JÁ EXISTE
        # --------------------------------------------------

        if item_existente:

            nova_quantidade = (
                item_existente.quantidade
                + item.quantidade
            )

            if nova_quantidade > produto.estoque:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade total "
                        "ultrapassa estoque."
                    )
                )

            item_existente.quantidade = nova_quantidade

            return self.repository.atualizar(
                item_existente
            )

        # --------------------------------------------------
        # CRIAR NOVO ITEM
        # --------------------------------------------------

        novo_item = ItensCarrinho(
            **item.model_dump()
        )

        return self.repository.criar(
            novo_item
        )

    # ==================================================
    # LISTAR ITENS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        carrinho_id: int | None = None,
        produto_id: int | None = None,
        quantidade_min: int | None = None,
        quantidade_max: int | None = None,
        sort_by: str = "id",
        order: str = "asc"
    ):
        self.validar_perfil_permitido()

        somente_proprio_cliente = (
            self.usuario_logado.perfil == "Cliente"
        )

        return self.repository.listar(
            skip=skip,
            limit=limit,
            carrinho_id=carrinho_id,
            produto_id=produto_id,
            quantidade_min=quantidade_min,
            quantidade_max=quantidade_max,
            usuario_id=self.usuario_logado.id,
            somente_proprio_cliente=somente_proprio_cliente,
            sort_by=sort_by,
            order=order
        )

    # ==================================================
    # ATUALIZAR ITEM
    # ==================================================

    def atualizar(
        self,
        id: int,
        item: ItemCarrinhoUpdate
    ):
        self.validar_perfil_permitido()

        item_db = self.buscar_por_id(id)

        dados = item.model_dump(
            exclude_unset=True
        )

        # --------------------------------------------------
        # NÃO HÁ NENHUM DADO PARA ATUALIZAR
        # --------------------------------------------------

        if not dados:
            raise HTTPException(
                status_code=400,
                detail="Nenhum dado foi informado para atualização."
            )

        # --------------------------------------------------
        # ATUALIZAR QUANTIDADE
        # --------------------------------------------------

        if "quantidade" in dados:

            quantidade = dados["quantidade"]

            if quantidade <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade deve ser "
                        "maior que zero."
                    )
                )

            produto = self.buscar_produto(
                item_db.produto_id
            )

            if quantidade > produto.estoque:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade maior que "
                        "estoque disponível."
                    )
                )

            item_db.quantidade = quantidade

        return self.repository.atualizar(
            item_db
        )

    # ==================================================
    # DELETAR ITEM
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        self.validar_perfil_permitido()

        item = self.buscar_por_id(id)

        self.repository.deletar(
            item
        )

        return True

