from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.produto_repository import ProdutoRepository
from backend.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate,
)
from backend.services.implementations.produto_service_impl import ProdutoServiceImpl

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# ==================================================
# DEPENDÊNCIA DO SERVICE
# ==================================================


def get_service(
    session: Annotated[Session, Depends(get_session)],
    usuario_logado: Annotated[Usuarios, Depends(get_current_user)],
):
    repository = ProdutoRepository(session)

    return ProdutoServiceImpl(
        repository=repository,
        usuario_logado=usuario_logado,
    )


ProdutoServiceDep = Annotated[
    ProdutoServiceImpl,
    Depends(get_service),
]


# ==================================================
# CRIAR PRODUTO
# Apenas Administrador
# ==================================================


@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar(
    produto: ProdutoCreate,
    service: ProdutoServiceDep,
):
    return service.criar(produto)


# ==================================================
# LISTAR PRODUTOS
# Usuários autenticados
# ==================================================


@router.get("/", response_model=list[ProdutoResponse])
def listar(
    service: ProdutoServiceDep,
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
    order: str = "asc",
):
    return service.listar(
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
        order=order,
    )


# ==================================================
# BUSCAR PRODUTO POR ID
# Usuários autenticados
# ==================================================


@router.get("/{id}", response_model=ProdutoResponse)
def buscar(
    id: int,
    service: ProdutoServiceDep,
):
    return service.buscar_por_id(id)


# ==================================================
# ATUALIZAR PRODUTO
# Apenas Administrador
# ==================================================


@router.put("/{id}", response_model=ProdutoResponse)
def atualizar(
    id: int,
    produto: ProdutoUpdate,
    service: ProdutoServiceDep,
):
    return service.atualizar(id, produto)


# ==================================================
# DELETAR PRODUTO
# Apenas Administrador
# ==================================================


@router.delete("/{id}")
def deletar(
    id: int,
    service: ProdutoServiceDep,
):
    return {"success": service.deletar(id)}
