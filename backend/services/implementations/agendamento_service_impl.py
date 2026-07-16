from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.agendamento_model import Agendamentos
from backend.models.animal_model import Animais

from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate
)


class AgendamentoServiceImpl:
    """
    Service responsável pelas regras de negócio
    dos agendamentos.

    Responsabilidades:

    - Validar consultas
    - Verificar existência do animal
    - Evitar conflitos de horário
    - Controlar status
    - Criar agendamentos
    - Atualizar consultas
    - Cancelar consultas
    """

    def __init__(self, session: Session):
        """
        Recebe a sessão do banco.

        Usada para:

        - Consultar dados
        - Criar registros
        - Atualizar registros
        - Remover registros
        """

        self.session = session


    # ==================================================
    # BUSCAS
    # ==================================================

    def buscar_por_id(self, id: int):
        """
        Busca agendamento pelo ID.

        Retorna:

        - Agendamento encontrado
        - None caso não exista
        """

        return self.session.scalars(
            select(Agendamentos)
            .where(Agendamentos.id == id)
        ).first()


    def buscar_animal(self, id: int):
        """
        Busca o animal relacionado ao agendamento.

        Todo agendamento precisa possuir
        um animal cadastrado.
        """

        return self.session.scalars(
            select(Animais)
            .where(Animais.id == id)
        ).first()



    # ==================================================
    # VALIDAÇÕES
    # ==================================================

    def validar_data(self, data_agendamento: datetime):
        """
        Verifica se a data do agendamento
        é futura.

        Bloqueia datas no passado.
        """

        agora = datetime.now()

        if data_agendamento <= agora:
            raise HTTPException(
                status_code=400,
                detail="A data do agendamento deve ser futura."
            )


    def validar_distancia_data(self, data_agendamento: datetime):
        """
        Impede agendamentos muito distantes.

        Regra:

        Máximo permitido:
        1 ano à frente.
        """

        limite = datetime.now().replace(
            year=datetime.now().year + 1
        )

        if data_agendamento > limite:
            raise HTTPException(
                status_code=400,
                detail="Não é permitido agendar mais de 1 ano à frente."
            )


    def validar_descricao(self, descricao: str):
        """
        Valida descrição do agendamento.

        Exemplos:

        Permitidos:

        - Consulta veterinária
        - Vacinação
        - Banho


        Bloqueados:

        ""
        "   "
        """

        if not descricao.strip():
            raise HTTPException(
                status_code=400,
                detail="Descrição é obrigatória."
            )


    def normalizar_descricao(self, descricao: str):
        """
        Remove espaços extras
        e padroniza texto.

        Exemplo:

        Entrada:

        " consulta "

        Saída:

        "Consulta"
        """

        return descricao.strip().capitalize()



    def validar_status(self, status: str):
        """
        Controla os status permitidos.

        Status válidos:

        - Pendente
        - Confirmado
        - Concluido
        - Cancelado
        """

        status_permitidos = [
            "Pendente",
            "Confirmado",
            "Concluido",
            "Cancelado"
        ]

        if status not in status_permitidos:
            raise HTTPException(
                status_code=400,
                detail="Status inválido."
            )

        # ==================================================
    # CRIAR AGENDAMENTO
    # ==================================================

    def criar(
        self,
        agendamento: AgendamentoCreate
    ):
        """
        Cria um novo agendamento.

        Regras aplicadas:

        1 - Animal precisa existir
        2 - Data precisa ser futura
        3 - Descrição obrigatória
        4 - Não permite conflito de horário
        5 - Novo agendamento inicia como Pendente


        Fluxo:

        Recebe dados

             ↓

        Valida informações

             ↓

        Verifica animal

             ↓

        Verifica conflitos

             ↓

        Cria agendamento

             ↓

        Salva no banco
        """


        # ==============================================
        # VALIDAR DESCRIÇÃO
        # ==============================================

        self.validar_descricao(
            agendamento.descricao
        )


        # ==============================================
        # VALIDAR DATA
        # ==============================================

        self.validar_data(
            agendamento.data_agendamento
        )


        # ==============================================
        # VALIDAR LIMITE DE DATA
        # ==============================================

        self.validar_distancia_data(
            agendamento.data_agendamento
        )


        # ==============================================
        # VERIFICAR ANIMAL
        # ==============================================

        animal = self.buscar_animal(
            agendamento.animal_id
        )


        if not animal:

            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )


        # ==============================================
        # VERIFICAR CONFLITO DE HORÁRIO
        # ==============================================

        conflito = self.session.scalars(

            select(Agendamentos)
            .where(
                Agendamentos.animal_id ==
                agendamento.animal_id
            )
            .where(
                Agendamentos.data_agendamento ==
                agendamento.data_agendamento
            )
            .where(
                Agendamentos.status != "Cancelado"
            )

        ).first()


        if conflito:

            raise HTTPException(
                status_code=409,
                detail=
                "Já existe agendamento nesse horário."
            )


        # ==============================================
        # NORMALIZAR DESCRIÇÃO
        # ==============================================

        dados = agendamento.model_dump()

        dados["descricao"] = self.normalizar_descricao(
            dados["descricao"]
        )


        # ==============================================
        # CRIAR OBJETO
        # ==============================================

        db = Agendamentos(
            **dados,
            status="Pendente"
        )


        # ==============================================
        # SALVAR NO BANCO
        # ==============================================

        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db



    # ==================================================
    # LISTAR AGENDAMENTOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        status: str | None = None,
        descricao: str | None = None,
        data: datetime | None = None,
        sort_by: str = "data_agendamento",
        order: str = "asc",
    ):
        """
        Lista agendamentos.
        Recursos:
        - Paginação
        - Filtros
        - Ordenação

        Exemplos:
        Buscar pendentes:
        /agendamentos?status=Pendente


        Buscar animal específico:

        /agendamentos?animal_id=1
        """


        query = select(Agendamentos)


        # ==============================================
        # FILTROS
        # ==============================================

        if animal_id is not None:

            query = query.where(
                Agendamentos.animal_id == animal_id
            )


        if status:

            query = query.where(
                Agendamentos.status.ilike(
                    f"%{status}%"
                )
            )


        if descricao:

            query = query.where(
                Agendamentos.descricao.ilike(
                    f"%{descricao}%"
                )
            )


        if data:

            query = query.where(
                Agendamentos.data_agendamento == data
            )


        # ==============================================
        # ORDENAÇÃO
        # ==============================================

        campos = {

            "id":
            Agendamentos.id,

            "data_agendamento":
            Agendamentos.data_agendamento,

            "status":
            Agendamentos.status,

            "descricao":
            Agendamentos.descricao,

            "animal_id":
            Agendamentos.animal_id
        }


        coluna = campos.get(
            sort_by,
            Agendamentos.data_agendamento
        )


        if order.lower() == "desc":

            query = query.order_by(
                desc(coluna)
            )

        else:

            query = query.order_by(
                asc(coluna)
            )


        # ==============================================
        # PAGINAÇÃO
        # ==============================================

        query = (
            query
            .offset(skip)
            .limit(limit)
        )


        return self.session.scalars(query).all()



    # ==================================================
    # ATUALIZAR AGENDAMENTO
    # ==================================================

    def atualizar(
        self,
        id: int,
        agendamento: AgendamentoUpdate
    ):
        """
        Atualiza um agendamento.

        Aceita atualização parcial.

        Exemplo:

        {
            "status":"Confirmado"
        }


        Apenas o status será alterado.
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Agendamento não encontrado."
            )


        dados = agendamento.model_dump(
            exclude_unset=True
        )


        # ==============================================
        # IMPEDIR ALTERAÇÃO DE CONCLUÍDO
        # ==============================================

        if db.status == "Concluido":

            raise HTTPException(
                status_code=409,
                detail=
                "Consulta concluída não pode ser alterada."
            )


        # ==============================================
        # VALIDAÇÕES
        # ==============================================

        if "data_agendamento" in dados:

            self.validar_data(
                dados["data_agendamento"]
            )


        if "descricao" in dados:

            self.validar_descricao(
                dados["descricao"]
            )

            dados["descricao"] = (
                self.normalizar_descricao(
                    dados["descricao"]
                )
            )


        if "status" in dados:

            self.validar_status(
                dados["status"]
            )


        # ==============================================
        # APLICAR ALTERAÇÕES
        # ==============================================

        for campo, valor in dados.items():

            setattr(
                db,
                campo,
                valor
            )


        self.session.commit()

        self.session.refresh(db)


        return db
    
        # ==================================================
    # CANCELAR AGENDAMENTO
    # ==================================================

    def cancelar(
        self,
        id: int
    ):
        """
        Cancela um agendamento.

        Não remove o registro do banco.

        Apenas altera o status para:

        Cancelado


        Mantém o histórico
        do atendimento.
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail=
                "Agendamento não encontrado."
            )


        # ==============================================
        # IMPEDIR CANCELAR CONCLUÍDO
        # ==============================================

        if db.status == "Concluido":

            raise HTTPException(
                status_code=409,
                detail=
                "Consulta concluída não pode ser cancelada."
            )


        # ==============================================
        # ALTERAR STATUS
        # ==============================================

        db.status = "Cancelado"


        self.session.commit()

        self.session.refresh(db)


        return db



    # ==================================================
    # VALIDAR DISTÂNCIA DA DATA
    # ==================================================

    def validar_distancia_data(
        self,
        data_agendamento: datetime
    ):
        """
        Controla o limite máximo
        para criação de agendamentos.

        Regra: Não permite agendar mais de 1 ano no futuro.

        Exemplo:

        Permitido:20/07/2027

        Bloqueado: 20/08/2028
        """


        agora = datetime.now()


        limite = agora.replace(
            year=agora.year + 1
        )


        if data_agendamento > limite:

            raise HTTPException(
                status_code=400,
                detail=
                "Não é permitido agendar mais de 1 ano à frente."
            )



    # ==================================================
    # NORMALIZAR DESCRIÇÃO
    # ==================================================

    def normalizar_descricao(
        self,
        descricao: str
    ):
        """
        Padroniza a descrição.
        Remove espaços extras.

        Exemplo:


        Entrada:

        "  consulta veterinária  "


        Saída:

        "Consulta veterinária"
        """


        return descricao.strip().capitalize()



    # ==================================================
    # CONCLUIR AGENDAMENTO
    # ==================================================

    def concluir(
        self,
        id: int
    ):
        """
        Finaliza um agendamento.


        Regras:

        - Agendamento precisa existir
        - Não pode concluir cancelado
        - Altera status para Concluido


        Exemplo:


        Antes:

        Confirmado


        Depois:

        Concluido
        """


        agendamento = self.buscar_por_id(id)


        if not agendamento:

            raise HTTPException(
                status_code=404,
                detail=
                "Agendamento não encontrado."
            )


        # ==============================================
        # IMPEDIR CONCLUIR CANCELADO
        # ==============================================

        if agendamento.status == "Cancelado":

            raise HTTPException(
                status_code=409,
                detail=
                "Agendamento cancelado não pode ser concluído."
            )


        # ==============================================
        # IMPEDIR CONCLUIR DUAS VEZES
        # ==============================================

        if agendamento.status == "Concluido":

            raise HTTPException(
                status_code=409,
                detail=
                "Agendamento já está concluído."
            )


        # ==============================================
        # ALTERAR STATUS
        # ==============================================

        agendamento.status = "Concluido"


        self.session.commit()

        self.session.refresh(agendamento)


        return agendamento
    
    def deletar(self,id: int):

        agendamento = self.buscar_por_id(id)

        if not agendamento:

            raise HTTPException(
                status_code=404,
                detail="Agendamento não encontrado."
            )


        raise HTTPException(
            status_code=409,
            detail="Agendamentos não podem ser excluídos."
        )