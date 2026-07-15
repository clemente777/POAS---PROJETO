from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.auth.token import decode_token
from backend.database.database import get_session
from backend.services.implementations.token_service_impl import TokenService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

SessionDep = Annotated[Session, Depends(get_session)]


def get_token_service(session: SessionDep):
    return TokenService(session)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: TokenService = Depends(get_token_service),
):
    try:

        if token_service.esta_revogado(token):
            raise HTTPException(
                status_code=401,
                detail="Token revogado"
            )

        payload = decode_token(token)

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )