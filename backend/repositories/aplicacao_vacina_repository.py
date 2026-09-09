from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models.aplicacao_vacina_model import AplicacoesVacina
from backend.models.animal_model import Animais
from backend.models.vacina_model import Vacinas


class AplicacaoVacinaRepository:
    """
    Repository responsável exclusivamente pelo acesso
    aos dados de Aplicações de Vacina.
    """

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # BUSCAR APLICAÇÃO POR ID
    # ==========================================================

    def buscar_por_id(
        self,
        aplicacao_id: int
    ) -> AplicacoesVacina | None:

        return self.session.get(
            AplicacoesVacina,
            aplicacao_id
        )

    # ==========================================================
    # BUSCAR ANIMAL POR ID
    # ==========================================================

    def buscar_animal(
        self,
        animal_id: int
    ) -> Animais | None:

        return self.session.get(
            Animais,
            animal_id
        )

    # ==========================================================
    # BUSCAR VACINA POR ID
    # ==========================================================

    def buscar_vacina(
        self,
        vacina_id: int
    ) -> Vacinas | None:

        return self.session.get(
            Vacinas,
            vacina_id
        )

    # ==========================================================
    # BUSCAR APLICAÇÃO DA MESMA VACINA NO MESMO DIA
    # ==========================================================

    def buscar_aplicacao_no_dia(
        self,
        animal_id: int,
        vacina_id: int,
        data: datetime
    ) -> AplicacoesVacina | None:

        return self.session.scalar(
            select(AplicacoesVacina)
            .where(
                AplicacoesVacina.animal_id == animal_id
            )
            .where(
                AplicacoesVacina.vacina_id == vacina_id
            )
            .where(
                func.date(
                    AplicacoesVacina.data_aplicacao
                )
                == data.date()
            )
        )

    # ==========================================================
    # LISTAR TODAS AS APLICAÇÕES
    # ==========================================================

    def listar(self) -> list[AplicacoesVacina]:

        return self.session.scalars(
            select(AplicacoesVacina)
            .order_by(
                AplicacoesVacina.data_aplicacao.desc()
            )
        ).all()

    # ==========================================================
    # LISTAR APLICAÇÕES DE UM ANIMAL
    # ==========================================================

    def listar_por_animal(
        self,
        animal_id: int
    ) -> list[AplicacoesVacina]:

        return self.session.scalars(
            select(AplicacoesVacina)
            .where(
                AplicacoesVacina.animal_id == animal_id
            )
            .order_by(
                AplicacoesVacina.data_aplicacao.desc()
            )
        ).all()

    # ==========================================================
    # CRIAR APLICAÇÃO
    # ==========================================================

    def criar(
        self,
        aplicacao: AplicacoesVacina
    ) -> AplicacoesVacina:

        try:
            self.session.add(aplicacao)
            self.session.commit()
            self.session.refresh(aplicacao)

            return aplicacao

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # ATUALIZAR APLICAÇÃO
    # ==========================================================

    def atualizar(
        self,
        aplicacao: AplicacoesVacina
    ) -> AplicacoesVacina:

        try:
            self.session.commit()
            self.session.refresh(aplicacao)

            return aplicacao

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # DELETAR APLICAÇÃO
    # ==========================================================

    def deletar(
        self,
        aplicacao: AplicacoesVacina
    ) -> None:

        try:
            self.session.delete(aplicacao)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

