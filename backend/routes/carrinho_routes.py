from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoUpdate,
    CarrinhoResponse,
    CompraResponse
)
from backend.services.implementations.carrinho_service_impl import CarrinhoServiceImpl
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/carrinhos", tags=["Carrinhos"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return CarrinhoServiceImpl(session)


@router.post("/", response_model=CarrinhoResponse)
def criar(carrinho: CarrinhoCreate, service=Depends(get_service)):
    return service.criar(carrinho)

#PAGINAÇÃO e filtros
from datetime import datetime

@router.get("/", response_model=list[CarrinhoResponse],)
def listar(
    skip: int = 0,
    limit: int = 10,
    cliente_id: int | None = None,
    data_criacao: datetime | None = None,
    sort_by: str = "data_criacao",
    order: str = "desc",
    service: CarrinhoServiceImpl = Depends(get_service),
):

    return service.listar(
        skip=skip,
        limit=limit,
        cliente_id=cliente_id,
        data_criacao=data_criacao,
        sort_by=sort_by,
        order=order,
    )


@router.get("/{id}", response_model=CarrinhoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=CarrinhoResponse)
def atualizar(id: int, carrinho: CarrinhoUpdate, service=Depends(get_service)):
    return service.atualizar(id, carrinho)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}
 

@router.post("/{id}/finalizar", response_model=CompraResponse, summary="Finalizar compra do carrinho")
def finalizar_compra(id: int, service: CarrinhoServiceImpl = Depends(get_service)):
    try:

        return service.finalizar_compra(id)
    
    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )