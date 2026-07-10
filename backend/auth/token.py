from datetime import datetime, timedelta, timezone
import jwt

# Ela é utilizada para assinar o token.
# Somente quem conhece essa chave consegue:
# criar um token válido;
# verificar se o token foi alterado.
SECRET_KEY = "sua-chave-super-secreta"
# Aqui você define o algoritmo de criptografia utilizado para assinar o JWT.
ALGORITHM = "HS256"
# Define que o token será válido durante 60 minutos.
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# cria um token contendo informações do usuário e adiciona uma data de expiração de 60 minutos. 
# O token é assinado utilizando uma chave secreta (SECRET_KEY) e o algoritmo HS256, 
# garantindo que ele não possa ser alterado sem ser detectado
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# recebe o token enviado pelo cliente, verifica sua assinatura, confirma se ele ainda é válido e devolve os dados do usuário. 
# Se o token estiver expirado ou tiver sido modificado, a autenticação falha e a API retorna um erro 401."
def decode_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload