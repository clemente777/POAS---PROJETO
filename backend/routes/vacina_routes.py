from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.auth.permissions import exigir_perfil

from backend.schemas.vacina_schema import (
    VacinaCreate,
    VacinaUpdate,
    VacinaResponse
)

from backend.repositories.vacina_repository import (
    VacinaRepository
)

from backend.services.implementations.vacina_service_impl import (
    VacinaServiceImpl
)


router = APIRouter(
    prefix="/vacinas",
    tags=["Vacinas"]
)


# ==================================================
# DEPENDÊNCIA DO SERVICE
# ==================================================

def get_service(
    session: Session = Depends(get_session)
):

    repository = VacinaRepository(
        session
    )

    return VacinaServiceImpl(
        repository=repository
    )


# ==================================================
# LISTAR VACINAS
# Administrador e Veterinário
# ==================================================

@router.get(
    "/",
    response_model=list[VacinaResponse],
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador",
                "Veterinário"
            )
        )
    ]
)
def listar(
    service: VacinaServiceImpl = Depends(
        get_service
    )
):

    return service.listar()


# ==================================================
# BUSCAR VACINA POR ID
# Administrador e Veterinário
# ==================================================

@router.get(
    "/{vacina_id}",
    response_model=VacinaResponse,
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador",
                "Veterinário"
            )
        )
    ]
)
def buscar_por_id(
    vacina_id: int,
    service: VacinaServiceImpl = Depends(
        get_service
    )
):

    return service.buscar_por_id(
        vacina_id
    )


# ==================================================
# BUSCAR VACINA POR NOME
# Administrador e Veterinário
# ==================================================

@router.get(
    "/buscar/{nome}",
    response_model=list[VacinaResponse],
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador",
                "Veterinário"
            )
        )
    ]
)
def buscar_por_nome(
    nome: str,
    service: VacinaServiceImpl = Depends(
        get_service
    )
):

    return service.buscar_por_nome(
        nome
    )


# ==================================================
# CADASTRAR VACINA
# Apenas Administrador
# ==================================================

@router.post(
    "/",
    response_model=VacinaResponse,
    status_code=201,
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador"
            )
        )
    ]
)
def cadastrar(
    dados: VacinaCreate,
    service: VacinaServiceImpl = Depends(
        get_service
    )
):

    return service.cadastrar(
        dados
    )


# ==================================================
# ATUALIZAR VACINA
# Apenas Administrador
# ==================================================

@router.put(
    "/{vacina_id}",
    response_model=VacinaResponse,
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador"
            )
        )
    ]
)
def atualizar(
    vacina_id: int,
    dados: VacinaUpdate,
    service: VacinaServiceImpl = Depends(
        get_service
    )
):

    return service.atualizar(
        vacina_id,
        dados
    )


# ==================================================
# DELETAR VACINA
# Apenas Administrador
# ==================================================

@router.delete(
    "/{vacina_id}",
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador"
            )
        )
    ]
)
def deletar(
    vacina_id: int,
    service: VacinaServiceImpl = Depends(
        get_service
    )
):

    return service.deletar(
        vacina_id
    )

