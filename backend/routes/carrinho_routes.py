from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database.database import get_session

from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoUpdate,
    CarrinhoResponse,
    CompraResponse
)

from backend.services.implementations.carrinho_service_impl import (
    CarrinhoServiceImpl
)

from backend.models.usuario_model import Usuarios

from backend.auth.dependencies import get_current_user



router = APIRouter(
    prefix="/carrinhos",
    tags=["Carrinhos"]
)



# ==================================================
# SERVICE
# ==================================================

def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(get_current_user)
):

    return CarrinhoServiceImpl(
        session,
        usuario_logado
    )



# ==================================================
# CRIAR CARRINHO
# ==================================================

@router.post(
    "/",
    response_model=CarrinhoResponse,
    status_code=201
)
def criar(
    carrinho: CarrinhoCreate,

    service: CarrinhoServiceImpl = Depends(get_service)

):

    return service.criar(
        carrinho
    )



# ==================================================
# LISTAR CARRINHOS
# ==================================================

@router.get(
    "/",
    response_model=list[CarrinhoResponse]
)
def listar(

    skip: int = 0,

    limit: int = 10,

    cliente_id: int | None = None,

    data_criacao: datetime | None = None,

    sort_by: str = "data_criacao",

    order: str = "desc",

    service: CarrinhoServiceImpl = Depends(get_service)

):

    return service.listar(

        skip=skip,

        limit=limit,

        cliente_id=cliente_id,

        data_criacao=data_criacao,

        sort_by=sort_by,

        order=order

    )



# ==================================================
# BUSCAR CARRINHO
# ==================================================

@router.get(
    "/{id}",
    response_model=CarrinhoResponse
)
def buscar(

    id: int,

    service: CarrinhoServiceImpl = Depends(get_service)

):

    return service.buscar_por_id(
        id
    )



# ==================================================
# ATUALIZAR CARRINHO
# ==================================================

@router.put(
    "/{id}",
    response_model=CarrinhoResponse
)
def atualizar(

    id: int,

    carrinho: CarrinhoUpdate,

    service: CarrinhoServiceImpl = Depends(get_service)

):

    return service.atualizar(

        id,

        carrinho

    )



# ==================================================
# FINALIZAR COMPRA
# ==================================================

@router.post(
    "/{id}/finalizar",
    response_model=CompraResponse,
    summary="Finalizar compra do carrinho"
)
def finalizar_compra(

    id: int,

    service: CarrinhoServiceImpl = Depends(get_service)

):

    return service.finalizar_compra(
        id
    )



# ==================================================
# DELETAR CARRINHO
# ==================================================

@router.delete(
    "/{id}",
    status_code=204
)
def deletar(

    id: int,

    service: CarrinhoServiceImpl = Depends(get_service)

):

    service.deletar(
        id
    )

    return Response(
        status_code=204
    )