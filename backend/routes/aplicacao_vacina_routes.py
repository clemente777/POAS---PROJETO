from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.auth.permissions import exigir_perfil
from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.repositories.aplicacao_vacina_repository import AplicacaoVacinaRepository
from backend.schemas.aplicacao_vacina_schema import (
    AplicacaoVacinaClienteResponse,
    AplicacaoVacinaCreate,
    AplicacaoVacinaResponse,
    AplicacaoVacinaUpdate,
)
from backend.services.implementations.aplicacao_vacina_service_impl import (
    AplicacaoVacinaServiceImpl,
)

router = APIRouter(prefix="/aplicacoes-vacina", tags=["Aplicações de Vacina"])


# ==========================================================
# DEPENDÊNCIAS
# ==========================================================

SessionDep = Annotated[Session, Depends(get_session)]

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]

VeterinarioAdminDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Administrador", "Veterinário")),
]

ClienteDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Cliente")),
]

VeterinarioDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Veterinário")),
]

VeterinarioAdminAtualizacaoDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Veterinário", "Administrador")),
]

AdministradorDep = Annotated[
    Usuarios,
    Depends(exigir_perfil("Administrador")),
]


# ==========================================================
# DEPENDÊNCIA DO SERVICE
# ==========================================================


def get_service(
    session: SessionDep,
    usuario_logado: UsuarioLogadoDep,
):
    repository = AplicacaoVacinaRepository(session)

    return AplicacaoVacinaServiceImpl(repository, usuario_logado)


AplicacaoVacinaServiceDep = Annotated[
    AplicacaoVacinaServiceImpl,
    Depends(get_service),
]


# ==========================================================
# LISTAR TODAS AS APLICAÇÕES
# Administrador e Veterinário
# ==========================================================


@router.get("/", response_model=list[AplicacaoVacinaResponse])
def listar(
    usuario_logado: VeterinarioAdminDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.listar()


# ==========================================================
# BUSCAR POR ID
# Administrador e Veterinário
# ==========================================================


@router.get("/{aplicacao_id}", response_model=AplicacaoVacinaResponse)
def buscar_por_id(
    aplicacao_id: int,
    usuario_logado: VeterinarioAdminDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.buscar_por_id(aplicacao_id)


# ==========================================================
# LISTAR VACINAS DE UM ANIMAL
# Administrador e Veterinário
# ==========================================================


@router.get(
    "/animal/{animal_id}",
    response_model=list[AplicacaoVacinaResponse],
)
def listar_por_animal(
    animal_id: int,
    usuario_logado: VeterinarioAdminDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.listar_por_animal(animal_id)


# ==========================================================
# CARTEIRA DE VACINAÇÃO DE UM ANIMAL
# Somente Cliente (e só dos próprios animais)
# ==========================================================


@router.get(
    "/carteira/{animal_id}",
    response_model=list[AplicacaoVacinaClienteResponse],
)
def carteira_do_animal(
    animal_id: int,
    usuario_logado: ClienteDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.listar_carteira_do_animal(animal_id)


# ==========================================================
# APLICAR VACINA
# Somente Veterinário
# ==========================================================


@router.post(
    "/",
    response_model=AplicacaoVacinaResponse,
    status_code=201,
)
def aplicar_vacina(
    dados: AplicacaoVacinaCreate,
    usuario: VeterinarioDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.aplicar_vacina(dados, usuario.id)


# ==========================================================
# ATUALIZAR APLICAÇÃO
# Veterinário e Administrador
# ==========================================================


@router.put(
    "/{aplicacao_id}",
    response_model=AplicacaoVacinaResponse,
)
def atualizar(
    aplicacao_id: int,
    dados: AplicacaoVacinaUpdate,
    usuario_logado: VeterinarioAdminAtualizacaoDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.atualizar(aplicacao_id, dados)


# ==========================================================
# DELETAR APLICAÇÃO
# Somente Administrador
# ==========================================================


@router.delete("/{aplicacao_id}")
def deletar(
    aplicacao_id: int,
    usuario_logado: AdministradorDep,
    service: AplicacaoVacinaServiceDep,
):
    return service.deletar(aplicacao_id)
