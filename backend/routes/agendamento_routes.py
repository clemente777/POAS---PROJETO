from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate,
    AgendamentoResponse
)
from backend.services.implementations.agendamento_service_impl import AgendamentoServiceImpl

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


def get_service(session: Session = Depends(get_session)):
    return AgendamentoServiceImpl(session)


@router.post("/", response_model=AgendamentoResponse)
def criar(agendamento: AgendamentoCreate, service=Depends(get_service)):
    return service.criar(agendamento)


@router.get("/", response_model=list[AgendamentoResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=AgendamentoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=AgendamentoResponse)
def atualizar(id: int, agendamento: AgendamentoUpdate, service=Depends(get_service)):
    return service.atualizar(id, agendamento)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}