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

router = APIRouter(prefix="/usuarios", tags=["Usuarios"],)


def get_service(session: Session = Depends(get_session)):
    return UsuarioServiceImpl(session)


# Cadastro de usuário NÃO precisa de autenticação
@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar(
    usuario: UsuarioCreate,
    service: UsuarioServiceImpl = Depends(get_service),
):
    return service.criar(usuario)


# Listar usuários precisa de autenticação
@router.get(
    "/",
    response_model=list[UsuarioResponse],
    dependencies=[Depends(get_current_user)],
)
def listar(service: UsuarioServiceImpl = Depends(get_service)):
    return service.listar()


# Buscar usuário precisa de autenticação
@router.get(
    "/{id}",
    response_model=UsuarioResponse,
    dependencies=[Depends(get_current_user)],
)
def buscar(
    id: int,
    service: UsuarioServiceImpl = Depends(get_service),
):
    usuario = service.buscar_por_id(id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado",
        )

    return usuario


# Atualizar usuário precisa de autenticação
@router.put(
    "/{id}",
    response_model=UsuarioResponse,
    dependencies=[Depends(get_current_user)],
)
def atualizar(
    id: int,
    usuario: UsuarioUpdate,
    service: UsuarioServiceImpl = Depends(get_service),
):
    usuario_atualizado = service.atualizar(id, usuario)

    if not usuario_atualizado:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado",
        )

    return usuario_atualizado


# Deletar usuário precisa de autenticação
@router.delete(
    "/{id}",
    status_code=204,
    dependencies=[Depends(get_current_user)],
)
def deletar(
    id: int,
    service: UsuarioServiceImpl = Depends(get_service),
):
    removido = service.deletar(id)

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado",
        )

    return Response(status_code=204)