from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from backend.database.database import get_session


from backend.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse
)


from backend.services.implementations.produto_service_impl import (
    ProdutoServiceImpl
)


from backend.models.usuario_model import Usuarios


from backend.auth.dependencies import get_current_user



router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)



# ==================================================
# DEPENDÊNCIA SERVICE
# ==================================================


def get_service(
    session: Session = Depends(get_session),
    usuario_logado: Usuarios = Depends(get_current_user)
):

    return ProdutoServiceImpl(
        session,
        usuario_logado
    )



# ==================================================
# CRIAR PRODUTO
# Apenas Administrador
# ==================================================


@router.post(
    "/",
    response_model=ProdutoResponse,
    status_code=201
)
def criar(

    produto: ProdutoCreate,


    service: ProdutoServiceImpl = Depends(
        get_service
    )

):


    return service.criar(
        produto
    )



# ==================================================
# LISTAR PRODUTOS
# Usuários autenticados
# ==================================================


@router.get(
    "/",
    response_model=list[ProdutoResponse]
)
def listar(

    skip: int = 0,

    limit: int = 10,

    nome: str | None = None,

    descricao: str | None = None,

    preco_min: float | None = None,

    preco_max: float | None = None,

    estoque_min: int | None = None,

    estoque_max: int | None = None,

    em_estoque: bool | None = None,

    sort_by: str = "nome",

    order: str = "asc",


    usuario_logado: Usuarios = Depends(
        get_current_user
    ),


    service: ProdutoServiceImpl = Depends(
        get_service
    )

):


    return service.listar(

        skip=skip,

        limit=limit,

        nome=nome,

        descricao=descricao,

        preco_min=preco_min,

        preco_max=preco_max,

        estoque_min=estoque_min,

        estoque_max=estoque_max,

        em_estoque=em_estoque,

        sort_by=sort_by,

        order=order

    )



# ==================================================
# BUSCAR PRODUTO POR ID
# Usuários autenticados
# ==================================================


@router.get(
    "/{id}",
    response_model=ProdutoResponse
)
def buscar(

    id: int,


    service: ProdutoServiceImpl = Depends(
        get_service
    )

):


    return service.buscar_por_id(
        id
    )



# ==================================================
# ATUALIZAR PRODUTO
# Apenas Administrador
# ==================================================


@router.put(
    "/{id}",
    response_model=ProdutoResponse
)
def atualizar(

    id: int,


    produto: ProdutoUpdate,


    service: ProdutoServiceImpl = Depends(
        get_service
    )

):


    return service.atualizar(

        id,

        produto

    )



# ==================================================
# DELETAR PRODUTO
# Apenas Administrador
# ==================================================


@router.delete(
    "/{id}"
)
def deletar(

    id: int,


    service: ProdutoServiceImpl = Depends(
        get_service
    )

):


    return {

        "success":
        service.deletar(id)

    }