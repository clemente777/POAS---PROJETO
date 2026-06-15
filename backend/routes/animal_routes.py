from backend.models.models import Animais
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado

from backend.services.implementations.animal_service_impl import (
    AnimalServiceImpl
)

from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[
    Session,
    Depends(get_session)
]

router = APIRouter(
    prefix="/animais",
    tags=["animais"]
)

@router.get("/", response_model=list[Animais])
def get_animais(
    session: SessionDep,
    usuario: UsuarioLogado
):
    service = AnimalServiceImpl(session)
    return service.listar_animais()


@router.get("/{id}", response_model=Animais)
def get_animal_by_id(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    service = AnimalServiceImpl(session)
    return service.buscar_animal_por_id(id)


@router.post("/", response_model=Animais)
def create_animal(
    animal: Animais,
    session: SessionDep
):
    service = AnimalServiceImpl(session)
    return service.criar_animal(animal)


@router.put("/{id}")
def update_animal(
    id: int,
    animal: Animais,
    session: SessionDep,
    usuario: UsuarioLogado
):
    service = AnimalServiceImpl(session)

    if not service.atualizar_animal(
        id,
        animal
    ):
        return {"erro": "Animal não encontrado"}

    return {"mensagem": "Animal atualizado"}


@router.delete("/{id}")
def delete_animal(
    id: int,
    session: SessionDep,
    usuario: UsuarioLogado
):
    service = AnimalServiceImpl(session)

    if not service.deletar_animal(id):
        return {"erro": "Animal não encontrado"}

    return {"mensagem": "Animal removido"}