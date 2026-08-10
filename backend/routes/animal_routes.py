from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from backend.database.database import get_session


from backend.schemas.animal_schema import (
    AnimalCreate,
    AnimalUpdate,
    AnimalResponse
)


from backend.schemas.historico_schema import (
    AnimalHistoricoResponse
)


from backend.services.implementations.animal_service_impl import (
    AnimalServiceImpl
)


from backend.services.implementations.atendimento_service_impl import (
    AtendimentoServiceImpl
)


from backend.models.usuario_model import Usuarios


from backend.auth.permissions import exigir_perfil
from backend.auth.dependencies import get_current_user



router = APIRouter(
    prefix="/animais",
    tags=["Animais"]
)



# ==========================================================
# SERVICE ANIMAL
# ==========================================================


def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(get_current_user)
):

    return AnimalServiceImpl(
        session,
        usuario_logado
    )



# ==========================================================
# SERVICE ATENDIMENTO
# ==========================================================


def get_atendimento_service(
    session: Session = Depends(get_session)
):

    return AtendimentoServiceImpl(
        session
    )



# ==========================================================
# CRIAR
# ==========================================================


@router.post(
    "/",
    response_model=AnimalResponse,
    status_code=201
)
def criar(

    animal: AnimalCreate,

    service: AnimalServiceImpl = Depends(
        get_service
    )

):

    return service.criar(
        animal
    )



# ==========================================================
# LISTAR
# ==========================================================


@router.get(
    "/",
    response_model=list[AnimalResponse]
)
def listar(

    pagina: int = 1,

    limite: int = 10,

    nome: str | None = None,

    ordem: str = "asc",


    service: AnimalServiceImpl = Depends(
        get_service
    )

):


    return service.listar(

        pagina=pagina,

        limite=limite,

        nome=nome,

        ordem=ordem

    )



# ==========================================================
# BUSCAR POR ID
# ==========================================================


@router.get(
    "/{id}",
    response_model=AnimalResponse
)
def buscar(

    id: int,


    service: AnimalServiceImpl = Depends(
        get_service
    )

):

    return service.buscar_por_id(
        id
    )



# ==========================================================
# ATUALIZAR
# ==========================================================


@router.put(
    "/{id}",
    response_model=AnimalResponse
)
def atualizar(

    id: int,

    animal: AnimalUpdate,


    service: AnimalServiceImpl = Depends(
        get_service
    )

):


    return service.atualizar(

        id,

        animal

    )



# ==========================================================
# DELETAR
# ==========================================================


@router.delete(
    "/{id}"
)
def deletar(

    id: int,


    service: AnimalServiceImpl = Depends(
        get_service
    )

):


    return service.deletar(
        id
    )



# ==========================================================
# HISTÓRICO
# ==========================================================


@router.get(
    "/{id}/historico",
    response_model=AnimalHistoricoResponse
)
def historico(

    id: int,


    service_animal: AnimalServiceImpl = Depends(
        get_service
    ),


    service_atendimento: AtendimentoServiceImpl = Depends(
        get_atendimento_service
    )

):


    service_animal.buscar_por_id(
        id
    )



    resultado = service_atendimento.historico_completo(
        id
    )



    if resultado is None:

        raise HTTPException(

            status_code=404,

            detail="Histórico não encontrado."

        )



    return resultado
