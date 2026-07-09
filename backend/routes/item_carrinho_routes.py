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


@router.get("/", response_model=list[ItemCarrinhoResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=ItemCarrinhoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=ItemCarrinhoResponse)
def atualizar(id: int, item: ItemCarrinhoUpdate, service=Depends(get_service)):
    return service.atualizar(id, item)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}