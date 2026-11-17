from datetime import UTC, datetime

blacklist = {}


def adicionar_token(token: str):
    blacklist[token] = datetime.now(UTC)


def token_revogado(token: str) -> bool:
    return token in blacklist
