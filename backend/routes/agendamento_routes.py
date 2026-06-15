from backend.models.models import Agendamentos
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado

from backend.services.implementations.agendamento_service_impl import (
    AgendamentoServiceImpl
)

from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/agendamentos",
    tags=["agendamentos"]
)

@router.get("/", response_model=list[Agendamentos])
def get_agendamentos(
    session: SessionDep,
    usuario: UsuarioLogado
):
    return AgendamentoServiceImpl(
        session
    ).listar_agendamentos()

@router.post("/", response_model=Agendamentos)
def create_agendamento(
    agendamento: Agendamentos,
    session: SessionDep
):
    return AgendamentoServiceImpl(
        session
    ).criar_agendamento(agendamento)