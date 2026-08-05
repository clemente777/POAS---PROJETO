from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.auth.dependencies import (
    get_current_user
)

from backend.auth.permissions import (
    exigir_perfil
)

from backend.models.usuario_model import Usuarios

from backend.schemas.aplicacao_vacina_schema import (
    AplicacaoVacinaCreate,
    AplicacaoVacinaUpdate,
    AplicacaoVacinaResponse
)

from backend.services.implementations.aplicacao_vacina_service_impl import (
    AplicacaoVacinaServiceImpl
)



router = APIRouter(

    prefix="/aplicacoes-vacina",

    tags=["Aplicações de Vacina"]

)



def get_service(
    session: Session = Depends(get_session)
):

    return AplicacaoVacinaServiceImpl(session)




# ======================================
# LISTAR TODAS AS APLICAÇÕES
# Administrador e Veterinário
# ======================================

@router.get(
    "/",
    response_model=list[AplicacaoVacinaResponse],
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
    service: AplicacaoVacinaServiceImpl = Depends(get_service)
):

    return service.listar()




# ======================================
# BUSCAR POR ID
# Administrador e Veterinário
# ======================================

@router.get(
    "/{aplicacao_id}",
    response_model=AplicacaoVacinaResponse,
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
    aplicacao_id: int,
    service: AplicacaoVacinaServiceImpl = Depends(get_service)
):

    return service.buscar_por_id(
        aplicacao_id
    )




# ======================================
# LISTAR VACINAS DE UM ANIMAL
# Administrador e Veterinário
# ======================================

@router.get(
    "/animal/{animal_id}",
    response_model=list[AplicacaoVacinaResponse],
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador",
                "Veterinário"
            )
        )
    ]
)
def listar_por_animal(
    animal_id: int,
    service: AplicacaoVacinaServiceImpl = Depends(get_service)
):

    return service.listar_por_animal(
        animal_id
    )




# ======================================
# APLICAR VACINA
# Somente Veterinário
# ======================================

@router.post(
    "/",
    response_model=AplicacaoVacinaResponse,
    dependencies=[
        Depends(
            exigir_perfil(
                "Veterinário"
            )
        )
    ]
)
def aplicar_vacina(
    dados: AplicacaoVacinaCreate,

    usuario: Usuarios = Depends(
        get_current_user
    ),

    service: AplicacaoVacinaServiceImpl = Depends(
        get_service
    )

):

    return service.aplicar_vacina(

        dados,

        usuario.id

    )




# ======================================
# ATUALIZAR APLICAÇÃO
# Veterinário e Administrador
# ======================================

@router.put(
    "/{aplicacao_id}",
    response_model=AplicacaoVacinaResponse,
    dependencies=[
        Depends(
            exigir_perfil(
                "Veterinário",
                "Administrador"
            )
        )
    ]
)
def atualizar(
    aplicacao_id: int,

    dados: AplicacaoVacinaUpdate,

    service: AplicacaoVacinaServiceImpl = Depends(
        get_service
    )

):

    return service.atualizar(

        aplicacao_id,

        dados

    )




# ======================================
# DELETAR APLICAÇÃO
# Somente Administrador
# ======================================

@router.delete(
    "/{aplicacao_id}",
    dependencies=[
        Depends(
            exigir_perfil(
                "Administrador"
            )
        )
    ]
)
def deletar(
    aplicacao_id: int,

    service: AplicacaoVacinaServiceImpl = Depends(
        get_service
    )

):

    return service.deletar(

        aplicacao_id

    )