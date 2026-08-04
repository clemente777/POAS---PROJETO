from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session

from backend.schemas.cadastro_schema import CadastroCreate

from backend.services.implementations.cadastro_service_impl import (
    CadastroServiceImpl
)



router = APIRouter(
    prefix="/cadastro",
    tags=["Cadastro"]
)



SessionDep = Annotated[
    Session,
    Depends(get_session)
]



@router.post("/")
def cadastrar(
    dados: CadastroCreate,
    session: SessionDep
):


    service = CadastroServiceImpl(
        session
    )


    usuario, cliente = service.cadastrar(
        dados
    )



    return {

        "message":
        "Cadastro realizado com sucesso.",


        "usuario": {

            "id": usuario.id,

            "email": usuario.email

        },


        "cliente": {

            "id": cliente.id,

            "nome": cliente.nome

        }

    }