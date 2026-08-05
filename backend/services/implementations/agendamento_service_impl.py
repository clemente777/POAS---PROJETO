from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from datetime import datetime, timezone


from backend.models.agendamento_model import Agendamentos
from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios


from backend.schemas.agendamento_schema import (
    AgendamentoCreate,
    AgendamentoUpdate
)



class AgendamentoServiceImpl:

    """
    Service responsável pelas regras
    de negócio dos agendamentos.

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
        session: Session,
        usuario_logado: Usuarios
    ):

        self.session = session
        self.usuario_logado = usuario_logado



    # ==================================================
    # PERFIL
    # ==================================================


    def obter_perfil(self):

        perfil = self.usuario_logado.perfil


        if hasattr(perfil, "nome"):

            return perfil.nome


        return perfil




    # ==================================================
    # VERIFICAR ACESSO AO ANIMAL
    # ==================================================


    def verificar_acesso_animal(
        self,
        animal: Animais
    ):

        perfil = self.obter_perfil()



        if perfil in [

            "Administrador",
            "Veterinário"

        ]:

            return




        if perfil == "Cliente":


            cliente = self.session.scalar(

                select(Clientes)
                .where(
                    Clientes.usuario_id ==
                    self.usuario_logado.id
                )

            )


            if not cliente:

                raise HTTPException(

                    status_code=403,

                    detail=
                    "Usuário não possui cliente vinculado."

                )



            if animal.cliente_id != cliente.id:

                raise HTTPException(

                    status_code=403,

                    detail=
                    "Você não possui acesso a este animal."

                )


            return




        raise HTTPException(

            status_code=403,

            detail=
            "Perfil sem permissão."

        )





    # ==================================================
    # BUSCAS
    # ==================================================


    def buscar_animal(
        self,
        animal_id: int
    ):


        animal = self.session.scalar(

            select(Animais)
            .where(
                Animais.id == animal_id
            )

        )



        if not animal:

            raise HTTPException(

                status_code=404,

                detail=
                "Animal não encontrado."

            )



        self.verificar_acesso_animal(

            animal

        )


        return animal





    def buscar_por_id(
        self,
        id: int
    ):


        agendamento = self.session.scalar(

            select(Agendamentos)
            .where(
                Agendamentos.id == id
            )

        )



        if not agendamento:


            raise HTTPException(

                status_code=404,

                detail=
                "Agendamento não encontrado."

            )



        self.verificar_acesso_animal(

            agendamento.animal

        )



        return agendamento
    
        # ==================================================
    # VALIDAÇÕES
    # ==================================================


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

                detail=
                "Não é permitido agendamento em data passada."

            )




    def validar_status(
        self,
        status: str
    ):


        if status not in self.STATUS_VALIDOS:


            raise HTTPException(

                status_code=400,

                detail=
                "Status inválido."

            )




    def validar_descricao(
        self,
        descricao: str
    ):


        if not descricao:

            raise HTTPException(

                status_code=400,

                detail=
                "Descrição obrigatória."

            )



        descricao = descricao.strip()



        if not descricao:


            raise HTTPException(

                status_code=400,

                detail=
                "Descrição inválida."

            )



        if len(descricao) < 5:


            raise HTTPException(

                status_code=400,

                detail=
                "Descrição deve possuir no mínimo 5 caracteres."

            )




    def validar_conflito_horario(
        self,
        animal_id: int,
        data: datetime,
        agendamento_id: int | None = None
    ):


        query = select(
            Agendamentos
        ).where(

            Agendamentos.animal_id == animal_id,

            Agendamentos.data_agendamento == data,

            Agendamentos.status != "Cancelado"

        )



        if agendamento_id:


            query = query.where(

                Agendamentos.id != agendamento_id

            )



        existe = self.session.scalar(
            query
        )



        if existe:


            raise HTTPException(

                status_code=409,

                detail=
                "Já existe agendamento para este animal neste horário."

            )





    # ==================================================
    # CRIAR AGENDAMENTO
    # ==================================================


    def criar(
        self,
        agendamento: AgendamentoCreate
    ):


        self.buscar_animal(

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


        if self.obter_perfil() == "Veterinário":

            dados["veterinario_id"] = self.usuario_logado.id


        novo = Agendamentos(
            **dados,
            status="Pendente"
        )


        try:


            self.session.add(
                novo
            )


            self.session.commit()



            self.session.refresh(
                novo
            )



            return novo



        except Exception as e:

            self.session.rollback()

            print("ERRO AO CRIAR AGENDAMENTO:", e)

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    def atribuir_veterinario(
    self,
    id: int,
    veterinario_id: int
):

        agendamento = self.buscar_por_id(id)


        veterinario = self.session.scalar(
            select(Usuarios)
            .where(
                Usuarios.id == veterinario_id
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
                detail="Usuário informado não é veterinário."
            )


        agendamento.veterinario_id = veterinario_id


        self.session.commit()

        self.session.refresh(
            agendamento
        )


        return agendamento



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
        order: str = "asc"
    ):


        query = select(
            Agendamentos
        )



        perfil = self.obter_perfil()



        # ==============================================
        # CLIENTE SÓ VISUALIZA SEUS ANIMAIS
        # ==============================================


        if perfil == "Cliente":


            cliente = self.session.scalar(

                select(Clientes)
                .where(
                    Clientes.usuario_id ==
                    self.usuario_logado.id
                )

            )



            if not cliente:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Cliente não encontrado."

                )



            query = (

                query

                .join(
                    Animais
                )

                .where(

                    Animais.cliente_id ==
                    cliente.id

                )

            )




        if animal_id is not None:


            query = query.where(

                Agendamentos.animal_id ==
                animal_id

            )





        if status:


            self.validar_status(
                status
            )


            query = query.where(

                Agendamentos.status ==
                status

            )




        if descricao:


            query = query.where(

                Agendamentos.descricao.ilike(

                    f"%{descricao.strip()}%"

                )

            )




        if data:


            query = query.where(

                Agendamentos.data_agendamento ==
                data

            )




        campos = {


            "id":
            Agendamentos.id,


            "data_agendamento":
            Agendamentos.data_agendamento,


            "descricao":
            Agendamentos.descricao,


            "status":
            Agendamentos.status,


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




        if skip < 0:

            skip = 0



        if limit <= 0:

            limit = 10



        if limit > 100:

            limit = 100




        query = (

            query

            .offset(skip)

            .limit(limit)

        )



        return self.session.scalars(

            query

        ).all()
    
        # ==================================================
    # ATUALIZAR AGENDAMENTO
    # ==================================================


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

                detail=
                "Nenhum dado informado para atualização."

            )





        if "data_agendamento" in valores:


            self.validar_data(

                valores["data_agendamento"]

            )



            self.validar_conflito_horario(

                agendamento.animal_id,

                valores["data_agendamento"],

                agendamento.id

            )





        if "descricao" in valores:


            self.validar_descricao(

                valores["descricao"]

            )





        if "status" in valores:


            self.validar_status(

                valores["status"]

            )





        campos_permitidos = [

            "data_agendamento",

            "descricao",

            "status"

        ]




        try:


            for campo, valor in valores.items():


                if campo in campos_permitidos:


                    setattr(

                        agendamento,

                        campo,

                        valor

                    )



            self.session.commit()



            self.session.refresh(

                agendamento

            )



            return agendamento




        except Exception:


            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao atualizar agendamento."

            )






        # ==================================================
    # CANCELAR AGENDAMENTO
    # ==================================================

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

                detail=
                "Não é possível cancelar atendimento finalizado."

            )


        if agendamento.status == "Cancelado":

            raise HTTPException(

                status_code=409,

                detail=
                "Agendamento já está cancelado."

            )


        agendamento.status = "Cancelado"


        self.session.commit()


        self.session.refresh(
            agendamento
        )


        return agendamento



    # ==================================================
    # DELETAR AGENDAMENTO
    # BLOQUEADO
    # ==================================================

    def deletar(
        self,
        id: int
    ):

        self.buscar_por_id(
            id
        )


        raise HTTPException(

            status_code=409,

            detail=
            "Agendamentos não podem ser excluídos. Utilize o cancelamento."

        )