from datetime import datetime, timezone

from fastapi import HTTPException

from backend.models.agendamento_model import Agendamentos
from backend.models.animal_model import Animais
from backend.models.usuario_model import Usuarios

from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate
)

from backend.repositories.agendamento_repository import (
    AgendamentoRepository
)


class AgendamentoServiceImpl:
    """
    Regras de negócio dos agendamentos.

    Regras:

    - Cliente agenda apenas seus animais.
    - Veterinário e Administrador possuem acesso total.
    - Animal precisa existir.
    - Data não pode estar no passado.
    - Não permite conflito de horário.
    - Status possui valores controlados.
    - Histórico não é apagado.
    """

    STATUS_VALIDOS = [
        "Pendente",
        "Confirmado",
        "Cancelado",
        "Finalizado"
    ]

    def __init__(
        self,
        repository: AgendamentoRepository,
        usuario_logado: Usuarios
    ):
        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # PERFIL
    # ==========================================================

    def obter_perfil(self):

        perfil = self.usuario_logado.perfil

        if hasattr(perfil, "nome"):
            return perfil.nome

        return perfil

    # ==========================================================
    # VERIFICAR ACESSO AO ANIMAL
    # ==========================================================

    def verificar_acesso_animal(
        self,
        animal: Animais
    ):

        perfil = self.obter_perfil()

        # ------------------------------------------------------
        # ADMINISTRADOR E VETERINÁRIO
        # ------------------------------------------------------

        if perfil in [
            "Administrador",
            "Veterinário"
        ]:
            return

        # ------------------------------------------------------
        # CLIENTE
        # ------------------------------------------------------

        if perfil == "Cliente":

            cliente = (
                self.repository
                .buscar_cliente_por_usuario_id(
                    self.usuario_logado.id
                )
            )

            if not cliente:

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Usuário não possui "
                        "cliente vinculado."
                    )
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

        # ------------------------------------------------------
        # PERFIL INVÁLIDO
        # ------------------------------------------------------

        raise HTTPException(
            status_code=403,
            detail="Perfil sem permissão."
        )

    # ==========================================================
    # BUSCAR ANIMAL
    # ==========================================================

    def buscar_animal(
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

        self.verificar_acesso_animal(
            animal
        )

        return animal

    # ==========================================================
    # BUSCAR AGENDAMENTO POR ID
    # ==========================================================

    def buscar_por_id(
        self,
        id: int
    ):

        agendamento = (
            self.repository.buscar_por_id(id)
        )

        if not agendamento:

            raise HTTPException(
                status_code=404,
                detail="Agendamento não encontrado."
            )

        self.verificar_acesso_animal(
            agendamento.animal
        )

        return agendamento

    # ==========================================================
    # VALIDAÇÃO DE DATA
    # ==========================================================

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

        if data < agora:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Não é permitido agendamento "
                    "em data passada."
                )
            )

    # ==========================================================
    # VALIDAÇÃO DE STATUS
    # ==========================================================

    def validar_status(
        self,
        status: str
    ):

        if status not in self.STATUS_VALIDOS:

            raise HTTPException(
                status_code=400,
                detail="Status inválido."
            )

    # ==========================================================
    # VALIDAÇÃO DE DESCRIÇÃO
    # ==========================================================

    def validar_descricao(
        self,
        descricao: str
    ):

        if not descricao:

            raise HTTPException(
                status_code=400,
                detail="Descrição obrigatória."
            )

        descricao = descricao.strip()

        if not descricao:

            raise HTTPException(
                status_code=400,
                detail="Descrição inválida."
            )

        if len(descricao) < 5:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Descrição deve possuir "
                    "no mínimo 5 caracteres."
                )
            )

    # ==========================================================
    # VALIDAÇÃO DE CONFLITO
    # ==========================================================

    def validar_conflito_horario(
        self,
        animal_id: int,
        data: datetime,
        agendamento_id: int | None = None
    ):

        existe = (
            self.repository
            .buscar_conflito_horario(
                animal_id,
                data,
                agendamento_id
            )
        )

        if existe:

            raise HTTPException(
                status_code=409,
                detail=(
                    "Já existe agendamento para "
                    "este animal neste horário."
                )
            )

    # ==========================================================
    # CRIAR AGENDAMENTO
    # ==========================================================

    def criar(
        self,
        agendamento: AgendamentoCreate
    ):

        animal = self.buscar_animal(
            agendamento.animal_id
        )

        self.validar_data(
            agendamento.data_agendamento
        )

        self.validar_descricao(
            agendamento.descricao
        )

        self.validar_conflito_horario(
            agendamento.animal_id,
            agendamento.data_agendamento
        )

        dados = agendamento.model_dump()

        # ------------------------------------------------------
        # VETERINÁRIO É AUTOMATICAMENTE ASSOCIADO
        # ------------------------------------------------------

        if self.obter_perfil() == "Veterinário":

            dados["veterinario_id"] = (
                self.usuario_logado.id
            )

        novo = Agendamentos(
            **dados,
            status="Pendente"
        )

        try:

            return self.repository.criar(
                novo
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Erro ao criar agendamento."
            )

    # ==========================================================
    # ATRIBUIR VETERINÁRIO
    # ==========================================================

    def atribuir_veterinario(
        self,
        id: int,
        veterinario_id: int
    ):

        agendamento = self.buscar_por_id(
            id
        )

        veterinario = (
            self.repository
            .buscar_veterinario_por_id(
                veterinario_id
            )
        )

        if not veterinario:

            raise HTTPException(
                status_code=404,
                detail="Veterinário não encontrado."
            )

        if veterinario.perfil != "Veterinário":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Usuário informado "
                    "não é veterinário."
                )
            )

        agendamento.veterinario_id = (
            veterinario_id
        )

        try:

            return self.repository.atualizar(
                agendamento
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Erro ao atribuir veterinário."
                )
            )

    # ==========================================================
    # LISTAR AGENDAMENTOS
    # ==========================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        status: str | None = None,
        descricao: str | None = None,
        data: datetime | None = None,
        sort_by: str = "data_agendamento",
        order: str = "asc"
    ):

        perfil = self.obter_perfil()

        cliente_id = None

        # ------------------------------------------------------
        # CLIENTE SÓ VISUALIZA SEUS ANIMAIS
        # ------------------------------------------------------

        if perfil == "Cliente":

            cliente = (
                self.repository
                .buscar_cliente_por_usuario_id(
                    self.usuario_logado.id
                )
            )

            if not cliente:

                raise HTTPException(
                    status_code=403,
                    detail="Cliente não encontrado."
                )

            cliente_id = cliente.id

        # ------------------------------------------------------
        # STATUS
        # ------------------------------------------------------

        if status:

            self.validar_status(
                status
            )

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
        # LISTAGEM
        # ------------------------------------------------------

        return self.repository.listar(
            skip=skip,
            limit=limit,
            animal_id=animal_id,
            status=status,
            descricao=(
                descricao.strip()
                if descricao
                else None
            ),
            data=data,
            cliente_id=cliente_id,
            sort_by=sort_by,
            order=order
        )

    # ==========================================================
    # ATUALIZAR AGENDAMENTO
    # ==========================================================

    def atualizar(
        self,
        id: int,
        dados: AgendamentoUpdate
    ):

        agendamento = self.buscar_por_id(
            id
        )

        valores = dados.model_dump(
            exclude_unset=True
        )

        if not valores:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Nenhum dado informado "
                    "para atualização."
                )
            )

        # ------------------------------------------------------
        # DATA
        # ------------------------------------------------------

        if "data_agendamento" in valores:

            self.validar_data(
                valores["data_agendamento"]
            )

            self.validar_conflito_horario(
                agendamento.animal_id,
                valores["data_agendamento"],
                agendamento.id
            )

        # ------------------------------------------------------
        # DESCRIÇÃO
        # ------------------------------------------------------

        if "descricao" in valores:

            self.validar_descricao(
                valores["descricao"]
            )

        # ------------------------------------------------------
        # STATUS
        # ------------------------------------------------------

        if "status" in valores:

            self.validar_status(
                valores["status"]
            )

        # ------------------------------------------------------
        # CAMPOS PERMITIDOS
        # ------------------------------------------------------

        campos_permitidos = [
            "data_agendamento",
            "descricao",
            "status"
        ]

        for campo, valor in valores.items():

            if campo in campos_permitidos:

                setattr(
                    agendamento,
                    campo,
                    valor
                )

        try:

            return self.repository.atualizar(
                agendamento
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Erro ao atualizar agendamento."
                )
            )

    # ==========================================================
    # CANCELAR AGENDAMENTO
    # ==========================================================

    def cancelar(
        self,
        id: int
    ):

        agendamento = self.buscar_por_id(
            id
        )

        if agendamento.status == "Finalizado":

            raise HTTPException(
                status_code=409,
                detail=(
                    "Não é possível cancelar "
                    "atendimento finalizado."
                )
            )

        if agendamento.status == "Cancelado":

            raise HTTPException(
                status_code=409,
                detail=(
                    "Agendamento já está cancelado."
                )
            )

        agendamento.status = "Cancelado"

        try:

            return self.repository.cancelar(
                agendamento
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Erro ao cancelar agendamento."
                )
            )

    # ==========================================================
    # DELETAR AGENDAMENTO
    #
    # BLOQUEADO
    # ==========================================================

    def deletar(
        self,
        id: int
    ):

        self.repository.buscar_por_id(
            id
        )

        raise HTTPException(
            status_code=409,
            detail=(
                "Agendamentos não podem ser "
                "excluídos. Utilize o cancelamento."
            )
        )

