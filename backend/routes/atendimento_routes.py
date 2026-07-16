from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database.database import get_session
from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoUpdate,
    AtendimentoResponse
)
from sqlalchemy import select

from backend.models.animal_model import Animais
from backend.models.atendimento_model import Atendimentos
from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes
from backend.services.implementations.atendimento_service_impl import AtendimentoServiceImpl
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return AtendimentoServiceImpl(session)


@router.post("/", response_model=AtendimentoResponse)
def criar(atendimento: AtendimentoCreate, service=Depends(get_service)):
    return service.criar(atendimento)


#paginacao e filtros
@router.get("/", response_model=list[AtendimentoResponse])
def listar(
    skip: int = 0,
    limit: int = 10,
    animal_id: int | None = None,
    usuario_id: int | None = None,
    diagnostico: str | None = None,
    data: datetime | None = None,
    sort_by: str = "data_atendimento",
    order: str = "asc",
    service: AtendimentoServiceImpl = Depends(get_service),
):

    return service.listar(
        skip=skip,
        limit=limit,
        animal_id=animal_id,
        usuario_id=usuario_id,
        diagnostico=diagnostico,
        data=data,
        sort_by=sort_by,
        order=order,
    )


@router.get("/{id}", response_model=AtendimentoResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=AtendimentoResponse)
def atualizar(id: int, atendimento: AtendimentoUpdate, service=Depends(get_service)):
    return service.atualizar(id, atendimento)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}