from fastapi import Depends, HTTPException

from backend.auth.dependencies import get_current_user
from backend.models.usuario_model import Usuarios



def exigir_perfil(
    *perfis_permitidos: str
):
    """
    Dependência responsável
    pelo controle de acesso por perfil.

    Perfis disponíveis:

    • Administrador
    • Veterinário
    • Cliente


    Exemplo:

    exigir_perfil(
        "Administrador"
    )

    permite apenas administrador.


    exigir_perfil(
        "Administrador",
        "Veterinário"
    )

    permite ambos.
    """


    def verificar(

        usuario: Usuarios = Depends(
            get_current_user
        )

    ):

        if usuario.perfil not in perfis_permitidos:

            raise HTTPException(

                status_code=403,

                detail=(
                    "Usuário sem permissão "
                    "para acessar este recurso."
                )

            )


        return usuario


    return verificar