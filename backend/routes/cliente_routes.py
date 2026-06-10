from backend.models.models import Clientes
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado
from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/clientes",tags=["clientes"])

@router.get("/", response_model=list[Clientes])

def get_clientes(session: SessionDep,usuario: UsuarioLogado):
    return session.query(Clientes).all()

@router.get("/{id}", response_model=Clientes)
def get_cliente_by_id(id: int, session: SessionDep,usuario: UsuarioLogado):
    return session.query(Clientes).get(id)

@router.post("/", response_model=Clientes)
def create_cliente(cliente: Clientes, session: SessionDep):
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@router.delete("/{id}")
def delete_cliente(id: int, session: SessionDep, usuario_logado: UsuarioLogado):
    cliente = session.query(Clientes).get(id)
    if not cliente:
        return {"erro": "Cliente não encontrado"}
    session.delete(cliente)
    session.commit()
    return {"mensagem": "Cliente removido"}

@router.put("/{id}")
def update_cliente(id: int, cliente: Clientes, session: SessionDep, usuario_logado: UsuarioLogado):
    session.query(Clientes).filter(Clientes.id == id).update(cliente.model_dump())
    session.commit()
    return {"mensagem": "Cliente atualizado"}