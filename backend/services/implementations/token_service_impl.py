from datetime import datetime

from sqlalchemy.orm import Session

from backend.models.token_revogado_model import TokenRevogado


class TokenService:

    def __init__(self, session: Session):
        self.session = session

    def revogar(self, token: str, expira_em: datetime):
        token_existente = (
            self.session.query(TokenRevogado)
            .filter(TokenRevogado.token == token)
            .first()
        )

        if token_existente:
            return
    
        token_revogado = TokenRevogado(
            token=token,
            expira_em=expira_em
        )

        self.session.add(token_revogado)
        self.session.commit()

    def esta_revogado(self, token: str):

        return (
            self.session.query(TokenRevogado)
            .filter(TokenRevogado.token == token)
            .first()
        )