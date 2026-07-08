from fastapi import APIRouter, Depends,Response, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl
from backend.auth.dependencies import get_current_user
router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return UsuarioServiceImpl(session)


@router.post("/", response_model=UsuarioResponse)
def criar(usuario: UsuarioCreate, service=Depends(get_service)):
    return service.criar(usuario)


@router.get("/", response_model=list[UsuarioResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=UsuarioResponse)
def buscar(id: int, service=Depends(get_service)):

    usuario = service.buscar_por_id(id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario


@router.put("/{id}", response_model=UsuarioResponse)
def atualizar(
    id: int,
    usuario: UsuarioUpdate,
    service=Depends(get_service)
):

    usuario_atualizado = service.atualizar(id, usuario)

    if not usuario_atualizado:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario_atualizado

@router.delete("/{id}", status_code=204)
def deletar(id: int, service=Depends(get_service)):

    removido = service.deletar(id)

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return Response(status_code=204)