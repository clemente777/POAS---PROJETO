# routes/usuario_routes.py
from fastapi import APIRouter, HTTPException
from backend.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from backend.services.usuario_service import (
    criar_usuario,
    listar_usuarios,
    buscar_usuario,
    atualizar_usuario,
    deletar_usuario
)

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/")
def create_usuario(usuario: UsuarioCreate):
    result = criar_usuario(usuario)

    if result is None:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    return result


@router.get("/")
def get_usuarios():
    return listar_usuarios()


@router.get("/{usuario_id}")
def get_usuario(usuario_id: int):
    result = buscar_usuario(usuario_id)

    if not result:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return result


@router.put("/{usuario_id}")
def update_usuario(usuario_id: int, usuario: UsuarioUpdate):
    result = atualizar_usuario(usuario_id, usuario)

    if result is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if result == "email_duplicado":
        raise HTTPException(status_code=400, detail="Email já está em uso")

    return result


@router.delete("/{usuario_id}")
def delete_usuario(usuario_id: int):
    result = deletar_usuario(usuario_id)

    if not result:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"mensagem": "Usuário removido com sucesso"}