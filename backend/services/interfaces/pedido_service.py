from abc import ABC, abstractmethod


class PedidoService(ABC):

    @abstractmethod
    def listar_pedidos(
        self,
        skip: int = 0,
        limite: int = 10,
        cliente_id: int | None = None
    ):
        pass

    @abstractmethod
    def buscar_pedido_por_id(self, id):
        pass
