from pwdlib import PasswordHash

pwd_context = PasswordHash()

# Essa função recebe uma senha digitada pelo usuário e Ela transforma essa senha em um hash criptografado.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Essa função é usada no login.
# Ela recebe dois valores:
# senha digitada pelo usuário
# hash armazenado no banco
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)