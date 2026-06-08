
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlmodel import Session

from backend.database.database import get_session
from backend.models.models import Usuarios
from backend.services.token_service import create_access_token, decode_token

router = APIRouter(prefix="/login", tags=["Login"])

senha_context = PasswordHash.recommended()
oauth_schema = OAuth2PasswordBearer(tokenUrl="/login")

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          session: SessionDep = None):

    usuario = session.query(Usuarios).filter(
        Usuarios.email == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if not senha_context.verify(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha inválida")

    access_token = create_access_token(
        data={"sub": usuario.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_usuario(
    token: Annotated[str, Depends(oauth_schema)],
    session: SessionDep
):
    payload = decode_token(token)
    email = payload.get("sub")

    usuario = session.query(Usuarios).filter(
        Usuarios.email == email
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário inválido")

    return usuario

UsuarioLogado = Annotated[Usuarios, Depends(get_usuario)]
