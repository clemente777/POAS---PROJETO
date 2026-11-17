from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.animal_repository import AnimalRepository
from backend.repositories.atendimento_repository import AtendimentoRepository
from backend.schemas.animal_schema import AnimalCreate, AnimalResponse, AnimalUpdate
from backend.schemas.historico_schema import AnimalHistoricoResponse
from backend.services.implementations.animal_service_impl import AnimalServiceImpl
from backend.services.implementations.atendimento_service_impl import (
    AtendimentoServiceImpl,
)

router = APIRouter(prefix="/animais", tags=["Animais"])


# ==========================================================
# DEPENDÊNCIAS
# ==========================================================

SessionDep = Annotated[Session, Depends(get_session)]

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]


# ==========================================================
# SERVICE ANIMAL
# ==========================================================


def get_service(
    session: SessionDep,
    usuario_logado: UsuarioLogadoDep,
):
    repository = AnimalRepository(session)

    return AnimalServiceImpl(repository, usuario_logado)


AnimalServiceDep = Annotated[
    AnimalServiceImpl,
    Depends(get_service),
]


# ==========================================================
# SERVICE ATENDIMENTO
# ==========================================================


def get_atendimento_service(
    session: SessionDep,
    usuario_logado: UsuarioLogadoDep,
):
    repository = AtendimentoRepository(session)

    return AtendimentoServiceImpl(repository, usuario_logado)


AtendimentoServiceDep = Annotated[
    AtendimentoServiceImpl,
    Depends(get_atendimento_service),
]


# ==========================================================
# CRIAR
# ==========================================================


@router.post("/", response_model=AnimalResponse, status_code=201)
def criar(
    animal: AnimalCreate,
    service: AnimalServiceDep,
):
    return service.criar(animal)


# ==========================================================
# LISTAR
# ==========================================================


@router.get("/", response_model=list[AnimalResponse])
def listar(
    service: AnimalServiceDep,
    pagina: int = 1,
    limite: int = 10,
    nome: str | None = None,
    ordem: str = "asc",
):
    return service.listar(
        pagina=pagina,
        limite=limite,
        nome=nome,
        ordem=ordem,
    )


# ==========================================================
# BUSCAR POR ID
# ==========================================================


@router.get("/{id}", response_model=AnimalResponse)
def buscar(
    id: int,
    service: AnimalServiceDep,
):
    return service.buscar_por_id(id)


# ==========================================================
# ATUALIZAR
# ==========================================================


@router.put("/{id}", response_model=AnimalResponse)
def atualizar(
    id: int,
    animal: AnimalUpdate,
    service: AnimalServiceDep,
):
    return service.atualizar(id, animal)


# ==========================================================
# DELETAR
# ==========================================================


@router.delete("/{id}")
def deletar(
    id: int,
    service: AnimalServiceDep,
):
    return service.deletar(id)


# ==========================================================
# HISTÓRICO
# ==========================================================


@router.get("/{id}/historico", response_model=AnimalHistoricoResponse)
def historico(
    id: int,
    service_atendimento: AtendimentoServiceDep,
):
    return service_atendimento.historico_completo(id)
