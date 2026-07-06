from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoUpdate,
    CarrinhoResponse
)
from backend.services.implementations.carrinho_service_impl import CarrinhoServiceImpl

router = APIRouter(prefix="/carrinhos", tags=["Carrinhos"])


def get_service(session: Session = Depends(get_session)):
    return CarrinhoServiceImpl(session)


@router.post("/", response_model=CarrinhoResponse)
def criar(carrinho: CarrinhoCreate, service=Depends(get_service)):
    return service.criar(carrinho)


@router.get("/", response_model=list[CarrinhoResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=CarrinhoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=CarrinhoResponse)
def atualizar(id: int, carrinho: CarrinhoUpdate, service=Depends(get_service)):
    return service.atualizar(id, carrinho)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}