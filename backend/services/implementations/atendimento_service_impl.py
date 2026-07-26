from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session
from datetime import datetime, timezone


from backend.models.atendimento_model import Atendimentos
from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios


from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoUpdate
)



class AtendimentoServiceImpl:


    """
    Service responsável pelas regras
    de negócio dos atendimentos.


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


        if hasattr(
            perfil,
            "nome"
        ):

            return perfil.nome


        return perfil





    # ==================================================
    # PERMISSÃO
    # ==================================================


    def validar_permissao(self):

        perfil = self.obter_perfil()


        if perfil not in (
            "Veterinário",
            "Administrador"
        ):


            raise HTTPException(

                status_code=403,

                detail=
                "Sem permissão para gerenciar atendimentos."

            )





    # ==================================================
    # BUSCAR USUÁRIO
    # ==================================================


    def buscar_usuario(
        self,
        usuario_id:int
    ):


        usuario = self.session.scalar(

            select(Usuarios)
            .where(
                Usuarios.id == usuario_id
            )

        )


        if not usuario:


            raise HTTPException(

                status_code=404,

                detail=
                "Usuário não encontrado."

            )


        return usuario





    # ==================================================
    # VALIDAR USUÁRIO ATIVO
    # ==================================================


    def validar_usuario_ativo(
        self,
        usuario:Usuarios
    ):


        if hasattr(
            usuario,
            "ativo"
        ):


            if not usuario.ativo:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Usuário desativado."

                )





    # ==================================================
    # VALIDAR VETERINÁRIO
    # ==================================================


    def validar_veterinario(
        self,
        usuario:Usuarios
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

                detail=
                "Usuário informado não é veterinário."

            )





    # ==================================================
    # BUSCAR ANIMAL
    # ==================================================


    def buscar_animal(
        self,
        animal_id:int
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


        self.validar_acesso_animal(
            animal
        )


        return animal
    
        # ==================================================
    # VALIDAR ACESSO AO ANIMAL
    # ==================================================

    def validar_acesso_animal(
        self,
        animal: Animais
    ):

        perfil = self.obter_perfil()


        # Veterinário e Administrador acessam tudo

        if perfil in (

            "Veterinário",
            "Administrador"

        ):

            return




        # Cliente só acessa seus animais

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
    # BUSCAR ATENDIMENTO POR ID
    # ==================================================

    def buscar_por_id(
        self,
        id:int
    ):


        atendimento = self.session.scalar(

            select(Atendimentos)
            .where(

                Atendimentos.id == id

            )

        )


        if not atendimento:


            raise HTTPException(

                status_code=404,

                detail=
                "Atendimento não encontrado."

            )



        self.buscar_animal(

            atendimento.animal_id

        )



        return atendimento





    # ==================================================
    # VALIDAÇÕES
    # ==================================================


    def validar_diagnostico(
        self,
        diagnostico:str
    ):


        if not diagnostico or not diagnostico.strip():


            raise HTTPException(

                status_code=400,

                detail=
                "Diagnóstico obrigatório."

            )





    def validar_observacoes(
        self,
        observacoes:str | None
    ):


        if observacoes is None:

            return



        if not observacoes.strip():


            raise HTTPException(

                status_code=400,

                detail=
                "Observações inválidas."

            )





    def validar_data(
        self,
        data:datetime
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

                detail=
                "A data do atendimento não pode ser futura."

            )





    def validar_duplicidade(
        self,
        animal_id:int,
        data:datetime
    ):


        existe = self.session.scalar(

            select(Atendimentos)
            .where(

                Atendimentos.animal_id == animal_id,

                Atendimentos.data_atendimento == data

            )

        )


        if existe:


            raise HTTPException(

                status_code=409,

                detail=
                "Já existe atendimento registrado nesta data."

            )





    def validar_finalizado(
        self,
        atendimento: Atendimentos,
        campos: list[str] | None = None
    ):

        if hasattr(
            atendimento,
            "status"
        ):

            if atendimento.status == "Finalizado":

                campos_bloqueados = [
                    "data_atendimento",
                    "usuario_id",
                    "animal_id",
                    "status"
                ]

                if campos:

                    for campo in campos:

                        if campo in campos_bloqueados:

                            raise HTTPException(
                                status_code=409,
                                detail="Atendimento finalizado não pode ser alterado."
                            )

    # ==================================================
    # CRIAR ATENDIMENTO
    # ==================================================

    def criar(
        self,
        atendimento: AtendimentoCreate
    ):


        # somente veterinário/admin

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



        try:


            self.session.add(
                novo
            )


            self.session.commit()



            self.session.refresh(
                novo
            )


            return novo



        except Exception:


            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao criar atendimento."

            )
        # ==================================================
    # LISTAR ATENDIMENTOS
    # ==================================================

    def listar(
        self,
        skip:int = 0,
        limit:int = 10,
        animal_id:int | None = None,
        usuario_id:int | None = None,
        diagnostico:str | None = None,
        data:datetime | None = None,
        sort_by:str = "data_atendimento",
        order:str = "asc"
    ):


        query = select(
            Atendimentos
        )


        perfil = self.obter_perfil()



        # ==============================================
        # CLIENTE VISUALIZA SOMENTE SEUS ANIMAIS
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




        # ==============================================
        # FILTROS
        # ==============================================


        if animal_id is not None:


            query = query.where(

                Atendimentos.animal_id ==
                animal_id

            )



        if usuario_id is not None:


            query = query.where(

                Atendimentos.usuario_id ==
                usuario_id

            )



        if diagnostico:


            query = query.where(

                Atendimentos.diagnostico.ilike(

                    f"%{diagnostico.strip()}%"

                )

            )



        if data:


            query = query.where(

                Atendimentos.data_atendimento ==
                data

            )





        # ==============================================
        # ORDENAÇÃO
        # ==============================================


        campos = {


            "id":

            Atendimentos.id,


            "data_atendimento":

            Atendimentos.data_atendimento,


            "diagnostico":

            Atendimentos.diagnostico,


            "animal_id":

            Atendimentos.animal_id,


            "usuario_id":

            Atendimentos.usuario_id


        }



        coluna = campos.get(

            sort_by,

            Atendimentos.data_atendimento

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
    # ATUALIZAR ATENDIMENTO
    # ==================================================

    def atualizar(
        self,
        id:int,
        atendimento:AtendimentoUpdate
    ):


        self.validar_permissao()


        db = self.buscar_por_id(id)


        dados = atendimento.model_dump(
            exclude_unset=True
        )


        self.validar_finalizado(
            db,
            list(dados.keys())
)


        if "diagnostico" in dados:


            self.validar_diagnostico(

                dados["diagnostico"]

            )


            db.diagnostico = (

                dados["diagnostico"].strip()

            )





        if "observacoes" in dados:


            self.validar_observacoes(

                dados["observacoes"]

            )


            db.observacoes = (

                dados["observacoes"]

            )





        if "data_atendimento" in dados:


            self.validar_data(

                dados["data_atendimento"]

            )


            db.data_atendimento = (

                dados["data_atendimento"]

            )





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





        try:


            self.session.commit()



            self.session.refresh(

                db

            )



            return db




        except Exception:


            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao atualizar atendimento."

            )
        # ==================================================
    # CANCELAR ATENDIMENTO
    # ==================================================

    def cancelar(
        self,
        id:int
    ):


        self.validar_permissao()


        atendimento = self.buscar_por_id(

            id

        )



        if hasattr(
            atendimento,
            "status"
        ):


            if atendimento.status == "Finalizado":


                raise HTTPException(

                    status_code=409,

                    detail=
                    "Não é possível cancelar atendimento finalizado."

                )



            atendimento.status = "Cancelado"



            self.session.commit()



            self.session.refresh(

                atendimento

            )



        return atendimento





    # ==================================================
    # DELETAR ATENDIMENTO
    # ==================================================

    def deletar(
        self,
        id:int
    ):


        self.validar_permissao()



        self.buscar_por_id(

            id

        )



        raise HTTPException(

            status_code=409,

            detail= 
        "Atendimentos não podem ser excluídos. Histórico deve ser preservado."
        )


    


    # ==================================================
    # HISTÓRICO COMPLETO DO ANIMAL
    # ==================================================

    def historico_completo(
        self,
        animal_id:int,
        skip:int = 0,
        limit:int = 10
    ):


        animal = self.buscar_animal(

            animal_id

        )



        atendimentos = self.session.scalars(

            select(Atendimentos)

            .where(

                Atendimentos.animal_id ==
                animal_id

            )

            .order_by(

                desc(

                    Atendimentos.data_atendimento

                )

            )

            .offset(skip)

            .limit(limit)

        ).all()





        historico = []




        for atendimento in atendimentos:


            veterinario = None



            if atendimento.usuario:


                veterinario = (

                    atendimento.usuario.nome

                )




            historico.append({


                "id":

                atendimento.id,



                "data":

                atendimento.data_atendimento,



                "veterinario":

                veterinario,



                "diagnostico":

                atendimento.diagnostico,



                "observacoes":

                atendimento.observacoes



            })







        cliente = animal.cliente




        return {


            "animal": {


                "id":

                animal.id,


                "nome":

                animal.nome,


                "especie":

                animal.especie,


                "raca":

                animal.raca,


                "idade":

                animal.idade


            },



            "cliente": {


                "id":

                cliente.id,


                "nome":

                cliente.nome,


                "telefone":

                cliente.telefone,


                "email":

                cliente.email


            } if cliente else None,



            "paginacao": {


                "skip":

                skip,


                "limit":

                limit,


                "quantidade":

                len(historico)


            },



            "historico":

            historico

        }