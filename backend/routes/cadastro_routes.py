from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_session
from backend.repositories.cadastro_repository import CadastroRepository
from backend.schemas.cadastro_schema import CadastroCreate
from backend.services.implementations.cadastro_service_impl import CadastroServiceImpl

router = APIRouter(prefix="/cadastro", tags=["Cadastro"])


# ==========================================================
# DEPENDÊNCIA DA SESSÃO
# ==========================================================

SessionDep = Annotated[Session, Depends(get_session)]


# ==========================================================
# DEPENDÊNCIA DO SERVICE
# ==========================================================


def get_service(session: SessionDep):
    repository = CadastroRepository(session)

    return CadastroServiceImpl(repository)


CadastroServiceDep = Annotated[
    CadastroServiceImpl,
    Depends(get_service),
]


# ==========================================================
# CADASTRO PÚBLICO
# ==========================================================


@router.post("/")
def cadastrar(
    dados: CadastroCreate,
    service: CadastroServiceDep,
):
    usuario, cliente = service.cadastrar(dados)

    return {
        "message": "Cadastro realizado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
        },
        "cliente": {
            "id": cliente.id,
            "nome": cliente.nome,
        },
    }
