from backend.models.models import Produtos
from backend.database.database import get_session
from backend.routes.login_router import UsuarioLogado
from backend.services.implementations.produto_service_impl import ProdutoServiceImpl

from typing import Annotated
from fastapi import Depends, APIRouter
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)

@router.get("/", response_model=list[Produtos])
def get_produtos(session: SessionDep,
                 usuario: UsuarioLogado):
    return ProdutoServiceImpl(session).listar_produtos()

@router.get("/{id}", response_model=Produtos)
def get_produto_by_id(id: int,
                      session: SessionDep,
                      usuario: UsuarioLogado):
    return ProdutoServiceImpl(session).buscar_produto_por_id(id)

@router.post("/", response_model=Produtos)
def create_produto(produto: Produtos,
                   session: SessionDep):
    return ProdutoServiceImpl(session).criar_produto(produto)

@router.put("/{id}")
def update_produto(id: int,
                   produto: Produtos,
                   session: SessionDep,
                   usuario: UsuarioLogado):

    service = ProdutoServiceImpl(session)

    if not service.atualizar_produto(id, produto):
        return {"erro":"Produto não encontrado"}

    return {"mensagem":"Produto atualizado"}

@router.delete("/{id}")
def delete_produto(id: int,
                   session: SessionDep,
                   usuario: UsuarioLogado):

    service = ProdutoServiceImpl(session)

    if not service.deletar_produto(id):
        return {"erro":"Produto não encontrado"}

    return {"mensagem":"Produto removido"}