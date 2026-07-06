from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


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
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=UsuarioResponse)
def atualizar(id: int, usuario: UsuarioUpdate, service=Depends(get_service)):
    return service.atualizar(id, usuario)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}