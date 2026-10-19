from fastapi import HTTPException

from backend.models.usuario_model import Usuarios

from backend.repositories.pedido_repository import (
    PedidoRepository
)

from backend.services.interfaces.pedido_service import (
    PedidoService
)


class PedidoServiceImpl(PedidoService):
    """
    Regras de negócio do histórico de compras.

    Regras:
    - Cliente vê apenas as próprias compras.
    - Administrador vê todas (e pode filtrar por cliente).
    - Veterinário não acessa compras.
    """

    PERFIS_COM_ACESSO = ("Administrador", "Cliente")

    def __init__(
        self,
        repository: PedidoRepository,
        usuario_logado: Usuarios
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # AUXILIAR
    # ==========================================================

    def obter_perfil(self):
        return self.usuario_logado.perfil

    def is_admin(self):
        return self.obter_perfil() == "Administrador"

    def validar_acesso(self):

        if self.obter_perfil() not in self.PERFIS_COM_ACESSO:

            raise HTTPException(
                status_code=403,
                detail="Você não possui acesso às compras."
            )

    # ==========================================================
    # LISTAR
    # ==========================================================

    def listar_pedidos(
        self,
        skip: int = 0,
        limite: int = 10,
        cliente_id: int | None = None
    ):

        self.validar_acesso()

        if skip < 0:
            skip = 0

        if limite <= 0:
            limite = 10

        if limite > 100:
            limite = 100

        if self.is_admin():

            return self.repository.listar(
                skip=skip,
                limite=limite,
                cliente_id=cliente_id
            )

        # Cliente: só enxerga o que é dele,
        # ignorando qualquer cliente_id informado.
        cliente = self.repository.buscar_cliente_por_usuario_id(
            self.usuario_logado.id
        )

        if not cliente:
            return []

        return self.repository.listar(
            skip=skip,
            limite=limite,
            cliente_id=cliente.id
        )

    # ==========================================================
    # BUSCAR
    # ==========================================================

    def buscar_pedido_por_id(self, id: int):

        self.validar_acesso()

        pedido = self.repository.buscar_por_id(id)

        if not pedido:

            raise HTTPException(
                status_code=404,
                detail="Compra não encontrada."
            )

        if not self.is_admin():

            cliente = (
                self.repository.buscar_cliente_por_usuario_id(
                    self.usuario_logado.id
                )
            )

            if not cliente or pedido.cliente_id != cliente.id:

                raise HTTPException(
                    status_code=403,
                    detail="Você não possui acesso a esta compra."
                )

        return pedido
