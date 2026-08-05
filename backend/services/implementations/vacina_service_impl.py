from sqlalchemy import func

from backend.models.aplicacao_vacina_model import (
    AplicacoesVacina
)
from fastapi import HTTPException

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models.aplicacao_vacina_model import AplicacoesVacina
from backend.models.vacina_model import Vacinas

from backend.schemas.vacina_schema import (
    VacinaCreate,
    VacinaUpdate
)

from backend.services.interfaces.vacina_service import (
    VacinaService
)


class VacinaServiceImpl(VacinaService):

    def __init__(self, session: Session):
        self.session = session

    def listar(self):

        return self.session.scalars(
            select(Vacinas)
            .order_by(Vacinas.nome)
        ).all()

    def buscar_por_id(self, vacina_id: int):

        vacina = self.session.get(
            Vacinas,
            vacina_id
        )

        if not vacina:
            raise HTTPException(
                status_code=404,
                detail="Vacina não encontrada."
            )

        return vacina

    def buscar_por_nome(self, nome: str):

        return self.session.scalars(

            select(Vacinas)

            .where(
                Vacinas.nome.ilike(f"%{nome}%")
            )

            .order_by(
                Vacinas.nome
            )

        ).all()

    def cadastrar(
        self,
        dados: VacinaCreate
    ):

        vacina_existente = self.session.scalar(

            select(Vacinas)

            .where(
                func.lower(Vacinas.nome)
                == dados.nome.lower()
            )

        )

        if vacina_existente:

            raise HTTPException(
                status_code=400,
                detail="Já existe uma vacina cadastrada com esse nome."
            )

        vacina = Vacinas(

            nome=dados.nome,

            fabricante=dados.fabricante,

            quantidade_doses=dados.quantidade_doses,

            intervalo_dias=dados.intervalo_dias,

            descricao=dados.descricao

        )

        self.session.add(vacina)

        self.session.commit()

        self.session.refresh(vacina)

        return vacina

    def atualizar(
        self,
        vacina_id: int,
        dados: VacinaUpdate
    ):

        vacina = self.buscar_por_id(
            vacina_id
        )

        if dados.nome is not None:

            vacina_existente = self.session.scalar(

                select(Vacinas)

                .where(
                    func.lower(Vacinas.nome)
                    == dados.nome.lower()
                )

                .where(
                    Vacinas.id != vacina.id
                )

            )

            if vacina_existente:

                raise HTTPException(
                    status_code=400,
                    detail="Já existe uma vacina cadastrada com esse nome."
                )

            vacina.nome = dados.nome

        if dados.fabricante is not None:
            vacina.fabricante = dados.fabricante

        if dados.quantidade_doses is not None:
            vacina.quantidade_doses = dados.quantidade_doses

        if dados.intervalo_dias is not None:
            vacina.intervalo_dias = dados.intervalo_dias

        if dados.descricao is not None:
            vacina.descricao = dados.descricao

        self.session.commit()

        self.session.refresh(vacina)

        return vacina

    def deletar(
        self,
        vacina_id: int
    ):

        vacina = self.buscar_por_id(
            vacina_id
        )

        quantidade_aplicacoes = self.session.scalar(

            select(func.count())

            .select_from(AplicacoesVacina)

            .where(
                AplicacoesVacina.vacina_id == vacina.id
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

        self.session.delete(vacina)

        self.session.commit()

        return {
            "mensagem": "Vacina removida com sucesso."
        }