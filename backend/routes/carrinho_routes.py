from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado

from backend.models.models import Carrinhos

from backend.services.implementations.carrinho_service_impl import (
    CarrinhoServiceImpl
)

SessionDep = Annotated[
    Session,
    Depends(get_session)
]

router = APIRouter(
    prefix="/carrinhos",
    tags=["carrinhos"]
)


@router.get("/", response_model=list[Carrinhos])
def get_carrinhos(
    session: SessionDep,
    usuario: UsuarioLogado
):
    return CarrinhoServiceImpl(
        session
    ).listar_carrinhos()


@router.get("/{id}", response_model=Carrinhos)
def get_carrinho_by_id(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    return CarrinhoServiceImpl(
        session
    ).buscar_carrinho_por_id(id)


@router.post("/", response_model=Carrinhos)
def create_carrinho(
    carrinho: Carrinhos,
    session: SessionDep,
    usuario: UsuarioLogado
):
    return CarrinhoServiceImpl(
        session
    ).criar_carrinho(carrinho)


@router.put("/{id}")
def update_carrinho(
    id: int,
    carrinho: Carrinhos,
    session: SessionDep,
    usuario: UsuarioLogado
):
    atualizado = CarrinhoServiceImpl(
        session
    ).atualizar_carrinho(
        id,
        carrinho
    )

    if not atualizado:
        return {
            "erro": "Carrinho não encontrado"
        }

    return {
        "mensagem": "Carrinho atualizado"
    }


@router.delete("/{id}")
def delete_carrinho(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    deletado = CarrinhoServiceImpl(
        session
    ).deletar_carrinho(id)

    if not deletado:
        return {
            "erro": "Carrinho não encontrado"
        }

    return {
        "mensagem": "Carrinho removido"
    }