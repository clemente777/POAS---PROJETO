from datetime import datetime

from backend.repositories.token_repository import TokenRepository

class TokenService:


    def __init__(
        self,
        repository: TokenRepository
    ):
        self.repository = repository

    def revogar(
        self,
        token: str,
        expira_em: datetime
    ):
        token_existente = self.repository.buscar_por_token(
            token
        )

        if token_existente:
            return

        return self.repository.criar(
            token=token,
            expira_em=expira_em
        )

    def esta_revogado(
        self,
        token: str
    ):
        return self.repository.buscar_por_token(
            token
        )

