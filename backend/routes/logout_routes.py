from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.auth.token import decode_token
from backend.database.database import get_session
from backend.repositories.token_repository import TokenRepository
from backend.services.implementations.token_service_impl import TokenService

router = APIRouter(prefix="/logout", tags=["Logout"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_token_service(session: SessionDep):
    repository = TokenRepository(session)

    return TokenService(repository=repository)


TokenServiceDep = Annotated[
    TokenService,
    Depends(get_token_service),
]


@router.post("/")
def logout(
    token: TokenDep,
    token_service: TokenServiceDep,
):
    # ==========================================
    # DECODIFICAR TOKEN
    # ==========================================

    try:
        payload = decode_token(token)

    except Exception as erro:
        raise HTTPException(
            status_code=401,
            detail="Token inválido.",
        ) from erro

    # ==========================================
    # VALIDAR EXPIRAÇÃO
    # ==========================================

    if "exp" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido.")

    # ==========================================
    # CONVERTER EXPIRAÇÃO
    # ==========================================

    expira_em = datetime.fromtimestamp(payload["exp"], tz=UTC)

    # ==========================================
    # REVOGAR TOKEN
    # ==========================================

    token_service.revogar(token=token, expira_em=expira_em)

    # ==========================================
    # RETORNAR RESPOSTA
    # ==========================================

    return {"message": "Logout realizado com sucesso."}
