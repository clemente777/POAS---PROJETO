from pwdlib import PasswordHash


senha_context = PasswordHash.recommended()


# Cria o hash da senha
def hash_password(password: str) -> str:
    return senha_context.hash(password)



# Verifica a senha digitada contra o hash salvo
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return senha_context.verify(
        plain_password,
        hashed_password
    )