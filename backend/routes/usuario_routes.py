from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado

from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)

from backend.services.implementations.usuario_service_impl import (
    UsuarioServiceImpl
)

from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[
    Session,
    Depends(get_session)
]

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/", response_model=list[UsuarioResponse])
def get_usuarios(
    session: SessionDep,
    usuario: UsuarioLogado
):
    return UsuarioServiceImpl(session).listar_usuarios()


@router.get("/{id}", response_model=UsuarioResponse)
def get_usuario_by_id(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    return UsuarioServiceImpl(session).buscar_usuario_por_id(id)


@router.post("/", response_model=UsuarioResponse)
def create_usuario(
    usuario: UsuarioCreate,
    session: SessionDep
):
    return UsuarioServiceImpl(session).criar_usuario(usuario)


@router.put("/{id}")
def update_usuario(
    id: int,
    usuario: UsuarioUpdate,
    session: SessionDep,
    usuario_logado: UsuarioLogado
):
    atualizado = UsuarioServiceImpl(
        session
    ).atualizar_usuario(id, usuario)

    if not atualizado:
        return {"erro": "Usuário não encontrado"}

    return {"mensagem": "Usuário atualizado"}


@router.delete("/{id}")
def delete_usuario(
    id: int,
    session: SessionDep,
    usuario_logado: UsuarioLogado
):
    sucesso = UsuarioServiceImpl(
        session
    ).deletar_usuario(id)

    if not sucesso:
        return {"erro": "Usuário não encontrado"}

    return {"mensagem": "Usuário removido"}