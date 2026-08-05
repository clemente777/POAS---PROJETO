from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from backend.database.database import get_session


from backend.auth.permissions import exigir_perfil


from backend.schemas.vacina_schema import (
    VacinaCreate,
    VacinaUpdate,
    VacinaResponse
)


from backend.services.implementations.vacina_service_impl import (
    VacinaServiceImpl
)



router = APIRouter(

    prefix="/vacinas",

    tags=["Vacinas"]

)



def get_service(

    session: Session = Depends(get_session)

):

    return VacinaServiceImpl(
        session
    )





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





@router.post(
    "/",
    response_model=VacinaResponse,
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