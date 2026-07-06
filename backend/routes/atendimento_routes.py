from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoUpdate,
    AtendimentoResponse
)
from backend.services.implementations.atendimento_service_impl import AtendimentoServiceImpl
from backend.auth.dependencies import get_current_user
router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return AtendimentoServiceImpl(session)


@router.post("/", response_model=AtendimentoResponse)
def criar(atendimento: AtendimentoCreate, service=Depends(get_service)):
    return service.criar(atendimento)


@router.get("/", response_model=list[AtendimentoResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=AtendimentoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=AtendimentoResponse)
def atualizar(id: int, atendimento: AtendimentoUpdate, service=Depends(get_service)):
    return service.atualizar(id, atendimento)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}