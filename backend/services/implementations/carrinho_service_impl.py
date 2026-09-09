from datetime import datetime

from fastapi import HTTPException

from backend.models.carrinho_model import Carrinhos
from backend.models.usuario_model import Usuarios

from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoUpdate
)

from backend.repositories.carrinho_repository import (
    CarrinhoRepository
)


class CarrinhoServiceImpl:
    """
    Service responsável pelas regras de negócio
    relacionadas aos carrinhos.

    Regras:

    - Cliente possui apenas um carrinho.
    - Cliente só acessa seu próprio carrinho.
    - Administrador possui acesso total.
    - Carrinho vazio não pode finalizar compra.
    - Produto sem estoque bloqueia compra.
    - Estoque é reduzido ao finalizar compra.
    - Carrinho com itens não pode ser excluído.
    """

    def __init__(
        self,
        repository: CarrinhoRepository,
        usuario_logado: Usuarios
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==================================================
    # PERFIL
    # ==================================================

    def obter_perfil(self):

        perfil = self.usuario_logado.perfil

        if hasattr(perfil, "nome"):
            return perfil.nome

        return perfil

    # ==================================================
    # VERIFICAR ADMINISTRADOR
    # ==================================================

    def is_admin(self):

        return (
            self.obter_perfil()
            == "Administrador"
        )

    # ==================================================
    # BUSCAR CARRINHO
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):

        carrinho = self.repository.buscar_por_id(
            id
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
    # BUSCAR POR CLIENTE
    # ==================================================

    def buscar_por_cliente(
        self,
        cliente_id: int
    ):

        return self.repository.buscar_por_cliente(
            cliente_id
        )

    # ==================================================
    # VALIDAR CLIENTE
    # ==================================================

    def validar_cliente(
        self,
        cliente_id: int
    ):

        cliente = self.repository.buscar_cliente(
            cliente_id
        )

        if not cliente:

            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )

        return cliente

    # ==================================================
    # VALIDAR PROPRIETÁRIO
    # ==================================================

    def validar_proprietario(
        self,
        carrinho: Carrinhos
    ):
        """
        Administradores podem acessar qualquer carrinho.

        Clientes somente podem acessar carrinhos
        vinculados ao próprio usuário.
        """

        if self.is_admin():
            return

        if not carrinho.cliente:

            raise HTTPException(
                status_code=404,
                detail="Cliente do carrinho não encontrado."
            )

        if (
            carrinho.cliente.usuario_id
            != self.usuario_logado.id
        ):

            raise HTTPException(
                status_code=403,
                detail=(
                    "Você não possui acesso "
                    "a este carrinho."
                )
            )

    # ==================================================
    # CRIAR CARRINHO
    # ==================================================

    def criar(
        self,
        carrinho: CarrinhoCreate
    ):

        # --------------------------------------------------
        # VALIDAR CLIENTE
        # --------------------------------------------------

        cliente = self.validar_cliente(
            carrinho.cliente_id
        )

        # --------------------------------------------------
        # CLIENTE SÓ PODE CRIAR O PRÓPRIO CARRINHO
        # --------------------------------------------------

        if not self.is_admin():

            if (
                cliente.usuario_id
                != self.usuario_logado.id
            ):

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Você só pode criar "
                        "seu próprio carrinho."
                    )
                )

        # --------------------------------------------------
        # VERIFICAR SE JÁ POSSUI CARRINHO
        # --------------------------------------------------

        existente = self.buscar_por_cliente(
            carrinho.cliente_id
        )

        if existente:

            raise HTTPException(
                status_code=409,
                detail=(
                    "Cliente já possui um carrinho."
                )
            )

        # --------------------------------------------------
        # CRIAR OBJETO
        # --------------------------------------------------

        novo = Carrinhos(
            **carrinho.model_dump()
        )

        try:

            return self.repository.criar(
                novo
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Erro ao criar carrinho."
            )

    # ==================================================
    # LISTAR CARRINHOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        cliente_id: int | None = None,
        data_criacao: datetime | None = None,
        sort_by: str = "data_criacao",
        order: str = "desc"
    ):

        # --------------------------------------------------
        # CORRIGIR PAGINAÇÃO
        # --------------------------------------------------

        if skip < 0:
            skip = 0

        if limit <= 0:
            limit = 10

        if limit > 100:
            limit = 100

        # --------------------------------------------------
        # CLIENTE
        # --------------------------------------------------

        if not self.is_admin():

            # Cliente não pode escolher outro cliente.
            cliente_id = None

            return self.repository.listar(
                skip=skip,
                limit=limit,
                cliente_id=None,
                data_criacao=data_criacao,
                usuario_id=self.usuario_logado.id,
                somente_proprio_cliente=True,
                sort_by=sort_by,
                order=order
            )

        # --------------------------------------------------
        # ADMINISTRADOR
        # --------------------------------------------------

        return self.repository.listar(
            skip=skip,
            limit=limit,
            cliente_id=cliente_id,
            data_criacao=data_criacao,
            usuario_id=None,
            somente_proprio_cliente=False,
            sort_by=sort_by,
            order=order
        )

    # ==================================================
    # ATUALIZAR
    # ==================================================

    def atualizar(
        self,
        id: int,
        carrinho: CarrinhoUpdate
    ):

        db = self.buscar_por_id(
            id
        )

        dados = carrinho.model_dump(
            exclude_unset=True
        )

        # --------------------------------------------------
        # NENHUM DADO
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
        # ALTERAÇÃO DE CLIENTE
        # --------------------------------------------------

        if "cliente_id" in dados:

            cliente = self.validar_cliente(
                dados["cliente_id"]
            )

            # Cliente não pode transferir
            # carrinho para outro cliente.

            if not self.is_admin():

                if (
                    cliente.usuario_id
                    != self.usuario_logado.id
                ):

                    raise HTTPException(
                        status_code=403,
                        detail=(
                            "Você não pode "
                            "transferir este carrinho."
                        )
                    )

            outro = self.buscar_por_cliente(
                dados["cliente_id"]
            )

            if (
                outro
                and outro.id != id
            ):

                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Cliente já possui "
                        "outro carrinho."
                    )
                )

        # --------------------------------------------------
        # APLICAR ALTERAÇÕES
        # --------------------------------------------------

        try:

            for campo, valor in dados.items():

                setattr(
                    db,
                    campo,
                    valor
                )

            return self.repository.atualizar(
                db
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar carrinho."
            )

    # ==================================================
    # DELETAR
    # ==================================================

    def deletar(
        self,
        id: int
    ):

        carrinho = self.buscar_por_id(
            id
        )

        # --------------------------------------------------
        # NÃO PERMITIR EXCLUSÃO COM ITENS
        # --------------------------------------------------

        if carrinho.itens:

            raise HTTPException(
                status_code=409,
                detail=(
                    "Carrinho possui itens. "
                    "Remova os produtos antes."
                )
            )

        try:

            self.repository.deletar(
                carrinho
            )

            return True

        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Erro ao excluir carrinho."
            )

    # ==================================================
    # FINALIZAR COMPRA
    # ==================================================

    def finalizar_compra(
        self,
        carrinho_id: int
    ):
        """
        Finaliza a compra do carrinho.

        Regras de negócio:

        - Usuário deve ser dono do carrinho.
        - Administrador pode finalizar qualquer carrinho.
        - Carrinho não pode estar vazio.
        - Produto precisa ter estoque suficiente.
        - Estoque é reduzido.
        - Itens são removidos após a compra.
        """

        # --------------------------------------------------
        # BUSCAR E VALIDAR ACESSO
        # --------------------------------------------------

        carrinho = self.buscar_por_id(
            carrinho_id
        )

        # --------------------------------------------------
        # VALIDAR CARRINHO VAZIO
        # --------------------------------------------------

        if not carrinho.itens:

            raise HTTPException(
                status_code=400,
                detail="Carrinho vazio."
            )

        # --------------------------------------------------
        # VALIDAR ESTOQUE
        # --------------------------------------------------

        for item in carrinho.itens:

            produto = item.produto

            if not produto:

                raise HTTPException(
                    status_code=404,
                    detail=(
                        "Produto do item "
                        "não encontrado."
                    )
                )

            if produto.estoque < item.quantidade:

                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Estoque insuficiente "
                        f"para {produto.nome}."
                    )
                )

        # --------------------------------------------------
        # FINALIZAR COMPRA
        # --------------------------------------------------

        try:

            return self.repository.finalizar_compra(
                carrinho
            )

        except HTTPException:

            raise

        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Erro ao finalizar compra."
            )