from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database.database import get_session
from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate,
    AgendamentoResponse
)
from backend.services.implementations.agendamento_service_impl import AgendamentoServiceImpl
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return AgendamentoServiceImpl(session)


@router.post("/", response_model=AgendamentoResponse)
def criar(agendamento: AgendamentoCreate, service=Depends(get_service)):
    return service.criar(agendamento)

#PAGINAÇÃO e filtros
@router.get("/", response_model=list[AgendamentoResponse])
def listar(
    skip: int = 0,
    limit: int = 10,
    animal_id: int | None = None,
    status: str | None = None,
    descricao: str | None = None,
    data: datetime | None = None,
    sort_by: str = "data_agendamento",
    order: str = "asc",
    service: AgendamentoServiceImpl = Depends(get_service),
):
    return service.listar(
        skip=skip,
        limit=limit,
        animal_id=animal_id,
        status=status,
        descricao=descricao,
        data=data,
        sort_by=sort_by,
        order=order,
    )


@router.get("/{id}", response_model=AgendamentoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=AgendamentoResponse)
def atualizar(id: int, agendamento: AgendamentoUpdate, service=Depends(get_service)):
    return service.atualizar(id, agendamento)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}