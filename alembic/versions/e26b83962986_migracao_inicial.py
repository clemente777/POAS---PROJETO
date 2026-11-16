
"""Migracao inicial completa do Petonline24h.

Revision ID: e26b83962986
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e26b83962986"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # USUARIOS
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "perfil",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(
        "ix_usuarios_email",
        "usuarios",
        ["email"],
        unique=True,
    )

    # VACINAS
    op.create_table(
        "vacinas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("fabricante", sa.String(length=100), nullable=False),
        sa.Column("quantidade_doses", sa.Integer(), nullable=False),
        sa.Column("intervalo_dias", sa.Integer(), nullable=False),
        sa.Column("descricao", sa.String(length=300), nullable=True),
        sa.Column("data_criacao", sa.DateTime(), nullable=False),
        sa.Column("data_atualizacao", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # PRODUTOS
    op.create_table(
        "produtos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("descricao", sa.String(length=255), nullable=False),
        sa.Column("preco", sa.Float(), nullable=False),
        sa.Column("estoque", sa.Integer(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # TOKENS REVOGADOS
    op.create_table(
        "tokens_revogados",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=600), nullable=False),
        sa.Column("expira_em", sa.DateTime(), nullable=False),
        sa.Column(
            "revogado_em",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )

    # CLIENTES
    op.create_table(
        "clientes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("cpf", sa.String(length=14), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("endereco", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("usuario_id"),
    )
    op.create_index(
        "ix_clientes_cpf",
        "clientes",
        ["cpf"],
        unique=True,
    )
    op.create_index(
        "ix_clientes_email",
        "clientes",
        ["email"],
        unique=True,
    )

    # ANIMAIS
    op.create_table(
        "animais",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("especie", sa.String(length=100), nullable=False),
        sa.Column("raca", sa.String(length=100), nullable=False),
        sa.Column("idade", sa.Integer(), nullable=False),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["clientes.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # AGENDAMENTOS
    op.create_table(
        "agendamentos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data_agendamento", sa.DateTime(), nullable=False),
        sa.Column("descricao", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("animal_id", sa.Integer(), nullable=False),
        sa.Column("veterinario_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["animal_id"],
            ["animais.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["veterinario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ATENDIMENTOS
    op.create_table(
        "atendimentos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "data_atendimento",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("diagnostico", sa.String(length=500), nullable=False),
        sa.Column("observacoes", sa.String(length=1000), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("animal_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["animal_id"],
            ["animais.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # APLICACOES DE VACINAS
    op.create_table(
        "aplicacoes_vacina",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("animal_id", sa.Integer(), nullable=False),
        sa.Column("vacina_id", sa.Integer(), nullable=False),
        sa.Column("veterinario_id", sa.Integer(), nullable=False),
        sa.Column("data_aplicacao", sa.DateTime(), nullable=False),
        sa.Column("proxima_dose", sa.DateTime(), nullable=True),
        sa.Column("lote", sa.String(length=100), nullable=True),
        sa.Column("observacoes", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(
            ["animal_id"],
            ["animais.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vacina_id"],
            ["vacinas.id"],
        ),
        sa.ForeignKeyConstraint(
            ["veterinario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # CARRINHOS
    op.create_table(
        "carrinhos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "data_criacao",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["clientes.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ITENS DO CARRINHO
    op.create_table(
        "itens_carrinho",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("carrinho_id", sa.Integer(), nullable=False),
        sa.Column("produto_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["carrinho_id"],
            ["carrinhos.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["produto_id"],
            ["produtos.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("itens_carrinho")
    op.drop_table("carrinhos")
    op.drop_table("aplicacoes_vacina")
    op.drop_table("atendimentos")
    op.drop_table("agendamentos")
    op.drop_table("animais")
    op.drop_index("ix_clientes_email", table_name="clientes")
    op.drop_index("ix_clientes_cpf", table_name="clientes")
    op.drop_table("clientes")
    op.drop_table("tokens_revogados")
    op.drop_table("produtos")
    op.drop_table("vacinas")
    op.drop_index("ix_usuarios_email", table_name="usuarios")
    op.drop_table("usuarios")
