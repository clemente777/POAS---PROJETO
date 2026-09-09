from datetime import datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil

from backend.models.usuario_model import Usuarios

from backend.repositories.agendamento_repository import (
    AgendamentoRepository
)

from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate,
    AgendamentoResponse
)

from backend.services.implementations.agendamento_service_impl import (
    AgendamentoServiceImpl
)


router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)


# ==========================================================
# DEPENDÊNCIA SERVICE
# ==========================================================

def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(
        get_current_user
    )
):

    repository = AgendamentoRepository(
        session
    )

    return AgendamentoServiceImpl(
        repository,
        usuario_logado
    )


# ==========================================================
# CRIAR
#
# Cliente, Veterinário e Administrador
# ==========================================================

@router.post(
    "/",
    response_model=AgendamentoResponse,
    status_code=201
)
def criar(

    agendamento: AgendamentoCreate,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Cliente",
            "Veterinário",
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.criar(
        agendamento
    )


# ==========================================================
# LISTAR
#
# Cliente, Veterinário e Administrador
# ==========================================================

@router.get(
    "/",
    response_model=list[AgendamentoResponse]
)
def listar(

    skip: int = 0,

    limit: int = 10,

    animal_id: int | None = None,

    status: str | None = None,

    descricao: str | None = None,

    data: datetime | None = None,

    sort_by: str = "data_agendamento",

    order: str = "asc",

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Cliente",
            "Veterinário",
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.listar(
        skip=skip,
        limit=limit,
        animal_id=animal_id,
        status=status,
        descricao=descricao,
        data=data,
        sort_by=sort_by,
        order=order
    )


# ==========================================================
# BUSCAR POR ID
#
# Cliente, Veterinário e Administrador
# ==========================================================

@router.get(
    "/{id}",
    response_model=AgendamentoResponse
)
def buscar(

    id: int,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Cliente",
            "Veterinário",
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.buscar_por_id(
        id
    )


# ==========================================================
# ATUALIZAR
#
# Veterinário e Administrador
# ==========================================================

@router.put(
    "/{id}",
    response_model=AgendamentoResponse
)
def atualizar(

    id: int,

    agendamento: AgendamentoUpdate,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Veterinário",
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.atualizar(
        id,
        agendamento
    )


# ==========================================================
# CANCELAR
#
# Cliente, Veterinário e Administrador
# ==========================================================

@router.post(
    "/{id}/cancelar",
    response_model=AgendamentoResponse
)
def cancelar(

    id: int,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Cliente",
            "Veterinário",
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.cancelar(
        id
    )


# ==========================================================
# DELETAR
#
# Apenas Administrador
#
# O Service bloqueia a exclusão.
# ==========================================================

@router.delete(
    "/{id}",
    status_code=204
)
def deletar(

    id: int,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(get_service)):

    service.deletar(id)
    return Response(
        status_code=204
    )

