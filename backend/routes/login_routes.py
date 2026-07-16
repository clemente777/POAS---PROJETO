from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.auth.token import create_access_token
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl


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

    return UsuarioServiceImpl(session)



@router.post("/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioServiceImpl = Depends(get_usuario_service)
):

    usuario = service.buscar_por_email(
        form_data.username
    )


    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )


    senha_valida = senha_context.verify(
        form_data.password,
        usuario.senha_hash
    )


    if not senha_valida:

        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )


    token = create_access_token(
        {
            "sub": usuario.email
        }
    )


    return {

        "access_token": token,

        "token_type": "bearer"
    }