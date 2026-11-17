from typing import Annotated

from fastapi import Depends, HTTPException

from backend.auth.dependencies import get_current_user
from backend.models.usuario_model import Usuarios

UsuarioLogadoDep = Annotated[
    Usuarios,
    Depends(get_current_user),
]


def exigir_perfil(*perfis_permitidos: str):
    """
    Dependência responsável pelo controle
    de acesso por perfil.
    """

    def verificar(usuario: UsuarioLogadoDep):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=403,
                detail="Usuário sem permissão para acessar este recurso.",
            )

        return usuario

    return verificar
