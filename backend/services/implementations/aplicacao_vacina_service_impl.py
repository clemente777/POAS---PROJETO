from datetime import datetime, timedelta

from fastapi import HTTPException

from sqlalchemy import select, func
from sqlalchemy.orm import Session


from backend.models.aplicacao_vacina_model import (
    AplicacoesVacina
)

from backend.models.vacina_model import (
    Vacinas
)

from backend.models.animal_model import (
    Animais
)

from backend.schemas.aplicacao_vacina_schema import (
    AplicacaoVacinaCreate,
    AplicacaoVacinaUpdate
)

from backend.services.interfaces.aplicacao_vacina_service import (
    AplicacaoVacinaService
)


class AplicacaoVacinaServiceImpl(
    AplicacaoVacinaService
):


    def __init__(
        self,
        session: Session
    ):

        self.session = session



    def listar(self):

        return self.session.scalars(

            select(AplicacoesVacina)

            .order_by(
                AplicacoesVacina.data_aplicacao.desc()
            )

        ).all()



    def buscar_por_id(
        self,
        aplicacao_id: int
    ):

        aplicacao = self.session.get(

            AplicacoesVacina,

            aplicacao_id

        )


        if not aplicacao:

            raise HTTPException(

                status_code=404,

                detail="Aplicação de vacina não encontrada."

            )


        return aplicacao



    def listar_por_animal(
        self,
        animal_id: int
    ):

        animal = self.session.get(

            Animais,

            animal_id

        )


        if not animal:

            raise HTTPException(

                status_code=404,

                detail="Animal não encontrado."

            )


        return self.session.scalars(

            select(AplicacoesVacina)

            .where(

                AplicacoesVacina.animal_id == animal_id

            )

            .order_by(

                AplicacoesVacina.data_aplicacao.desc()

            )

        ).all()



    def aplicar_vacina(
        self,
        dados: AplicacaoVacinaCreate,
        veterinario_id: int
    ):


        animal = self.session.get(

            Animais,

            dados.animal_id

        )


        if not animal:

            raise HTTPException(

                status_code=404,

                detail="Animal não encontrado."

            )



        vacina = self.session.get(

            Vacinas,

            dados.vacina_id

        )


        if not vacina:

            raise HTTPException(

                status_code=404,

                detail="Vacina não encontrada."

            )



        aplicacao_existente = self.session.scalar(

            select(AplicacoesVacina)

            .where(

                AplicacoesVacina.animal_id 
                == dados.animal_id

            )

            .where(

                AplicacoesVacina.vacina_id
                == dados.vacina_id

            )

            .where(

                func.date(
                    AplicacoesVacina.data_aplicacao
                )
                ==
                datetime.today().date()

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



        proxima_dose = None


        if vacina.intervalo_dias:

            proxima_dose = (

                datetime.now()

                +
                timedelta(
                    days=vacina.intervalo_dias
                )

            )



        aplicacao = AplicacoesVacina(

            animal_id=dados.animal_id,

            vacina_id=dados.vacina_id,

            veterinario_id=veterinario_id,

            data_aplicacao=datetime.now(),

            lote=dados.lote,

            observacoes=dados.observacoes,

            proxima_dose=proxima_dose

        )



        self.session.add(aplicacao)


        self.session.commit()


        self.session.refresh(aplicacao)


        return aplicacao



    def atualizar(
        self,
        aplicacao_id: int,
        dados: AplicacaoVacinaUpdate
    ):

        aplicacao = self.buscar_por_id(

            aplicacao_id

        )



        if dados.lote is not None:

            aplicacao.lote = dados.lote



        if dados.observacoes is not None:

            aplicacao.observacoes = dados.observacoes



        if dados.proxima_dose is not None:

            aplicacao.proxima_dose = dados.proxima_dose



        self.session.commit()


        self.session.refresh(aplicacao)


        return aplicacao



    def deletar(
        self,
        aplicacao_id: int
    ):


        aplicacao = self.buscar_por_id(

            aplicacao_id

        )


        self.session.delete(

            aplicacao

        )


        self.session.commit()


        return {

            "mensagem":
            "Aplicação de vacina removida com sucesso."

        }