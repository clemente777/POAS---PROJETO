# from __future__ import annotations

# from datetime import datetime

# from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from backend.database.database import Base


# # =========================================================
# # USUÁRIOS
# # =========================================================
# class Usuarios(Base):
#     __tablename__ = "usuarios"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     nome: Mapped[str] = mapped_column(String(100), nullable=False)
#     email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
#     senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
#     criado_em: Mapped[datetime] = mapped_column(
#         DateTime, server_default=func.now(), nullable=False
#     )

#     atendimentos: Mapped[list["Atendimentos"]] = relationship(
#         back_populates="usuario",
#         lazy="selectin"
#     )


# # =========================================================
# # CLIENTES
# # =========================================================
# class Clientes(Base):
#     __tablename__ = "clientes"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     nome: Mapped[str] = mapped_column(String(100), nullable=False)
#     cpf: Mapped[str] = mapped_column(String(14), unique=True, index=True, nullable=False)
#     telefone: Mapped[str] = mapped_column(String(20), nullable=False)
#     email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
#     endereco: Mapped[str] = mapped_column(String(255), nullable=False)

#     animais: Mapped[list["Animais"]] = relationship(
#         back_populates="cliente",
#         lazy="selectin"
#     )

#     carrinhos: Mapped[list["Carrinhos"]] = relationship(
#         back_populates="cliente",
#         lazy="selectin"
#     )


# # =========================================================
# # ANIMAIS
# # =========================================================
# class Animais(Base):
#     __tablename__ = "animais"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     nome: Mapped[str] = mapped_column(String(100), nullable=False)
#     especie: Mapped[str] = mapped_column(String(100), nullable=False)
#     raca: Mapped[str] = mapped_column(String(100), nullable=False)
#     idade: Mapped[int] = mapped_column(Integer, nullable=False)

#     cliente_id: Mapped[int] = mapped_column(
#         ForeignKey("clientes.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     cliente: Mapped["Clientes"] = relationship(
#         back_populates="animais",
#         lazy="selectin"
#     )

#     agendamentos: Mapped[list["Agendamentos"]] = relationship(
#         back_populates="animal",
#         lazy="selectin"
#     )

#     atendimentos: Mapped[list["Atendimentos"]] = relationship(
#         back_populates="animal",
#         lazy="selectin"
#     )


# # =========================================================
# # AGENDAMENTOS
# # =========================================================
# class Agendamentos(Base):
#     __tablename__ = "agendamentos"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     data_agendamento: Mapped[datetime] = mapped_column(DateTime, nullable=False)
#     descricao: Mapped[str] = mapped_column(String(255), nullable=False)
#     status: Mapped[str] = mapped_column(String(30), default="Pendente", nullable=False)

#     animal_id: Mapped[int] = mapped_column(
#         ForeignKey("animais.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     animal: Mapped["Animais"] = relationship(
#         back_populates="agendamentos",
#         lazy="selectin"
#     )


# # =========================================================
# # ATENDIMENTOS
# # =========================================================
# class Atendimentos(Base):
#     __tablename__ = "atendimentos"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     data_atendimento: Mapped[datetime] = mapped_column(
#         DateTime,
#         server_default=func.now(),
#         nullable=False
#     )

#     diagnostico: Mapped[str] = mapped_column(String(500), nullable=False)
#     observacoes: Mapped[str] = mapped_column(String(1000), default="")

#     animal_id: Mapped[int] = mapped_column(
#         ForeignKey("animais.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     usuario_id: Mapped[int] = mapped_column(
#         ForeignKey("usuarios.id", ondelete="SET NULL"),
#         nullable=True
#     )

#     animal: Mapped["Animais"] = relationship(
#         back_populates="atendimentos",
#         lazy="selectin"
#     )

#     usuario: Mapped["Usuarios"] = relationship(
#         back_populates="atendimentos",
#         lazy="selectin"
#     )


# # =========================================================
# # PRODUTOS
# # =========================================================
# class Produtos(Base):
#     __tablename__ = "produtos"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     nome: Mapped[str] = mapped_column(String(100), nullable=False)
#     descricao: Mapped[str] = mapped_column(String(255), nullable=False)
#     preco: Mapped[float] = mapped_column(Float, nullable=False)
#     estoque: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

#     itens_carrinho: Mapped[list["ItensCarrinho"]] = relationship(
#         back_populates="produto",
#         lazy="selectin"
#     )


# # =========================================================
# # CARRINHOS
# # =========================================================
# class Carrinhos(Base):
#     __tablename__ = "carrinhos"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     data_criacao: Mapped[datetime] = mapped_column(
#         DateTime,
#         server_default=func.now(),
#         nullable=False
#     )

#     cliente_id: Mapped[int] = mapped_column(
#         ForeignKey("clientes.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     cliente: Mapped["Clientes"] = relationship(
#         back_populates="carrinhos",
#         lazy="selectin"
#     )

#     itens: Mapped[list["ItensCarrinho"]] = relationship(
#         back_populates="carrinho",
#         lazy="selectin"
#     )


# # =========================================================
# # ITENS CARRINHO
# # =========================================================
# class ItensCarrinho(Base):
#     __tablename__ = "itens_carrinho"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     quantidade: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

#     carrinho_id: Mapped[int] = mapped_column(
#         ForeignKey("carrinhos.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     produto_id: Mapped[int] = mapped_column(
#         ForeignKey("produtos.id", ondelete="RESTRICT"),
#         nullable=False
#     )

#     carrinho: Mapped["Carrinhos"] = relationship(
#         back_populates="itens",
#         lazy="selectin"
#     )

#     produto: Mapped["Produtos"] = relationship(
#         back_populates="itens_carrinho",
#         lazy="selectin"
#     )