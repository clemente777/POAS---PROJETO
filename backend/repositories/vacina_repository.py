from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models.aplicacao_vacina_model import (
    AplicacoesVacina
)
from backend.models.vacina_model import Vacinas


class VacinaRepository:

    def __init__(self, session: Session):
        self.session = session

    # ==================================================
    # LISTAR VACINAS
    # ==================================================

    def listar(self):
        return self.session.scalars(
            select(Vacinas)
            .order_by(Vacinas.nome)
        ).all()

    # ==================================================
    # BUSCAR VACINA POR ID
    # ==================================================

    def buscar_por_id(
        self,
        vacina_id: int
    ):
        return self.session.get(
            Vacinas,
            vacina_id
        )

    # ==================================================
    # BUSCAR VACINA POR NOME
    # ==================================================

    def buscar_por_nome(
        self,
        nome: str
    ):
        return self.session.scalars(
            select(Vacinas)
            .where(
                Vacinas.nome.ilike(
                    f"%{nome}%"
                )
            )
            .order_by(
                Vacinas.nome
            )
        ).all()

    # ==================================================
    # BUSCAR VACINA PELO NOME EXATO
    # ==================================================

    def buscar_por_nome_exato(
        self,
        nome: str
    ):
        return self.session.scalar(
            select(Vacinas)
            .where(
                func.lower(Vacinas.nome)
                == nome.lower()
            )
        )

    # ==================================================
    # BUSCAR VACINA POR NOME EXATO
    # EXCLUINDO UMA VACINA
    # ==================================================

    def buscar_por_nome_exato_excluindo_id(
        self,
        nome: str,
        vacina_id: int
    ):
        return self.session.scalar(
            select(Vacinas)
            .where(
                func.lower(Vacinas.nome)
                == nome.lower()
            )
            .where(
                Vacinas.id != vacina_id
            )
        )

    # ==================================================
    # CONTAR APLICAÇÕES DA VACINA
    # ==================================================

    def contar_aplicacoes(
        self,
        vacina_id: int
    ):
        return self.session.scalar(
            select(func.count())
            .select_from(
                AplicacoesVacina
            )
            .where(
                AplicacoesVacina.vacina_id
                == vacina_id
            )
        )

    # ==================================================
    # CRIAR VACINA
    # ==================================================

    def criar(
        self,
        vacina: Vacinas
    ):
        self.session.add(
            vacina
        )

        self.session.commit()

        self.session.refresh(
            vacina
        )

        return vacina

    # ==================================================
    # ATUALIZAR VACINA
    # ==================================================

    def atualizar(
        self,
        vacina: Vacinas
    ):
        self.session.commit()

        self.session.refresh(
            vacina
        )

        return vacina

    # ==================================================
    # DELETAR VACINA
    # ==================================================

    def deletar(
        self,
        vacina: Vacinas
    ):
        self.session.delete(
            vacina
        )

        self.session.commit()

        return {
            "mensagem": "Vacina removida com sucesso."
        }

    # ==================================================
    # ROLLBACK
    # ==================================================

    def rollback(self):
        self.session.rollback()

