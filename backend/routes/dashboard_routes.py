from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.dashboard_repository import DashboardRepository
from backend.schemas.dashboard_schema import (
    DashboardClienteResponse,
    DashboardResponse,
    DashboardVeterinarioResponse,
)
from backend.services.implementations.dashboard_service_impl import DashboardServiceImpl

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ============================================================
# TIPOS DAS DEPENDÊNCIAS
# ============================================================

SessionDep = Annotated[Session, Depends(get_session)]
UsuarioDep = Annotated[Usuarios, Depends(get_current_user)]


# ============================================================
# DEPENDÊNCIA DO SERVICE
# ============================================================


def get_service(
    session: SessionDep,
    usuario: UsuarioDep,
):
    repository = DashboardRepository(session)

    return DashboardServiceImpl(
        repository=repository,
        usuario=usuario,
    )


ServiceDep = Annotated[DashboardServiceImpl, Depends(get_service)]


# ============================================================
# DASHBOARD ADMIN
# ============================================================


@router.get("/admin", response_model=DashboardResponse)
def dashboard_admin(
    service: ServiceDep,
    usuario: UsuarioDep,
):
    if usuario.perfil != "Administrador":
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem acessar.",
        )

    return service.dashboard_admin()


# ============================================================
# DASHBOARD VETERINÁRIO
# ============================================================


@router.get("/veterinario", response_model=DashboardVeterinarioResponse)
def dashboard_veterinario(
    service: ServiceDep,
    usuario: UsuarioDep,
):
    if usuario.perfil != "Veterinário":
        raise HTTPException(
            status_code=403,
            detail="Apenas veterinários podem acessar.",
        )

    return service.dashboard_veterinario()


# ============================================================
# DASHBOARD CLIENTE
# ============================================================


@router.get("/cliente", response_model=DashboardClienteResponse)
def dashboard_cliente(
    service: ServiceDep,
    usuario: UsuarioDep,
):
    if usuario.perfil != "Cliente":
        raise HTTPException(
            status_code=403,
            detail="Apenas clientes podem acessar.",
        )

    return service.dashboard_cliente()
