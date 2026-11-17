from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.atendimento_repository import AtendimentoRepository
from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoResponse,
    AtendimentoUpdate,
)
from backend.services.implementations.atendimento_service_impl import (
    AtendimentoServiceImpl,
)

router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])


# ==========================================================
# DEPENDÊNCIAS
# ==========================================================

SessionDep = Annotated[Session, Depends(get_session)]

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]

VeterinarioAdminDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Veterinário", "Administrador")),
]

ClienteVeterinarioAdminDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Cliente", "Veterinário", "Administrador")),
]

AdministradorDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Administrador")),
]


# ==========================================================
# DEPENDÊNCIA DO SERVICE
# ==========================================================


def get_service(
    session: SessionDep,
    usuario_logado: UsuarioLogadoDep,
):
    repository = AtendimentoRepository(session)

    return AtendimentoServiceImpl(repository, usuario_logado)


AtendimentoServiceDep = Annotated[
    AtendimentoServiceImpl,
    Depends(get_service),
]


# ==========================================================
# CRIAR ATENDIMENTO
# SOMENTE VETERINÁRIO E ADMINISTRADOR
# ==========================================================


@router.post("/", response_model=AtendimentoResponse, status_code=201)
def criar(
    atendimento: AtendimentoCreate,
    usuario_logado: VeterinarioAdminDep,
    service: AtendimentoServiceDep,
):
    return service.criar(atendimento)


# ==========================================================
# LISTAR ATENDIMENTOS
# CLIENTE / VETERINÁRIO / ADMINISTRADOR
# ==========================================================


@router.get("/", response_model=list[AtendimentoResponse])
def listar(
    usuario_logado: ClienteVeterinarioAdminDep,
    service: AtendimentoServiceDep,
    skip: int = 0,
    limit: int = 10,
    animal_id: int | None = None,
    usuario_id: int | None = None,
    diagnostico: str | None = None,
    data: datetime | None = None,
    sort_by: str = "data_atendimento",
    order: str = "asc",
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


# ==========================================================
# HISTÓRICO DO ANIMAL
# CLIENTE / VETERINÁRIO / ADMINISTRADOR
# ==========================================================


@router.get("/historico/{animal_id}")
def historico(
    animal_id: int,
    usuario_logado: ClienteVeterinarioAdminDep,
    service: AtendimentoServiceDep,
    skip: int = 0,
    limit: int = 10,
):
    return service.historico_completo(animal_id, skip, limit)


# ==========================================================
# BUSCAR ATENDIMENTO
# CLIENTE / VETERINÁRIO / ADMINISTRADOR
# ==========================================================


@router.get("/{id}", response_model=AtendimentoResponse)
def buscar(
    id: int,
    usuario_logado: ClienteVeterinarioAdminDep,
    service: AtendimentoServiceDep,
):
    return service.buscar_por_id(id)


# ==========================================================
# ATUALIZAR ATENDIMENTO
# SOMENTE VETERINÁRIO E ADMINISTRADOR
# ==========================================================


@router.put("/{id}", response_model=AtendimentoResponse)
def atualizar(
    id: int,
    atendimento: AtendimentoUpdate,
    usuario_logado: VeterinarioAdminDep,
    service: AtendimentoServiceDep,
):
    return service.atualizar(id, atendimento)


# ==========================================================
# CANCELAR ATENDIMENTO
# SOMENTE VETERINÁRIO E ADMINISTRADOR
# ==========================================================


@router.patch("/{id}/cancelar", response_model=AtendimentoResponse)
def cancelar(
    id: int,
    usuario_logado: VeterinarioAdminDep,
    service: AtendimentoServiceDep,
):
    return service.cancelar(id)


# ==========================================================
# DELETAR
# SOMENTE ADMINISTRADOR
#
# A operação é bloqueada pelo Service porque o histórico
# dos atendimentos deve ser preservado.
# ==========================================================


@router.delete("/{id}")
def deletar(
    id: int,
    usuario_logado: AdministradorDep,
    service: AtendimentoServiceDep,
):
    return service.deletar(id)
