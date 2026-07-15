from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.models.usuario_model import Usuarios
from backend.auth.dependencies import get_current_user
from backend.auth.token import create_access_token, decode_token
from backend.services.implementations.usuario_service_impl import UsuarioServiceImpl
from backend.services.implementations.token_service_impl import TokenService

router = APIRouter(prefix="/login",tags=["Login"])

senha_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

SessionDep = Annotated[Session, Depends(get_session)]


def get_service(session: SessionDep):
    return UsuarioServiceImpl(session)


def get_token_service(session: SessionDep):
    return TokenService(session)


@router.post("/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioServiceImpl = Depends(get_service),
):

    usuario = service.buscar_por_email(form_data.username)

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    if not senha_context.verify(
        form_data.password,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    token = create_access_token(
        data={
            "sub": usuario.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: TokenService = Depends(get_token_service),
):

    payload = decode_token(token)

    expira_em = datetime.fromtimestamp(
        payload["exp"],
        tz=timezone.utc
    )

    token_service.revogar(
        token,
        expira_em
    )

    return {
        "message": "Logout realizado com sucesso."
    }


def get_usuario(
    payload: Annotated[dict, Depends(get_current_user)],
    service: UsuarioServiceImpl = Depends(get_service),
):

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


UsuarioLogado = Annotated[
    Usuarios,
    Depends(get_usuario)
]