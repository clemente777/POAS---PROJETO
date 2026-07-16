from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.schemas.animal_schema import (
    AnimalCreate,
    AnimalUpdate,
    AnimalResponse
)
from backend.services.implementations.animal_service_impl import AnimalServiceImpl
from backend.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/animais",
    tags=["Animais"],
    dependencies=[Depends(get_current_user)]  # 🔒 protege tudo aqui
)

def get_service(session: Session = Depends(get_session)):
    return AnimalServiceImpl(session)


@router.post("/", response_model=AnimalResponse)
def criar(animal: AnimalCreate, service=Depends(get_service)):
    return service.criar(animal)


#PAGINAÇÃO e Filtro
@router.get("/",response_model=list[AnimalResponse])
def listar(
    skip: int = 0,
    limit: int = 10,
    nome: str | None = None,
    especie: str | None = None,
    raca: str | None = None,
    idade: int | None = None,
    cliente_id: int | None = None,
    sort_by: str = "id",
    order: str = "asc",
    service: AnimalServiceImpl = Depends(get_service),
):
    return service.listar(
        skip=skip,
        limit=limit,
        nome=nome,
        especie=especie,
        raca=raca,
        idade=idade,
        cliente_id=cliente_id,
        sort_by=sort_by,
        order=order,
    )



@router.get("/{id}", response_model=AnimalResponse)
def buscar(id: int, service=Depends(get_service)):
    return service.buscar_por_id(id)


@router.put("/{id}", response_model=AnimalResponse)
def atualizar(id: int, animal: AnimalUpdate, service=Depends(get_service)):
    return service.atualizar(id, animal)


@router.delete("/{id}")
def deletar(id: int, service=Depends(get_service)):
    return {"success": service.deletar(id)}