from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
from backend.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(100))
    email = Column("email", String(100), unique=True,  nullable=False)
    senha = Column("senha", String(100))


