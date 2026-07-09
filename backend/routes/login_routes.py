from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.auth.token import (
    create_access_token,
    decode_token,
)
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl

router = APIRouter(prefix="/login",tags=["Login"])

senha_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

SessionDep = Annotated[Session, Depends(get_session)]


def get_service(session: SessionDep):
    return UsuarioServiceImpl(session)


@router.post("/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioServiceImpl = Depends(get_service),
):

    usuario = service.buscar_por_email(form_data.username)

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado",
        )

    if not senha_context.verify(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="Senha inválida",
        )

    token = create_access_token(
        data={"sub": usuario.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def get_usuario(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UsuarioServiceImpl = Depends(get_service),
):

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )

    usuario = service.buscar_por_email(email)

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado",
        )

    return usuario


UsuarioLogado = Annotated[Usuarios, Depends(get_usuario)]