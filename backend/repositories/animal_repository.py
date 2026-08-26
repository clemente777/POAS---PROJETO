from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.animal_model import Animais
from backend.models.atendimento_model import Atendimentos
from backend.models.cliente_model import Clientes


class AnimalRepository:

    def __init__(self, session: Session):
        self.session = session

    # ==========================================================
    # ANIMAL
    # ==========================================================

    def buscar_por_id(self, animal_id: int) -> Animais | None:

        return self.session.scalar(
            select(Animais)
            .where(
                Animais.id == animal_id
            )
        )

    def listar(
        self,
        pagina: int = 1,
        limite: int = 10,
        nome: str | None = None,
        ordem: str = "asc",
        cliente_id: int | None = None
    ) -> list[Animais]:

        query = select(Animais)

        # Filtro por cliente
        if cliente_id is not None:

            query = query.where(
                Animais.cliente_id == cliente_id
            )

        # Filtro por nome
        if nome:

            query = query.where(
                Animais.nome.ilike(
                    f"%{nome.strip()}%"
                )
            )

        # Ordenação
        if ordem.lower() == "desc":

            query = query.order_by(
                desc(Animais.nome)
            )

        else:

            query = query.order_by(
                asc(Animais.nome)
            )

        # Paginação
        offset = (pagina - 1) * limite

        query = (
            query
            .offset(offset)
            .limit(limite)
        )

        return self.session.scalars(
            query
        ).all()

    # ==========================================================
    # CLIENTE
    # ==========================================================

    def buscar_cliente_por_id(
        self,
        cliente_id: int
    ) -> Clientes | None:

        return self.session.scalar(
            select(Clientes)
            .where(
                Clientes.id == cliente_id
            )
        )

    def buscar_cliente_por_usuario_id(
        self,
        usuario_id: int
    ) -> Clientes | None:

        return self.session.scalar(
            select(Clientes)
            .where(
                Clientes.usuario_id == usuario_id
            )
        )

    # ==========================================================
    # ATENDIMENTO
    # ==========================================================

    def possui_atendimento(
        self,
        animal_id: int
    ) -> bool:

        atendimento = self.session.scalar(
            select(Atendimentos.id)
            .where(
                Atendimentos.animal_id == animal_id
            )
            .limit(1)
        )

        return atendimento is not None

    # ==========================================================
    # PERSISTÊNCIA
    # ==========================================================

    def criar(
        self,
        animal: Animais
    ) -> Animais:

        self.session.add(animal)

        self.session.commit()

        self.session.refresh(animal)

        return animal

    def atualizar(
        self,
        animal: Animais
    ) -> Animais:

        self.session.commit()

        self.session.refresh(animal)

        return animal

    def deletar(
        self,
        animal: Animais
    ) -> None:

        self.session.delete(animal)

        self.session.commit()