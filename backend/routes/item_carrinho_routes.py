from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.item_carrinho_repository import ItemCarrinhoRepository
from backend.schemas.item_carrinho_schema import (
    ItemCarrinhoCreate,
    ItemCarrinhoResponse,
    ItemCarrinhoUpdate,
)
from backend.services.implementations.item_carrinho_service_impl import (
    ItemCarrinhoServiceImpl,
)

router = APIRouter(prefix="/itens-carrinho", tags=["Itens Carrinho"])


# ==================================================
# DEPENDÊNCIAS
# ==================================================

SessionDep = Annotated[Session, Depends(get_session)]

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]


# ==================================================
# DEPENDÊNCIA DO SERVICE
# ==================================================


def get_service(
    session: SessionDep,
    usuario_logado: UsuarioLogadoDep,
):
    repository = ItemCarrinhoRepository(session)

    return ItemCarrinhoServiceImpl(
        repository=repository,
        usuario_logado=usuario_logado,
    )


ItemCarrinhoServiceDep = Annotated[
    ItemCarrinhoServiceImpl,
    Depends(get_service),
]


# ==================================================
# CRIAR ITEM
# Cliente e Administrador
# ==================================================


@router.post("/", response_model=ItemCarrinhoResponse, status_code=201)
def criar(
    item: ItemCarrinhoCreate,
    service: ItemCarrinhoServiceDep,
):
    return service.criar(item)


# ==================================================
# LISTAR ITENS
# ==================================================


@router.get("/", response_model=list[ItemCarrinhoResponse])
def listar(
    service: ItemCarrinhoServiceDep,
    skip: int = 0,
    limit: int = 10,
    carrinho_id: int | None = None,
    produto_id: int | None = None,
    quantidade_min: int | None = None,
    quantidade_max: int | None = None,
    sort_by: str = "id",
    order: str = "asc",
):
    return service.listar(
        skip=skip,
        limit=limit,
        carrinho_id=carrinho_id,
        produto_id=produto_id,
        quantidade_min=quantidade_min,
        quantidade_max=quantidade_max,
        sort_by=sort_by,
        order=order,
    )


# ==================================================
# BUSCAR ITEM
# ==================================================


@router.get("/{id}", response_model=ItemCarrinhoResponse)
def buscar(
    id: int,
    service: ItemCarrinhoServiceDep,
):
    return service.buscar_por_id(id)


# ==================================================
# ATUALIZAR ITEM
# ==================================================


@router.put("/{id}", response_model=ItemCarrinhoResponse)
def atualizar(
    id: int,
    item: ItemCarrinhoUpdate,
    service: ItemCarrinhoServiceDep,
):
    return service.atualizar(id, item)


# ==================================================
# DELETAR ITEM
# ==================================================


@router.delete("/{id}", status_code=204)
def deletar(
    id: int,
    service: ItemCarrinhoServiceDep,
):
    service.deletar(id)

    return Response(status_code=204)
