from datetime import datetime, timedelta, timezone

import jwt

from fastapi import HTTPException

from jwt import (
    ExpiredSignatureError,
    InvalidTokenError
)



SECRET_KEY = "sua-chave-super-secreta"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60





def create_access_token(
    data: dict
):

    """
    Cria JWT autenticado.

    Informações armazenadas:

    - email
    - perfil
    - expiração
    """


    to_encode = data.copy()


    expire = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


    to_encode.update(
        {
            "exp": expire
        }
    )


    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )





def decode_token(
    token: str
):

    """
    Valida e decodifica JWT.
    """


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )


        return payload



    except ExpiredSignatureError:


        raise HTTPException(
            status_code=401,
            detail="Token expirado."
        )



    except InvalidTokenError:


        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )