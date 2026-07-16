from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.auth.token import decode_token
from backend.services.implementations.token_service_impl import TokenService


router = APIRouter(
    prefix="/logout",
    tags=["Logout"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


SessionDep = Annotated[
    Session,
    Depends(get_session)
]


def get_token_service(session: SessionDep):
    return TokenService(session)


@router.post("/")
def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: TokenService = Depends(get_token_service),
):
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

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