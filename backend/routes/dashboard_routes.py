from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session


from backend.database.database import get_session

from backend.auth.dependencies import get_current_user


from backend.models.usuario_model import Usuarios


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





# ==================================
# DASHBOARD ADMIN
# ==================================


@router.get("/admin", response_model=DashboardResponse)
def dashboard_admin(
    session: Session = Depends(get_session),
    usuario: Usuarios = Depends(get_current_user)
):
    print("Entrou na rota")

    if usuario.perfil != "Administrador":
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem acessar."
        )

    service = DashboardServiceImpl(
        session=session,
        usuario=usuario
    )

    try:
        dados = service.dashboard_admin()
        print(dados)
        return dados

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise





# ==================================
# DASHBOARD VETERINÁRIO
# ==================================



@router.get(
    "/veterinario",
    response_model=DashboardVeterinarioResponse
)
def dashboard_veterinario(


    session: Session = Depends(get_session),


    usuario: Usuarios = Depends(get_current_user)

):


    if usuario.perfil != "Veterinário":

        raise HTTPException(

            status_code=403,

            detail="Apenas veterinários podem acessar."

        )




    service = DashboardServiceImpl(

        session=session,

        usuario=usuario

    )



    return service.dashboard_veterinario()

# ==================================
# DASHBOARD CLIENTE
# ==================================


@router.get("/cliente", response_model=DashboardClienteResponse)
def dashboard_cliente(
    session: Session = Depends(get_session),
    usuario: Usuarios = Depends(get_current_user)
):

    if usuario.perfil != "Cliente":
        raise HTTPException(
            status_code=403,
            detail="Apenas clientes podem acessar."
        )

    service = DashboardServiceImpl(
        session=session,
        usuario=usuario
    )

    return service.dashboard_cliente()