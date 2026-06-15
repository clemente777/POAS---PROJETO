from backend.models.models import Clientes
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado

from backend.services.implementations.cliente_service_impl import (
    ClienteServiceImpl
)

from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[
    Session,
    Depends(get_session)
]

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"]
)

@router.get("/", response_model=list[Clientes])
def get_clientes(
    session: SessionDep,
    usuario: UsuarioLogado
):
    service = ClienteServiceImpl(session)
    return service.listar_clientes()


@router.get("/{id}", response_model=Clientes)
def get_cliente_by_id(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    service = ClienteServiceImpl(session)
    return service.buscar_cliente_por_id(id)


@router.post("/", response_model=Clientes)
def create_cliente(
    cliente: Clientes,
    session: SessionDep
):
    service = ClienteServiceImpl(session)
    return service.criar_cliente(cliente)


@router.delete("/{id}")
def delete_cliente(
    id: int,
    session: SessionDep,
    usuario_logado: UsuarioLogado
):
    service = ClienteServiceImpl(session)

    sucesso = service.deletar_cliente(id)

    if not sucesso:
        return {
            "erro": "Cliente não encontrado"
        }

    return {
        "mensagem": "Cliente removido"
    }


@router.put("/{id}")
def update_cliente(
    id: int,
    cliente: Clientes,
    session: SessionDep,
    usuario_logado: UsuarioLogado
):
    service = ClienteServiceImpl(session)

    cliente_atualizado = service.atualizar_cliente(
        id,
        cliente
    )

    if not cliente_atualizado:
        return {"erro": "Cliente não encontrado"}

    return {"mensagem": "Cliente atualizado"}