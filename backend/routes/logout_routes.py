from fastapi import APIRouter, Depends

from backend.auth.dependencies import UsuarioLogado
from backend.services.implementations.token_service_impl import TokenService
from backend.auth.dependencies import get_token_service


router = APIRouter(
    prefix="/logout",
    tags=["Logout"]
)



@router.post("/")
def logout(
    usuario: UsuarioLogado,
    token_service: TokenService = Depends(get_token_service)
):

    token_service.revogar_token()

    return {
        "message":
        "Logout realizado com sucesso"
    }