
from backend.models.models import Usuarios
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado
from typing import Annotated    
from fastapi import Depends, APIRouter
from pwdlib import PasswordHash
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

senha_context = PasswordHash.recommended()

@router.get("/", response_model=list[Usuarios])
def get_usuarios(session: SessionDep, usuario: UsuarioLogado):
    return session.query(Usuarios).all()

@router.get("/{id}", response_model=Usuarios)
def get_usuario_by_id(id: int, session: SessionDep, usuario: UsuarioLogado):
    return session.query(Usuarios).get(id)

@router.post("/", response_model=Usuarios)
def create_usuario(usuario: Usuarios, session: SessionDep):
    usuario.senha_hash = senha_context.hash(usuario.senha_hash)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete("/{id}")
def delete_usuario(id: int, session: SessionDep, usuario_logado: UsuarioLogado):
    usuario = session.query(Usuarios).get(id)
    if not usuario:
        return {"erro":"Usuário não encontrado"}
    session.delete(usuario)
    session.commit()
    return {"mensagem":"Usuário removido"}

@router.put("/{id}")
def update_usuario(id: int, usuario: Usuarios,
                   session: SessionDep,
                   usuario_logado: UsuarioLogado):
    session.query(Usuarios).filter(
        Usuarios.id == id
    ).update(usuario.model_dump())
    session.commit()
    return {"mensagem":"Usuário atualizado"}
