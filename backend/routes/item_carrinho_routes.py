from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.item_carrinho_schema import (
    ItemCarrinhoCreate,
    ItemCarrinhoUpdate,
    ItemCarrinhoResponse
)
from backend.services.implementations.item_carrinho_service_impl import ItemCarrinhoServiceImpl
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/itens-carrinho", tags=["Itens Carrinho"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return ItemCarrinhoServiceImpl(session)


@router.post("/", response_model=ItemCarrinhoResponse)
def criar(item: ItemCarrinhoCreate, service=Depends(get_service)):
    return service.criar(item)

#PAGINAÇÃO e filtros
@router.get(
    "/",
    response_model=list[ItemCarrinhoResponse],
    dependencies=[Depends(get_current_user)],
)
def listar(
    skip: int = 0,
    limit: int = 10,
    carrinho_id: int | None = None,
    produto_id: int | None = None,
    quantidade_min: int | None = None,
    quantidade_max: int |None = None,
    sort_by: str = "id",
    order: str = "asc",
    service: ItemCarrinhoServiceImpl = Depends(get_service),
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


@router.get("/{id}", response_model=ItemCarrinhoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=ItemCarrinhoResponse)
def atualizar(id: int, item: ItemCarrinhoUpdate, service=Depends(get_service)):
    return service.atualizar(id, item)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}