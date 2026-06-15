from backend.models.models import Atendimentos
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado
from backend.services.implementations.atendimento_service_impl import AtendimentoServiceImpl

from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/atendimentos",
    tags=["atendimentos"]
)

@router.get("/", response_model=list[Atendimentos])
def get_atendimentos(session: SessionDep,
                     usuario: UsuarioLogado):
    return AtendimentoServiceImpl(session).listar_atendimentos()

@router.get("/{id}", response_model=Atendimentos)
def get_atendimento_by_id(id: int,
                          session: SessionDep,
                          usuario: UsuarioLogado):
    return AtendimentoServiceImpl(session).buscar_atendimento_por_id(id)

@router.post("/", response_model=Atendimentos)
def create_atendimento(atendimento: Atendimentos,
                       session: SessionDep):
    return AtendimentoServiceImpl(session).criar_atendimento(atendimento)

@router.put("/{id}")
def update_atendimento(id: int,
                       atendimento: Atendimentos,
                       session: SessionDep,
                       usuario: UsuarioLogado):

    service = AtendimentoServiceImpl(session)

    if not service.atualizar_atendimento(id, atendimento):
        return {"erro":"Atendimento não encontrado"}

    return {"mensagem":"Atendimento atualizado"}

@router.delete("/{id}")
def delete_atendimento(id: int,
                       session: SessionDep,
                       usuario: UsuarioLogado):

    service = AtendimentoServiceImpl(session)

    if not service.deletar_atendimento(id):
        return {"erro":"Atendimento não encontrado"}

    return {"mensagem":"Atendimento removido"}