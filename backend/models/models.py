from datetime import datetime
from typing import Optional, List
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class Usuarios(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, nullable=False, unique=True)
    senha_hash: str = Field(default=None, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.now)

    atendimentos: List["Atendimentos"] = Relationship(back_populates="usuario")


class Clientes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)
    cpf: str = Field(default=None, nullable=False, unique=True)
    telefone: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, nullable=False, unique=True)
    endereco: str = Field(default=None, nullable=False)

    animais: List["Animais"] = Relationship(back_populates="cliente")


class Animais(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False)
    especie: str = Field(nullable=False)
    raca: str = Field(nullable=False)
    idade: int = Field(nullable=False)

    cliente_id: int = Field(foreign_key="clientes.id")

    cliente: Optional["Clientes"] = Relationship(back_populates="animais")
    agendamentos: List["Agendamentos"] = Relationship(back_populates="animal")
    atendimentos: List["Atendimentos"] = Relationship(back_populates="animal")


class Agendamentos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_agendamento: datetime = Field(nullable=False)
    descricao: str = Field(nullable=False)
    status: str = Field(default="Pendente")

    animal_id: int = Field(foreign_key="animais.id")

    animal: Optional["Animais"] = Relationship(back_populates="agendamentos")


class Atendimentos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    data_atendimento: datetime = Field(default_factory=datetime.now)
    diagnostico: str = Field(nullable=False)
    observacoes: str = Field(default="")

    animal_id: int = Field(foreign_key="animais.id")
    usuario_id: int = Field(foreign_key="usuarios.id")

    animal: Optional["Animais"] = Relationship(back_populates="atendimentos")
    usuario: Optional["Usuarios"] = Relationship(back_populates="atendimentos")