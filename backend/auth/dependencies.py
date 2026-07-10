from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from backend.auth.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Essa é a principal função da autenticação.
# Ela recebe um parâmetro chamado token.
# Você não precisa passar esse token manualmente.
# O FastAPI faz isso automaticamente.
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Aqui acontece toda a validação.
        # Ele verifica:
        # assinatura, SECRET_KEY algoritmo e expiração
        payload = decode_token(token)

        # você pode retornar user_id ou email
        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )
    