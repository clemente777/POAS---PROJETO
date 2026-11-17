from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.pedido_repository import PedidoRepository
from backend.schemas.pedido_schema import PedidoResponse
from backend.services.implementations.pedido_service_impl import PedidoServiceImpl

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# ==========================================================
# SERVICE
# ==========================================================


def get_service(
    session: Annotated[Session, Depends(get_session)],
    usuario_logado: Annotated[Usuarios, Depends(get_current_user)],
):
    repository = PedidoRepository(session)

    return PedidoServiceImpl(repository, usuario_logado)


PedidoServiceDep = Annotated[
    PedidoServiceImpl,
    Depends(get_service),
]


# ==========================================================
# LISTAR COMPRAS
# Cliente: apenas as suas | Administrador: todas
# ==========================================================


@router.get("/", response_model=list[PedidoResponse])
def listar(
    service: PedidoServiceDep,
    skip: int = 0,
    limit: int = 10,
    cliente_id: int | None = None,
):
    return service.listar_pedidos(
        skip=skip,
        limite=limit,
        cliente_id=cliente_id,
    )


# ==========================================================
# BUSCAR COMPRA
# ==========================================================


@router.get("/{id}", response_model=PedidoResponse)
def buscar(
    id: int,
    service: PedidoServiceDep,
):
    return service.buscar_pedido_por_id(id)
