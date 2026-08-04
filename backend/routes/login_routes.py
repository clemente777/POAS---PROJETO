from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session



from backend.database.database import get_session

from backend.auth.token import (
    create_access_token
)
from sqlalchemy import select
from backend.models.cliente_model import Clientes

from backend.services.implementations.usuario_service_impl import (
    UsuarioServiceImpl
)



router = APIRouter(
    prefix="/login",
    tags=["Login"]
)



senha_context = PasswordHash.recommended()



SessionDep = Annotated[
    Session,
    Depends(get_session)
]



def get_usuario_service(
    session: SessionDep
):

    return UsuarioServiceImpl(
        session
    )





@router.post("/")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    service: UsuarioServiceImpl = Depends(
        get_usuario_service
    )

):


    # ==========================================
    # BUSCAR USUÁRIO
    # ==========================================

    usuario = service.buscar_por_email(
        form_data.username
    )


    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado."
        )



    # ==========================================
    # VALIDAR SENHA
    # ==========================================

    senha_valida = senha_context.verify(

        form_data.password,

        usuario.senha_hash

    )
    if not senha_valida:

        raise HTTPException(
            status_code=401,
            detail="Senha inválida."
        )


# ==========================================
# BUSCAR CLIENTE SE FOR CLIENTE
# ==========================================

    if usuario.perfil == "Cliente":

        cliente = service.session.scalar(

            select(Clientes).where(

                Clientes.usuario_id == usuario.id

            )

        )

        if not cliente:

            raise HTTPException(
                status_code=404,
                detail="Este usuário não possui cadastro de cliente."
            )
    # ==========================================
    # CRIAR TOKEN
    # ==========================================

    token = create_access_token(

        {

            "sub":
            usuario.email,


            "perfil":
            usuario.perfil,


            "usuario_id":
            usuario.id

        }

    )



    return {

        "access_token": token,

        "token_type": "bearer",

        "usuario": {

            "id": usuario.id,
            
            "nome": usuario.nome,

            "email": usuario.email,

            "perfil": usuario.perfil

        }

    }