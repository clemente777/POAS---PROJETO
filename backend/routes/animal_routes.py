from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.animal_schema import (
    AnimalCreate,
    AnimalUpdate,
    AnimalResponse
)
from backend.services.implementations.animal_service_impl import AnimalServiceImpl

router = APIRouter(prefix="/animais", tags=["Animais"])


def get_service(session: Session = Depends(get_session)):
    return AnimalServiceImpl(session)


@router.post("/", response_model=AnimalResponse)
def criar(animal: AnimalCreate, service=Depends(get_service)):
    return service.criar(animal)


@router.get("/", response_model=list[AnimalResponse])
def listar(service=Depends(get_service)):
    return service.listar()


@router.get("/{id}", response_model=AnimalResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=AnimalResponse)
def atualizar(id: int, animal: AnimalUpdate, service=Depends(get_service)):
    return service.atualizar(id, animal)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}