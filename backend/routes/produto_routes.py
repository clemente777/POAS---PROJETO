from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
)
from backend.services.implementations.produto_service_impl import ProdutoServiceImpl
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/produtos", tags=["Produtos"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return ProdutoServiceImpl(session)


@router.post("/", response_model=ProdutoResponse)
def criar(produto: ProdutoCreate, service=Depends(get_service)):
    return service.criar(produto)

#PAGINAÇÃO e filtros
@router.get("/",response_model=list[ProdutoResponse])
def listar(
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
    service: ProdutoServiceImpl = Depends(get_service),
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


@router.get("/{id}", response_model=ProdutoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=ProdutoResponse)
def atualizar(id: int, produto: ProdutoUpdate, service=Depends(get_service)):
    return service.atualizar(id, produto)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}