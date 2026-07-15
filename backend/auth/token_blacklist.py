from datetime import datetime, timezone

blacklist = {}


def adicionar_token(token: str):
    blacklist[token] = datetime.now(timezone.utc)


def token_revogado(token: str) -> bool:
    return token in blacklist