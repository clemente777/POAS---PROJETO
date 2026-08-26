from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoUpdate,
    AtendimentoResponse
)

from backend.services.implementations.atendimento_service_impl import (
    AtendimentoServiceImpl
)

from backend.repositories.atendimento_repository import (
    AtendimentoRepository
)

from backend.models.usuario_model import Usuarios

from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil


router = APIRouter(
    prefix="/atendimentos",
    tags=["Atendimentos"]
)


# ==========================================================
# DEPENDÊNCIA SERVICE
# ==========================================================

def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(get_current_user)
):

    repository = AtendimentoRepository(
        session
    )

    return AtendimentoServiceImpl(
        repository,
        usuario_logado
    )


# ==========================================================
# CRIAR ATENDIMENTO
# SOMENTE VETERINÁRIO E ADMINISTRADOR
# ==========================================================

@router.post(
    "/",
    response_model=AtendimentoResponse,
    status_code=201
)
def criar(
    atendimento: AtendimentoCreate,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Veterinário",
            "Administrador"
        )
    ),

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.criar(
        atendimento
    )


# ==========================================================
# LISTAR ATENDIMENTOS
# CLIENTE / VETERINÁRIO / ADMINISTRADOR
# ==========================================================

@router.get(
    "/",
    response_model=list[AtendimentoResponse]
)
def listar(
    skip: int = 0,
    limit: int = 10,
    animal_id: int | None = None,
    usuario_id: int | None = None,
    diagnostico: str | None = None,
    data: datetime | None = None,
    sort_by: str = "data_atendimento",
    order: str = "asc",

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Cliente",
            "Veterinário",
            "Administrador"
        )
    ),

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.listar(
        skip=skip,
        limit=limit,
        animal_id=animal_id,
        usuario_id=usuario_id,
        diagnostico=diagnostico,
        data=data,
        sort_by=sort_by,
        order=order
    )

# ==========================================================
# HISTÓRICO DO ANIMAL
# CLIENTE / VETERINÁRIO / ADMINISTRADOR
# ==========================================================

@router.get(
    "/historico/{animal_id}"
)
def historico(
    animal_id: int,
    skip: int = 0,
    limit: int = 10,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Cliente",
            "Veterinário",
            "Administrador"
        )
    ),

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.historico_completo(
        animal_id,
        skip,
        limit
    )   
# ==========================================================
# BUSCAR ATENDIMENTO
# CLIENTE / VETERINÁRIO / ADMINISTRADOR
# ==========================================================

@router.get(
    "/{id}",
    response_model=AtendimentoResponse
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

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.buscar_por_id(
        id
    )


# ==========================================================
# ATUALIZAR ATENDIMENTO
# SOMENTE VETERINÁRIO E ADMINISTRADOR
# ==========================================================

@router.put(
    "/{id}",
    response_model=AtendimentoResponse
)
def atualizar(
    id: int,
    atendimento: AtendimentoUpdate,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Veterinário",
            "Administrador"
        )
    ),

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.atualizar(
        id,
        atendimento
    )


# ==========================================================
# CANCELAR ATENDIMENTO
# SOMENTE VETERINÁRIO E ADMINISTRADOR
# ==========================================================

@router.patch(
    "/{id}/cancelar",
    response_model=AtendimentoResponse
)
def cancelar(
    id: int,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Veterinário",
            "Administrador"
        )
    ),

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.cancelar(
        id
    )


# ==========================================================
# DELETAR
# SOMENTE ADMINISTRADOR
# ==========================================================

@router.delete(
    "/{id}"
)
def deletar(
    id: int,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),

    service: AtendimentoServiceImpl = Depends(
        get_service
    )
):

    return service.deletar(
        id
    )


