from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse
)

from backend.services.implementations.cliente_service_impl import (
    ClienteServiceImpl
)

from backend.models.usuario_model import Usuarios

from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# ==========================================================
# DEPENDÊNCIA SERVICE
# ==========================================================

def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(get_current_user)
):

    return ClienteServiceImpl(
        session,
        usuario_logado
    )


# ==========================================================
# CRIAR CLIENTE
# ==========================================================

@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=201
)
def criar(

    cliente: ClienteCreate,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador",
            "Cliente"
        )
    ),

    service: ClienteServiceImpl = Depends(
        get_service
    )

):

    return service.criar(
        cliente
    )


# ==========================================================
# LISTAR CLIENTES
# ==========================================================

@router.get(
    "/",
    response_model=list[ClienteResponse]
)
def listar(

    skip: int = 0,

    limit: int = 10,

    nome: str | None = None,

    cpf: str | None = None,

    email: str | None = None,

    sort_by: str = "id",

    order: str = "asc",

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador",
            "Veterinário",
            "Cliente"
        )
    ),

    service: ClienteServiceImpl = Depends(
        get_service
    )

):

    return service.listar(
        skip=skip,
        limit=limit,
        nome=nome,
        cpf=cpf,
        email=email,
        sort_by=sort_by,
        order=order
    )


# ==========================================================
# BUSCAR CLIENTE POR ID
# ==========================================================

@router.get(
    "/{id}",
    response_model=ClienteResponse
)
def buscar(

    id: int,

    usuario_logado: Usuarios = Depends(
        get_current_user
    ),

    service: ClienteServiceImpl = Depends(
        get_service
    )

):

    return service.buscar_por_id(
        id
    )


# ==========================================================
# ATUALIZAR CLIENTE
# ==========================================================

@router.put(
    "/{id}",
    response_model=ClienteResponse
)
def atualizar(

    id: int,

    cliente: ClienteUpdate,

    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador",
            "Cliente"
        )
    ),

    service: ClienteServiceImpl = Depends(
        get_service
    )

):

    return service.atualizar(
        id,
        cliente
    )


# ==========================================================
# DELETAR CLIENTE
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

    service: ClienteServiceImpl = Depends(
        get_service
    )

):

    service.deletar(
        id
    )

    return Response(
        status_code=204
    )