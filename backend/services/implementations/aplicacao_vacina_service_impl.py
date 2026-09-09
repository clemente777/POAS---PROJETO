from datetime import datetime, timedelta

from fastapi import HTTPException

from backend.models.aplicacao_vacina_model import AplicacoesVacina
from backend.models.usuario_model import Usuarios

from backend.schemas.aplicacao_vacina_schema import (
    AplicacaoVacinaCreate,
    AplicacaoVacinaUpdate
)

from backend.repositories.aplicacao_vacina_repository import (
    AplicacaoVacinaRepository
)

from backend.services.interfaces.aplicacao_vacina_service import (
    AplicacaoVacinaService
)


class AplicacaoVacinaServiceImpl(
    AplicacaoVacinaService
):
    """
    Service responsável pelas regras de negócio
    relacionadas às aplicações de vacina.
    """

    def __init__(
        self,
        repository: AplicacaoVacinaRepository,
        usuario_logado: Usuarios | None = None
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # LISTAR TODAS AS APLICAÇÕES
    # ==========================================================

    def listar(self):

        return self.repository.listar()

    # ==========================================================
    # BUSCAR APLICAÇÃO POR ID
    # ==========================================================

    def buscar_por_id(
        self,
        aplicacao_id: int
    ):

        aplicacao = self.repository.buscar_por_id(
            aplicacao_id
        )

        if not aplicacao:
            raise HTTPException(
                status_code=404,
                detail="Aplicação de vacina não encontrada."
            )

        return aplicacao

    # ==========================================================
    # LISTAR APLICAÇÕES DE UM ANIMAL
    # ==========================================================

    def listar_por_animal(
        self,
        animal_id: int
    ):

        animal = self.repository.buscar_animal(
            animal_id
        )

        if not animal:
            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )

        return self.repository.listar_por_animal(
            animal_id
        )

    # ==========================================================
    # APLICAR VACINA
    # ==========================================================

    def aplicar_vacina(
        self,
        dados: AplicacaoVacinaCreate,
        veterinario_id: int
    ):

        # ------------------------------------------------------
        # Verifica se o animal existe
        # ------------------------------------------------------

        animal = self.repository.buscar_animal(
            dados.animal_id
        )

        if not animal:
            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )

        # ------------------------------------------------------
        # Verifica se a vacina existe
        # ------------------------------------------------------

        vacina = self.repository.buscar_vacina(
            dados.vacina_id
        )

        if not vacina:
            raise HTTPException(
                status_code=404,
                detail="Vacina não encontrada."
            )

        # ------------------------------------------------------
        # Data atual da aplicação
        # ------------------------------------------------------

        data_aplicacao = datetime.now()

        # ------------------------------------------------------
        # Impede aplicar a mesma vacina no mesmo animal
        # no mesmo dia
        # ------------------------------------------------------

        aplicacao_existente = (
            self.repository.buscar_aplicacao_no_dia(
                animal_id=dados.animal_id,
                vacina_id=dados.vacina_id,
                data=data_aplicacao
            )
        )

        if aplicacao_existente:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Este animal já recebeu "
                    "esta vacina hoje."
                )
            )

        # ------------------------------------------------------
        # Calcula a próxima dose
        # ------------------------------------------------------

        proxima_dose = None

        if vacina.intervalo_dias:
            proxima_dose = (
                data_aplicacao
                + timedelta(
                    days=vacina.intervalo_dias
                )
            )

        # ------------------------------------------------------
        # Cria a aplicação
        # ------------------------------------------------------

        aplicacao = AplicacoesVacina(
            animal_id=dados.animal_id,
            vacina_id=dados.vacina_id,
            veterinario_id=veterinario_id,
            data_aplicacao=data_aplicacao,
            lote=dados.lote,
            observacoes=dados.observacoes,
            proxima_dose=proxima_dose
        )

        # ------------------------------------------------------
        # Repository salva no banco
        # ------------------------------------------------------

        return self.repository.criar(
            aplicacao
        )

    # ==========================================================
    # ATUALIZAR APLICAÇÃO
    # ==========================================================

    def atualizar(
        self,
        aplicacao_id: int,
        dados: AplicacaoVacinaUpdate
    ):

        aplicacao = self.buscar_por_id(
            aplicacao_id
        )

        # ------------------------------------------------------
        # Atualiza lote
        # ------------------------------------------------------

        if dados.lote is not None:
            aplicacao.lote = dados.lote

        # ------------------------------------------------------
        # Atualiza observações
        # ------------------------------------------------------

        if dados.observacoes is not None:
            aplicacao.observacoes = dados.observacoes

        # ------------------------------------------------------
        # Atualiza próxima dose
        # ------------------------------------------------------

        if dados.proxima_dose is not None:
            aplicacao.proxima_dose = dados.proxima_dose

        # ------------------------------------------------------
        # Repository salva as alterações
        # ------------------------------------------------------

        return self.repository.atualizar(
            aplicacao
        )

    # ==========================================================
    # DELETAR APLICAÇÃO
    # ==========================================================

    def deletar(
        self,
        aplicacao_id: int
    ):

        aplicacao = self.buscar_por_id(
            aplicacao_id
        )

        self.repository.deletar(
            aplicacao
        )

        return {
            "mensagem": (
                "Aplicação de vacina removida "
                "com sucesso."
            )
        }

