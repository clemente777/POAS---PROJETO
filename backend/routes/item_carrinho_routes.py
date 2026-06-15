from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado

from backend.models.models import ItensCarrinho

from backend.services.implementations.item_carrinho_service_impl import (
    ItemCarrinhoServiceImpl
)

SessionDep = Annotated[
    Session,
    Depends(get_session)
]

router = APIRouter(
    prefix="/itens-carrinho",
    tags=["itens-carrinho"]
)


@router.get("/", response_model=list[ItensCarrinho])
def get_itens_carrinho(
    session: SessionDep,
    usuario: UsuarioLogado
):
    return ItemCarrinhoServiceImpl(
        session
    ).listar_itens()


@router.get("/{id}", response_model=ItensCarrinho)
def get_item_carrinho_by_id(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    return ItemCarrinhoServiceImpl(
        session
    ).buscar_item_por_id(id)


@router.post("/", response_model=ItensCarrinho)
def create_item_carrinho(
    item: ItensCarrinho,
    session: SessionDep,
    usuario: UsuarioLogado
):
    return ItemCarrinhoServiceImpl(
        session
    ).criar_item(item)


@router.put("/{id}")
def update_item_carrinho(
    id: int,
    item: ItensCarrinho,
    session: SessionDep,
    usuario: UsuarioLogado
):
    atualizado = ItemCarrinhoServiceImpl(
        session
    ).atualizar_item(
        id,
        item
    )

    if not atualizado:
        return {
            "erro": "Item não encontrado"
        }

    return {
        "mensagem": "Item atualizado"
    }


@router.delete("/{id}")
def delete_item_carrinho(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    deletado = ItemCarrinhoServiceImpl(
        session
    ).deletar_item(id)

    if not deletado:
        return {
            "erro": "Item não encontrado"
        }

    return {
        "mensagem": "Item removido"
    }