from pydantic import BaseModel, EmailStr


class CadastroCreate(BaseModel):

    nome: str

    cpf: str

    telefone: str

    email: EmailStr

    endereco: str

    senha: str