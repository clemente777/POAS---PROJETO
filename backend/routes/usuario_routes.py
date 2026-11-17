from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.cliente_repository import ClienteRepository
from backend.repositories.usuario_repository import UsuarioRepository
from backend.schemas.usuario_schema import (
    UsuarioAdminCreate,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ==========================================================
# DEPENDÊNCIAS DE AUTORIZAÇÃO
# ==========================================================

AdministradorDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Administrador")),
]

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]


# ==========================================================
# DEPENDÊNCIA SERVICE PÚBLICO
# ==========================================================


def get_service_publico(
    session: Annotated[Session, Depends(get_session)],
):
    repository = UsuarioRepository(session)
    cliente_repository = ClienteRepository(session)

    return UsuarioServiceImpl(
        repository=repository,
        cliente_repository=cliente_repository,
    )


# ==========================================================
# DEPENDÊNCIA SERVICE AUTENTICADO
# ==========================================================


def get_service(
    session: Annotated[Session, Depends(get_session)],
    usuario_logado: UsuarioLogadoDep,
):
    repository = UsuarioRepository(session)
    cliente_repository = ClienteRepository(session)

    return UsuarioServiceImpl(
        repository=repository,
        cliente_repository=cliente_repository,
        usuario_logado=usuario_logado,
    )


UsuarioServicePublicoDep = Annotated[
    UsuarioServiceImpl,
    Depends(get_service_publico),
]

UsuarioServiceDep = Annotated[
    UsuarioServiceImpl,
    Depends(get_service),
]


# ==========================================================
# CRIAR USUÁRIO
#
# Público
#
# Sempre cria Cliente
# ==========================================================


@router.post("/", response_model=UsuarioResponse, status_code=201)
def criar(
    usuario: UsuarioCreate,
    service: UsuarioServicePublicoDep,
):
    return service.criar(usuario)


# ==========================================================
# CRIAR USUÁRIO POR ADMIN
#
# Apenas Administrador
# ==========================================================


@router.post("/admin", response_model=UsuarioResponse, status_code=201)
def criar_usuario_admin(
    usuario: UsuarioAdminCreate,
    usuario_logado: AdministradorDep,
    service: UsuarioServiceDep,
):
    return service.criar_por_admin(usuario)


# ==========================================================
# LISTAR USUÁRIOS
#
# Apenas Administrador
# ==========================================================


@router.get("/", response_model=list[UsuarioResponse])
def listar(
    skip: int = 0,
    limit: int = 10,
    nome: str | None = None,
    email: str | None = None,
    perfil: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    usuario_logado: AdministradorDep = None,
    service: UsuarioServiceDep = None,
):
    return service.listar(
        skip=skip,
        limit=limit,
        nome=nome,
        email=email,
        perfil=perfil,
        sort_by=sort_by,
        order=order,
    )


# ==========================================================
# BUSCAR USUÁRIO
#
# Apenas Administrador
# ==========================================================


@router.get("/{id}", response_model=UsuarioResponse)
def buscar(
    id: int,
    usuario_logado: AdministradorDep,
    service: UsuarioServiceDep,
):
    return service.buscar_por_id(id)


# ==========================================================
# ATUALIZAR USUÁRIO
#
# Apenas Administrador pela rota.
# O Service também valida as regras.
# ==========================================================


@router.put("/{id}", response_model=UsuarioResponse)
def atualizar(
    id: int,
    usuario: UsuarioUpdate,
    usuario_logado: AdministradorDep,
    service: UsuarioServiceDep,
):
    return service.atualizar(id, usuario)


# ==========================================================
# DELETAR USUÁRIO
#
# Apenas Administrador
# ==========================================================


@router.delete("/{id}", status_code=204)
def deletar(
    id: int,
    usuario_logado: AdministradorDep,
    service: UsuarioServiceDep,
):
    service.deletar(id)

    return Response(status_code=204)
