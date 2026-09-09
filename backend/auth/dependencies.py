from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.auth.token import decode_token
from backend.database.database import get_session

from backend.models.usuario_model import Usuarios

from backend.repositories.token_repository import (
    TokenRepository
)

from backend.repositories.usuario_repository import (
    UsuarioRepository
)

from backend.repositories.cliente_repository import (
    ClienteRepository
)

from backend.services.implementations.token_service_impl import (
    TokenService
)

from backend.services.implementations.usuario_service_impl import (
    UsuarioServiceImpl
)


# ==========================================================
# AUTENTICAÇÃO JWT
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/"
)


# ==========================================================
# DEPENDÊNCIA DA SESSÃO
# ==========================================================

SessionDep = Annotated[
    Session,
    Depends(get_session)
]


# ==========================================================
# TOKEN SERVICE
# ==========================================================

def get_token_service(
    session: SessionDep
):

    repository = TokenRepository(
        session
    )

    return TokenService(
        repository=repository
    )


# ==========================================================
# USUÁRIO SERVICE
# ==========================================================

def get_usuario_service(
    session: SessionDep
):

    usuario_repository = UsuarioRepository(
        session
    )

    cliente_repository = ClienteRepository(
        session
    )

    return UsuarioServiceImpl(
        repository=usuario_repository,
        cliente_repository=cliente_repository
    )


# ==========================================================
# USUÁRIO ATUAL
# ==========================================================

def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme)
    ],

    token_service: TokenService = Depends(
        get_token_service
    ),

    usuario_service: UsuarioServiceImpl = Depends(
        get_usuario_service
    )
):

    """
    Recupera o usuário autenticado.

    Fluxo:

    1 - Verifica se o token foi revogado.
    2 - Decodifica o JWT.
    3 - Recupera o email do token.
    4 - Busca o usuário no banco.
    5 - Verifica se o usuário existe.
    6 - Retorna o usuário autenticado.
    """

    # ======================================================
    # VERIFICAR TOKEN REVOGADO
    # ======================================================

    if token_service.esta_revogado(
        token
    ):

        raise HTTPException(
            status_code=401,
            detail="Token revogado."
        )

    # ======================================================
    # DECODIFICAR TOKEN
    # ======================================================

    try:

        payload = decode_token(
            token
        )

    except HTTPException:

        raise

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

    # ======================================================
    # RECUPERAR EMAIL DO TOKEN
    # ======================================================

    email = payload.get(
        "sub"
    )

    if not email:

        raise HTTPException(
            status_code=401,
            detail="Token sem usuário."
        )

    # ======================================================
    # BUSCAR USUÁRIO
    # ======================================================

    usuario = usuario_service.buscar_por_email(
        email
    )

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado."
        )

    # ======================================================
    # RETORNAR USUÁRIO LOGADO
    # ======================================================

    return usuario


# ==========================================================
# USUÁRIO LOGADO DISPONÍVEL NAS ROTAS
# ==========================================================

UsuarioLogado = Annotated[
    Usuarios,
    Depends(get_current_user)
]


# ==========================================================
# EXIGIR PERFIL
# ==========================================================

def exigir_perfil(
    *perfis_permitidos: str
):

    """
    Dependência responsável pelo controle
    de acesso por perfil.

    Perfis disponíveis:

    • Administrador
    • Veterinário
    • Cliente

    Exemplo:

        exigir_perfil("Administrador")

    permite apenas Administrador.

    Exemplo:

        exigir_perfil(
            "Administrador",
            "Veterinário"
        )

    permite Administrador e Veterinário.
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