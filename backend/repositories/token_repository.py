from datetime import datetime

from sqlalchemy.orm import Session

from backend.models.token_revogado_model import TokenRevogado

class TokenRepository:


    def __init__(
        self,
        session: Session
    ):
        self.session = session

    def buscar_por_token(
        self,
        token: str
    ):
        return (
            self.session.query(TokenRevogado)
            .filter(
                TokenRevogado.token == token
            )
            .first()
        )

    def criar(
        self,
        token: str,
        expira_em: datetime
    ):
        token_revogado = TokenRevogado(
            token=token,
            expira_em=expira_em
        )

        self.session.add(token_revogado)
        self.session.commit()

        return token_revogado

