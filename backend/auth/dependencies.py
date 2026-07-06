from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from backend.auth.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)

        # você pode retornar user_id ou email
        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )