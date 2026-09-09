from fastapi import HTTPException

from backend.models.vacina_model import Vacinas

from backend.schemas.vacina_schema import (
    VacinaCreate,
    VacinaUpdate
)

from backend.services.interfaces.vacina_service import (
    VacinaService
)

from backend.repositories.vacina_repository import (
    VacinaRepository
)


class VacinaServiceImpl(VacinaService):

    def __init__(
        self,
        repository: VacinaRepository
    ):
        self.repository = repository

    # ==================================================
    # LISTAR
    # ==================================================

    def listar(self):

        return self.repository.listar()

    # ==================================================
    # BUSCAR POR ID
    # ==================================================

    def buscar_por_id(
        self,
        vacina_id: int
    ):

        vacina = self.repository.buscar_por_id(
            vacina_id
        )

        if not vacina:
            raise HTTPException(
                status_code=404,
                detail="Vacina não encontrada."
            )

        return vacina

    # ==================================================
    # BUSCAR POR NOME
    # ==================================================

    def buscar_por_nome(
        self,
        nome: str
    ):

        return self.repository.buscar_por_nome(
            nome
        )

    # ==================================================
    # CADASTRAR
    # ==================================================

    def cadastrar(
        self,
        dados: VacinaCreate
    ):

        # --------------------------------------------------
        # NORMALIZAR NOME
        # --------------------------------------------------

        nome = dados.nome.strip()

        if not nome:
            raise HTTPException(
                status_code=400,
                detail="Nome da vacina é obrigatório."
            )

        # --------------------------------------------------
        # VERIFICAR DUPLICIDADE
        # --------------------------------------------------

        vacina_existente = (
            self.repository.buscar_por_nome_exato(
                nome
            )
        )

        if vacina_existente:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Já existe uma vacina cadastrada "
                    "com esse nome."
                )
            )

        # --------------------------------------------------
        # CRIAR VACINA
        # --------------------------------------------------

        vacina = Vacinas(
            nome=nome,
            fabricante=dados.fabricante,
            quantidade_doses=dados.quantidade_doses,
            intervalo_dias=dados.intervalo_dias,
            descricao=dados.descricao
        )

        try:

            return self.repository.criar(
                vacina
            )

        except Exception:

            self.repository.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao cadastrar vacina."
            )

    # ==================================================
    # ATUALIZAR
    # ==================================================

    def atualizar(
        self,
        vacina_id: int,
        dados: VacinaUpdate
    ):

        vacina = self.buscar_por_id(
            vacina_id
        )

        # --------------------------------------------------
        # ATUALIZAR NOME
        # --------------------------------------------------

        if dados.nome is not None:

            nome = dados.nome.strip()

            if not nome:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Nome da vacina "
                        "não pode ser vazio."
                    )
                )

            vacina_existente = (
                self.repository
                .buscar_por_nome_exato_excluindo_id(
                    nome,
                    vacina.id
                )
            )

            if vacina_existente:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Já existe uma vacina cadastrada "
                        "com esse nome."
                    )
                )

            vacina.nome = nome

        # --------------------------------------------------
        # ATUALIZAR FABRICANTE
        # --------------------------------------------------

        if dados.fabricante is not None:
            vacina.fabricante = dados.fabricante

        # --------------------------------------------------
        # ATUALIZAR QUANTIDADE DE DOSES
        # --------------------------------------------------

        if dados.quantidade_doses is not None:

            if dados.quantidade_doses <= 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade de doses "
                        "deve ser maior que zero."
                    )
                )

            vacina.quantidade_doses = (
                dados.quantidade_doses
            )

        # --------------------------------------------------
        # ATUALIZAR INTERVALO
        # --------------------------------------------------

        if dados.intervalo_dias is not None:

            if dados.intervalo_dias < 0:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Intervalo de dias "
                        "não pode ser negativo."
                    )
                )

            vacina.intervalo_dias = (
                dados.intervalo_dias
            )

        # --------------------------------------------------
        # ATUALIZAR DESCRIÇÃO
        # --------------------------------------------------

        if dados.descricao is not None:
            vacina.descricao = dados.descricao

        try:

            return self.repository.atualizar(
                vacina
            )

        except Exception:

            self.repository.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao atualizar vacina."
            )

    # ==================================================
    # DELETAR
    # ==================================================

    def deletar(
        self,
        vacina_id: int
    ):

        vacina = self.buscar_por_id(
            vacina_id
        )

        # --------------------------------------------------
        # VERIFICAR APLICAÇÕES EXISTENTES
        # --------------------------------------------------

        quantidade_aplicacoes = (
            self.repository.contar_aplicacoes(
                vacina.id
            )
        )

        if quantidade_aplicacoes > 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Não é possível excluir uma vacina "
                    "que possui aplicações registradas."
                )
            )

        try:

            return self.repository.deletar(
                vacina
            )

        except Exception:

            self.repository.rollback()

            raise HTTPException(
                status_code=500,
                detail="Erro ao excluir vacina."
            )

