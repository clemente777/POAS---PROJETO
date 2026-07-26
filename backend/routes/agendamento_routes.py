from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime


from backend.database.database import get_session


from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate,
    AgendamentoResponse
)


from backend.services.implementations.agendamento_service_impl import (
    AgendamentoServiceImpl
)


from backend.models.usuario_model import Usuarios


from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil



router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)



# ==================================================
# SERVICE
# ==================================================


def get_service(

    session: Session = Depends(get_session),

    usuario_logado: Usuarios = Depends(get_current_user)

):

    return AgendamentoServiceImpl(

        session,

        usuario_logado

    )



# ==================================================
# CRIAR
# ==================================================


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





# ==================================================
# LISTAR
# ==================================================


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





# ==================================================
# BUSCAR POR ID
# ==================================================


@router.get(
    "/{id}",
    response_model=AgendamentoResponse
)
def buscar(

    id:int,


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





# ==================================================
# ATUALIZAR
# ==================================================


@router.put(
    "/{id}",
    response_model=AgendamentoResponse
)
def atualizar(

    id:int,

    agendamento:AgendamentoUpdate,


    usuario_logado:Usuarios = Depends(

        exigir_perfil(

            "Veterinário",

            "Administrador"

        )

    ),


    service:AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.atualizar(

        id,

        agendamento

    )






# ==================================================
# CANCELAR
# Veterinário, Cliente e Administrador
# ==================================================


@router.post(
    "/{id}/cancelar",
    response_model=AgendamentoResponse
)
def cancelar(

    id:int,


    usuario_logado:Usuarios = Depends(

        exigir_perfil(
             "Cliente",
            "Veterinário",

            "Administrador"

        )

    ),


    service:AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.cancelar(
        id
    )






@router.delete(
    "/{id}"
)
def deletar(

    id:int,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),

    service: AgendamentoServiceImpl = Depends(
        get_service
    )

):

    return service.deletar(
        id
    )