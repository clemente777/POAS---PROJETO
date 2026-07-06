from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse
)
from backend.services.implementations.cliente_service_impl import ClienteServiceImpl
from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user
router = APIRouter(prefix="/clientes", tags=["Clientes"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return ClienteServiceImpl(session)


@router.post("/", response_model=ClienteResponse)
def criar(cliente: ClienteCreate, service=Depends(get_service)):
    return service.criar(cliente)


@router.get("/", response_model=list[ClienteResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=ClienteResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=ClienteResponse)
def atualizar(id: int, cliente: ClienteUpdate, service=Depends(get_service)):
    return service.atualizar(id, cliente)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}