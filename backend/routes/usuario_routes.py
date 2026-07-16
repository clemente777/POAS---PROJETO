from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl
from backend.models.usuario_model import Usuarios

from backend.auth.dependencies import UsuarioLogado

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)



def get_service(
    session: Session = Depends(get_session)
):
    return UsuarioServiceImpl(session)



# ==================================================
# CRIAR USUÁRIO
# Não precisa estar logado
# ==================================================

@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=201
)
def criar(
    usuario: UsuarioCreate,
    service: UsuarioServiceImpl = Depends(get_service),
):

    return service.criar(usuario)





# ==================================================
# LISTAR USUÁRIOS
# Precisa estar autenticado
# ==================================================

@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def listar(
    skip: int = 0,
    limit: int = 10,
    nome: str | None = None,
    email: str | None = None,
    sort_by: str = "id",
    order: str = "asc",

    usuario_logado: Usuarios = Depends(get_current_user),

    service: UsuarioServiceImpl = Depends(get_service),
):

    return service.listar(
        skip=skip,
        limit=limit,
        nome=nome,
        email=email,
        sort_by=sort_by,
        order=order,
    )





# ==================================================
# BUSCAR USUÁRIO
# ==================================================

@router.get(
    "/{id}",
    response_model=UsuarioResponse
)
def buscar(
    id:int,

    usuario_logado: Usuarios = Depends(get_current_user),

    service: UsuarioServiceImpl = Depends(get_service),
):

    usuario = service.buscar_por_id(id)


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )


    return usuario





# ==================================================
# ATUALIZAR USUÁRIO
# ==================================================

@router.put(
    "/{id}",
    response_model=UsuarioResponse
)
def atualizar(
    id:int,
    usuario:UsuarioUpdate,

    usuario_logado: Usuarios = Depends(get_current_user),

    service: UsuarioServiceImpl = Depends(get_service),
):

    usuario_atualizado = service.atualizar(
        id,
        usuario
    )


    if not usuario_atualizado:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )


    return usuario_atualizado





# ==================================================
# DELETAR USUÁRIO
# ==================================================

@router.delete(
    "/{id}",
    status_code=204
)
def deletar(
    id:int,

    usuario_logado: Usuarios = Depends(get_current_user),

    service: UsuarioServiceImpl = Depends(get_service),
):

    """
    Regra:

    Usuário só pode excluir
    a própria conta.


    Exemplo:

    Token pertence ao usuário ID 5


    Tentativa:

    DELETE /usuarios/8


    Resultado:

    Bloqueado.
    """


    if usuario_logado.id != id:

        raise HTTPException(
            status_code=403,
            detail="Você só pode excluir sua própria conta."
        )



    removido = service.deletar(id)



    if not removido:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )



    return Response(
        status_code=204
    )