from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.schemas.item_carrinho_schema import (
    ItemCarrinhoCreate,
    ItemCarrinhoUpdate,
    ItemCarrinhoResponse
)

from backend.services.implementations.item_carrinho_service_impl import (
    ItemCarrinhoServiceImpl
)

from backend.auth.dependencies import get_current_user

from backend.models.usuario_model import Usuarios



router = APIRouter(
    prefix="/itens-carrinho",
    tags=["Itens Carrinho"]
)



def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(get_current_user)
):

    return ItemCarrinhoServiceImpl(
        session,
        usuario_logado
    )





# ==================================================
# CRIAR ITEM
# Cliente e Administrador
# ==================================================

@router.post(
    "/",
    response_model=ItemCarrinhoResponse,
    status_code=201
)
def criar(
    item: ItemCarrinhoCreate,

    service: ItemCarrinhoServiceImpl = Depends(
        get_service
    )
):

    return service.criar(
        item
    )






# ==================================================
# LISTAR ITENS
# ==================================================

@router.get(
    "/",
    response_model=list[ItemCarrinhoResponse]
)
def listar(

    skip: int = 0,

    limit: int = 10,

    carrinho_id: int | None = None,

    produto_id: int | None = None,

    quantidade_min: int | None = None,

    quantidade_max: int | None = None,

    sort_by: str = "id",

    order: str = "asc",

    service: ItemCarrinhoServiceImpl = Depends(
        get_service
    )

):


    return service.listar(

        skip=skip,

        limit=limit,

        carrinho_id=carrinho_id,

        produto_id=produto_id,

        quantidade_min=quantidade_min,

        quantidade_max=quantidade_max,

        sort_by=sort_by,

        order=order

    )






# ==================================================
# BUSCAR ITEM
# ==================================================

@router.get(
    "/{id}",
    response_model=ItemCarrinhoResponse
)
def buscar(

    id: int,

    service: ItemCarrinhoServiceImpl = Depends(
        get_service
    )

):

    return service.buscar_por_id(
        id
    )






# ==================================================
# ATUALIZAR ITEM
# ==================================================

@router.put(
    "/{id}",
    response_model=ItemCarrinhoResponse
)
def atualizar(

    id: int,

    item: ItemCarrinhoUpdate,

    service: ItemCarrinhoServiceImpl = Depends(
        get_service
    )

):

    return service.atualizar(

        id,

        item

    )






# ==================================================
# DELETAR ITEM
# ==================================================

@router.delete(
    "/{id}",
    status_code=204
)
def deletar(

    id: int,

    service: ItemCarrinhoServiceImpl = Depends(
        get_service
    )

):


    service.deletar(
        id
    )


    return Response(
        status_code=204
    )