from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.auth.dependencies import get_current_user

from backend.models.usuario_model import Usuarios

from backend.repositories.dashboard_repository import (
    DashboardRepository
)

from backend.services.implementations.dashboard_service_impl import (
    DashboardServiceImpl
)

from backend.schemas.dashboard_schema import (
    DashboardResponse,
    DashboardVeterinarioResponse,
    DashboardClienteResponse
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ============================================================
# DEPENDÊNCIA DO SERVICE
# ============================================================

def get_service(
    session: Session = Depends(get_session),
    usuario: Usuarios = Depends(get_current_user)
):
    repository = DashboardRepository(session)

    return DashboardServiceImpl(
        repository=repository,
        usuario=usuario
    )


# ============================================================
# DASHBOARD ADMIN
# ============================================================

@router.get(
    "/admin",
    response_model=DashboardResponse
)
def dashboard_admin(
    service: DashboardServiceImpl = Depends(get_service),
    usuario: Usuarios = Depends(get_current_user)
):
    if usuario.perfil != "Administrador":
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem acessar."
        )

    return service.dashboard_admin()


# ============================================================
# DASHBOARD VETERINÁRIO
# ============================================================

@router.get(
    "/veterinario",
    response_model=DashboardVeterinarioResponse
)
def dashboard_veterinario(
    service: DashboardServiceImpl = Depends(get_service),
    usuario: Usuarios = Depends(get_current_user)
):
    if usuario.perfil != "Veterinário":
        raise HTTPException(
            status_code=403,
            detail="Apenas veterinários podem acessar."
        )

    return service.dashboard_veterinario()


# ============================================================
# DASHBOARD CLIENTE
# ============================================================

@router.get(
    "/cliente",
    response_model=DashboardClienteResponse
)
def dashboard_cliente(
    service: DashboardServiceImpl = Depends(get_service),
    usuario: Usuarios = Depends(get_current_user)
):
    if usuario.perfil != "Cliente":
        raise HTTPException(
            status_code=403,
            detail="Apenas clientes podem acessar."
        )

    return service.dashboard_cliente()

