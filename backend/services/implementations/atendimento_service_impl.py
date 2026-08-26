from datetime import datetime, timezone

from fastapi import HTTPException

from backend.models.atendimento_model import Atendimentos
from backend.models.animal_model import Animais
from backend.models.usuario_model import Usuarios

from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoUpdate
)

from backend.repositories.atendimento_repository import (
    AtendimentoRepository
)


class AtendimentoServiceImpl:

    """
    Service responsável pelas regras de negócio
    dos atendimentos.

    Regras:

    - Somente Veterinário e Administrador criam atendimentos.
    - Cliente só visualiza histórico dos seus animais.
    - Veterinário e Administrador possuem acesso total.
    - Diagnóstico é obrigatório.
    - Data não pode ser futura.
    - Histórico não pode ser apagado.
    - Atendimento finalizado não pode ser alterado.
    """

    def __init__(
        self,
        repository: AtendimentoRepository,
        usuario_logado: Usuarios
    ):

        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # PERFIL
    # ==========================================================

    def obter_perfil(self):

        perfil = self.usuario_logado.perfil

        if hasattr(
            perfil,
            "nome"
        ):

            return perfil.nome

        return perfil

    # ==========================================================
    # PERMISSÃO
    # ==========================================================

    def validar_permissao(self):

        perfil = self.obter_perfil()

        if perfil not in (
            "Veterinário",
            "Administrador"
        ):

            raise HTTPException(
                status_code=403,
                detail=(
                    "Sem permissão para "
                    "gerenciar atendimentos."
                )
            )

    # ==========================================================
    # USUÁRIO
    # ==========================================================

    def buscar_usuario(
        self,
        usuario_id: int
    ) -> Usuarios:

        usuario = self.repository.buscar_usuario(
            usuario_id
        )

        if not usuario:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        return usuario

    # ==========================================================
    # USUÁRIO ATIVO
    # ==========================================================

    def validar_usuario_ativo(
        self,
        usuario: Usuarios
    ):

        if hasattr(
            usuario,
            "ativo"
        ):

            if not usuario.ativo:

                raise HTTPException(
                    status_code=403,
                    detail="Usuário desativado."
                )

    # ==========================================================
    # VETERINÁRIO
    # ==========================================================

    def validar_veterinario(
        self,
        usuario: Usuarios
    ):

        perfil = usuario.perfil

        if hasattr(
            perfil,
            "nome"
        ):

            perfil = perfil.nome

        if perfil not in (
            "Veterinário",
            "Administrador"
        ):

            raise HTTPException(
                status_code=403,
                detail=(
                    "Usuário informado "
                    "não é veterinário."
                )
            )

    # ==========================================================
    # ANIMAL
    # ==========================================================

    def buscar_animal(
        self,
        animal_id: int
    ) -> Animais:

        animal = self.repository.buscar_animal(
            animal_id
        )

        if not animal:

            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )

        self.validar_acesso_animal(
            animal
        )

        return animal

    # ==========================================================
    # ACESSO AO ANIMAL
    # ==========================================================

    def validar_acesso_animal(
        self,
        animal: Animais
    ):

        perfil = self.obter_perfil()

        # Veterinário e Administrador
        # possuem acesso total.

        if perfil in (
            "Veterinário",
            "Administrador"
        ):

            return

        # Cliente só acessa
        # os próprios animais.

        if perfil == "Cliente":

            cliente = (
                self.repository
                .buscar_cliente_por_usuario(
                    self.usuario_logado.id
                )
            )

            if not cliente:

                raise HTTPException(
                    status_code=403,
                    detail="Cliente não encontrado."
                )

            if animal.cliente_id != cliente.id:

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Você não possui acesso "
                        "a este animal."
                    )
                )

            return

        raise HTTPException(
            status_code=403,
            detail="Perfil sem permissão."
        )

    # ==========================================================
    # ATENDIMENTO
    # ==========================================================

    def buscar_por_id(
        self,
        id: int
    ) -> Atendimentos:

        atendimento = (
            self.repository
            .buscar_por_id(id)
        )

        if not atendimento:

            raise HTTPException(
                status_code=404,
                detail="Atendimento não encontrado."
            )

        # Verifica existência e
        # permissão sobre o animal.

        self.buscar_animal(
            atendimento.animal_id
        )

        return atendimento

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    def validar_diagnostico(
        self,
        diagnostico: str
    ):

        if (
            not diagnostico
            or not diagnostico.strip()
        ):

            raise HTTPException(
                status_code=400,
                detail="Diagnóstico obrigatório."
            )

    def validar_observacoes(
        self,
        observacoes: str | None
    ):

        if observacoes is None:
            return

        if not observacoes.strip():

            raise HTTPException(
                status_code=400,
                detail="Observações inválidas."
            )

    def validar_data(
        self,
        data: datetime
    ):

        agora = datetime.now(
            timezone.utc
        )

        if data.tzinfo is None:

            data = data.replace(
                tzinfo=timezone.utc
            )

        if data > agora:

            raise HTTPException(
                status_code=400,
                detail=(
                    "A data do atendimento "
                    "não pode ser futura."
                )
            )

    def validar_duplicidade(
        self,
        animal_id: int,
        data: datetime,
        excluir_id: int | None = None
    ):
        existe = (
            self.repository
            .buscar_duplicado(
                animal_id,
                data,
                excluir_id
            )
        )

        if existe:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Já existe atendimento "
                    "registrado nesta data."
                )
            )

    def validar_finalizado(
        self,
        atendimento: Atendimentos,
        campos: list[str] | None = None
    ):

        if atendimento.status != "Finalizado":
            return

        campos_bloqueados = [
            "data_atendimento",
            "usuario_id",
            "animal_id",
            "status"
        ]

        if not campos:
            return

        for campo in campos:

            if campo in campos_bloqueados:

                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Atendimento finalizado "
                        "não pode ser alterado."
                    )
                )

    # ==========================================================
    # CRIAR
    # ==========================================================

    def criar(
        self,
        atendimento: AtendimentoCreate
    ):

        self.validar_permissao()

        self.buscar_animal(
            atendimento.animal_id
        )

        self.validar_diagnostico(
            atendimento.diagnostico
        )

        self.validar_observacoes(
            atendimento.observacoes
        )

        self.validar_data(
            atendimento.data_atendimento
        )

        veterinario = self.buscar_usuario(
            atendimento.usuario_id
        )

        self.validar_usuario_ativo(
            veterinario
        )

        self.validar_veterinario(
            veterinario
        )

        self.validar_duplicidade(
            atendimento.animal_id,
            atendimento.data_atendimento
        )

        novo = Atendimentos(
            **atendimento.model_dump()
        )



        return self.repository.criar(
                novo
            )

    # ==========================================================
    # LISTAR
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        usuario_id: int | None = None,
        diagnostico: str | None = None,
        data: datetime | None = None,
        sort_by: str = "data_atendimento",
        order: str = "asc"
    ):

        perfil = self.obter_perfil()

        # ------------------------------------------------------
        # PAGINAÇÃO
        # ------------------------------------------------------

        if skip < 0:
            skip = 0

        if limit <= 0:
            limit = 10

        if limit > 100:
            limit = 100

        # ------------------------------------------------------
        # ACESSO DO CLIENTE
        # ------------------------------------------------------

        cliente_id = None

        if perfil == "Cliente":

            cliente = (
                self.repository
                .buscar_cliente_por_usuario(
                    self.usuario_logado.id
                )
            )

            if not cliente:

                raise HTTPException(
                    status_code=403,
                    detail="Cliente não encontrado."
                )

            cliente_id = cliente.id

        elif perfil not in (
            "Veterinário",
            "Administrador"
        ):

            raise HTTPException(
                status_code=403,
                detail="Perfil sem permissão."
            )

        # ------------------------------------------------------
        # BUSCA
        # ------------------------------------------------------

        return self.repository.listar(
            skip=skip,
            limit=limit,
            animal_id=animal_id,
            usuario_id=usuario_id,
            diagnostico=diagnostico,
            data=data,
            cliente_id=cliente_id,
            sort_by=sort_by,
            order=order
        )

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

    def atualizar(
        self,
        id: int,
        atendimento: AtendimentoUpdate
    ):

        self.validar_permissao()

        db = self.buscar_por_id(
            id
        )

        dados = atendimento.model_dump(
            exclude_unset=True
        )

        self.validar_finalizado(
            db,
            list(dados.keys())
        )

        # ------------------------------------------------------
        # DIAGNÓSTICO
        # ------------------------------------------------------

        if "diagnostico" in dados:

            self.validar_diagnostico(
                dados["diagnostico"]
            )

            db.diagnostico = (
                dados["diagnostico"].strip()
            )

        # ------------------------------------------------------
        # OBSERVAÇÕES
        # ------------------------------------------------------

        if "observacoes" in dados:

            self.validar_observacoes(
                dados["observacoes"]
            )

            db.observacoes = (
                dados["observacoes"]
            )

        # ------------------------------------------------------
        # DATA
        # ------------------------------------------------------

        if "data_atendimento" in dados:

            self.validar_data(
                dados["data_atendimento"]
            )

            # Verificar duplicidade
            # para a nova data.

            self.validar_duplicidade(
                db.animal_id,
                dados["data_atendimento"],
                excluir_id=db.id
            )

            db.data_atendimento = (
                dados["data_atendimento"]
            )

        # ------------------------------------------------------
        # VETERINÁRIO
        # ------------------------------------------------------

        if "usuario_id" in dados:

            veterinario = self.buscar_usuario(
                dados["usuario_id"]
            )

            self.validar_usuario_ativo(
                veterinario
            )

            self.validar_veterinario(
                veterinario
            )

            db.usuario_id = (
                dados["usuario_id"]
            )


        return self.repository.atualizar(
                db
            )



    # ==========================================================
    # CANCELAR
    # ==========================================================

    def cancelar(
        self,
        id: int
    ):

        self.validar_permissao()

        atendimento = self.buscar_por_id(
            id
        )

        if atendimento.status == "Finalizado":

            raise HTTPException(
                status_code=409,
                detail=(
                    "Não é possível cancelar "
                    "atendimento finalizado."
                )
            )

        atendimento.status = "Cancelado"

        return self.repository.atualizar(
                atendimento
            )



    # ==========================================================
    # DELETAR
    # ==========================================================

    def deletar(
        self,
        id: int
    ):

        self.validar_permissao()

        self.buscar_por_id(
            id
        )

        raise HTTPException(
            status_code=409,
            detail=(
                "Atendimentos não podem ser "
                "excluídos. Histórico deve ser preservado."
            )
        )

    # ==========================================================
    # HISTÓRICO
    # ==========================================================

    def historico_completo(
        self,
        animal_id: int,
        skip: int = 0,
        limit: int = 10
    ):

        animal = self.buscar_animal(
            animal_id
        )

        if skip < 0:
            skip = 0

        if limit <= 0:
            limit = 10

        if limit > 100:
            limit = 100

        atendimentos = (
            self.repository
            .listar_historico(
                animal_id,
                skip,
                limit
            )
        )

        historico = []

        for atendimento in atendimentos:

            veterinario = None

            if atendimento.usuario:

                veterinario = (
                    atendimento.usuario.nome
                )

            historico.append(
                {
                    "id": atendimento.id,

                    "data": (
                        atendimento.data_atendimento
                    ),

                    "veterinario": veterinario,

                    "diagnostico": (
                        atendimento.diagnostico
                    ),

                    "observacoes": (
                        atendimento.observacoes
                    )
                }
            )

        cliente = animal.cliente

        return {
            "animal": {
                "id": animal.id,
                "nome": animal.nome,
                "especie": animal.especie,
                "raca": animal.raca,
                "idade": animal.idade
            },

            "cliente": {
                "id": cliente.id,
                "nome": cliente.nome,
                "telefone": cliente.telefone,
                "email": cliente.email
            } if cliente else None,

            "paginacao": {
                "skip": skip,
                "limit": limit,
                "quantidade": len(historico)
            },

            "historico": historico
        }