from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.carrinho_repository import CarrinhoRepository
from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoResponse,
    CarrinhoUpdate,
    CompraResponse,
)
from backend.services.implementations.carrinho_service_impl import CarrinhoServiceImpl

router = APIRouter(prefix="/carrinhos", tags=["Carrinhos"])


# ==================================================
# DEPENDÊNCIAS
# ==================================================

SessionDep = Annotated[Session, Depends(get_session)]

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]


# ==================================================
# SERVICE
# ==================================================


def get_service(
    session: SessionDep,
    usuario_logado: UsuarioLogadoDep,
):
    """
    Cria o Repository e o Service para
    cada requisição.
    """

    repository = CarrinhoRepository(session)

    return CarrinhoServiceImpl(repository, usuario_logado)


CarrinhoServiceDep = Annotated[
    CarrinhoServiceImpl,
    Depends(get_service),
]


# ==================================================
# CRIAR CARRINHO
# ==================================================


@router.post("/", response_model=CarrinhoResponse, status_code=201)
def criar(
    carrinho: CarrinhoCreate,
    service: CarrinhoServiceDep,
):
    return service.criar(carrinho)


# ==================================================
# LISTAR CARRINHOS
# ==================================================


@router.get("/", response_model=list[CarrinhoResponse])
def listar(
    service: CarrinhoServiceDep,
    skip: int = 0,
    limit: int = 10,
    cliente_id: int | None = None,
    data_criacao: datetime | None = None,
    sort_by: str = "data_criacao",
    order: str = "desc",
):
    return service.listar(
        skip=skip,
        limit=limit,
        cliente_id=cliente_id,
        data_criacao=data_criacao,
        sort_by=sort_by,
        order=order,
    )


# ==================================================
# BUSCAR CARRINHO
# ==================================================


@router.get("/{id}", response_model=CarrinhoResponse)
def buscar(
    id: int,
    service: CarrinhoServiceDep,
):
    return service.buscar_por_id(id)


# ==================================================
# ATUALIZAR CARRINHO
# ==================================================


@router.put("/{id}", response_model=CarrinhoResponse)
def atualizar(
    id: int,
    carrinho: CarrinhoUpdate,
    service: CarrinhoServiceDep,
):
    return service.atualizar(id, carrinho)


# ==================================================
# FINALIZAR COMPRA
# ==================================================


@router.post(
    "/{id}/finalizar",
    response_model=CompraResponse,
    summary="Finalizar compra do carrinho",
)
def finalizar_compra(
    id: int,
    service: CarrinhoServiceDep,
):
    return service.finalizar_compra(id)


# ==================================================
# DELETAR CARRINHO
# ==================================================


@router.delete("/{id}", status_code=204)
def deletar(
    id: int,
    service: CarrinhoServiceDep,
):
    service.deletar(id)

    return Response(status_code=204)
