from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session


from backend.database.database import get_session


from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioAdminCreate
)


from backend.services.implementations.usuario_service_impl import (
    UsuarioServiceImpl
)


from backend.models.usuario_model import Usuarios


from backend.auth.permissions import exigir_perfil



router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)



# ==========================================================
# SERVICE
# ==========================================================


def get_service(
    session: Session = Depends(get_session)
):

    return UsuarioServiceImpl(
        session
    )



# ==========================================================
# CRIAR USUÁRIO
#
# Público
#
# Sempre cria Cliente
# ==========================================================


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=201
)
def criar(

    usuario: UsuarioCreate,


    service: UsuarioServiceImpl = Depends(
        get_service
    )

):

    return service.criar(
        usuario
    )





# ==========================================================
# CRIAR USUÁRIO POR ADMIN
#
# Apenas Administrador
# ==========================================================


@router.post(
    "/admin",
    response_model=UsuarioResponse
)
def criar_usuario_admin(

    usuario: UsuarioAdminCreate,


    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),


    service: UsuarioServiceImpl = Depends(
        get_service
    )

):

    return service.criar_por_admin(
        usuario
    )





# ==========================================================
# LISTAR USUÁRIOS
#
# Apenas Administrador
# ==========================================================


@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def listar(

    skip: int = 0,

    limit: int = 10,

    nome: str | None = None,

    email: str | None = None,

    perfil: str | None = None,

    sort_by: str = "id",

    order: str = "asc",



    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),


    service: UsuarioServiceImpl = Depends(
        get_service
    )

):


    return service.listar(

        skip=skip,

        limit=limit,

        nome=nome,

        email=email,

        perfil=perfil,

        sort_by=sort_by,

        order=order

    )





# ==========================================================
# BUSCAR USUÁRIO
#
# Apenas Administrador
# ==========================================================


@router.get(
    "/{id}",
    response_model=UsuarioResponse
)
def buscar(

    id: int,


    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),


    service: UsuarioServiceImpl = Depends(
        get_service
    )

):


    return service.buscar_por_id(
        id
    )





# ==========================================================
# ATUALIZAR USUÁRIO
#
# Apenas Administrador
#
# Controle também no Service
# ==========================================================


@router.put(
    "/{id}",
    response_model=UsuarioResponse
)
def atualizar(

    id: int,


    usuario: UsuarioUpdate,


    usuario_logado: Usuarios = Depends(
        exigir_perfil(
            "Administrador"
        )
    ),


    service: UsuarioServiceImpl = Depends(
        get_service
    )

):


    return service.atualizar(

        id,

        usuario,

        usuario_logado

    )





# ==========================================================
# DELETAR USUÁRIO
#
# Apenas Administrador
#
# Controle também no Service
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


    service: UsuarioServiceImpl = Depends(
        get_service
    )

    ):


        service.deletar(

            id,

            usuario_logado

        )


        return Response(
            status_code=204
        )