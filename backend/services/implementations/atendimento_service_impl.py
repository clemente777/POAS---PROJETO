from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.atendimento_model import Atendimentos
from backend.models.animal_model import Animais
from backend.models.usuario_model import Usuarios

from backend.schemas.atendimento_schema import (
    AtendimentoCreate,
    AtendimentoUpdate
)


class AtendimentoServiceImpl:
    """
    Service responsável pelas regras de negócio
    dos atendimentos veterinários.

    Responsabilidades:

    - Validar atendimento
    - Verificar animal
    - Verificar veterinário
    - Registrar diagnóstico
    - Atualizar informações
    - Manter histórico do animal
    """

    def __init__(self, session: Session):
        """
        Recebe a sessão do banco.

        Usada para:

        - Consultar dados
        - Criar registros
        - Atualizar registros
        """

        self.session = session


    # ==================================================
    # BUSCAS
    # ==================================================

    def buscar_por_id(
        self,
        id: int
    ):
        """
        Busca atendimento pelo ID.

        Retorna:

        - Atendimento encontrado
        - None caso não exista
        """

        return self.session.scalars(
            select(Atendimentos)
            .where(
                Atendimentos.id == id
            )
        ).first()


    def buscar_animal(
        self,
        animal_id: int
    ):
        """
        Busca animal relacionado
        ao atendimento.

        Todo atendimento precisa
        possuir um animal existente.
        """

        return self.session.scalars(
            select(Animais)
            .where(
                Animais.id == animal_id
            )
        ).first()


    def buscar_usuario(
        self,
        usuario_id: int
    ):
        """
        Busca veterinário responsável.

        O atendimento precisa registrar
        quem realizou o procedimento.
        """

        return self.session.scalars(
            select(Usuarios)
            .where(
                Usuarios.id == usuario_id
            )
        ).first()



    # ==================================================
    # VALIDAÇÕES
    # ==================================================

    def validar_diagnostico(
        self,
        diagnostico: str
    ):
        """
        Diagnóstico é obrigatório.
        """

        if not diagnostico.strip():

            raise HTTPException(
                status_code=400,
                detail="Diagnóstico é obrigatório."
            )


    def validar_observacoes(
        self,
        observacoes: str
    ):
        """
        Observações são opcionais.

        Caso sejam enviadas,
        não podem conter apenas espaços.
        """

        if observacoes is not None:

            if observacoes.strip() == "":

                raise HTTPException(
                    status_code=400,
                    detail="Observações inválidas."
                )


    def validar_data(
        self,
        data: datetime
    ):
        """
        Impede atendimento
        com data futura.
        """

        agora = datetime.now()

        if data > agora:

            raise HTTPException(
                status_code=400,
                detail=
                "A data do atendimento não pode ser futura."
            )
        # ==================================================
    # CRIAR ATENDIMENTO
    # ==================================================

    def criar(
        self,
        atendimento: AtendimentoCreate
    ):
        """
        Cria um atendimento veterinário.

        Regras:

        1 - Animal precisa existir
        2 - Veterinário precisa existir
        3 - Diagnóstico obrigatório
        4 - Observações válidas
        """

        # Validar diagnóstico

        self.validar_diagnostico(
            atendimento.diagnostico
        )


        # Validar observações

        self.validar_observacoes(
            atendimento.observacoes
        )


        # Verificar animal

        animal = self.buscar_animal(
            atendimento.animal_id
        )


        if not animal:

            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )


        # Verificar veterinário

        usuario = self.buscar_usuario(
            atendimento.usuario_id
        )


        if not usuario:

            raise HTTPException(
                status_code=404,
                detail="Veterinário não encontrado."
            )


        # Criar atendimento

        db = Atendimentos(
            **atendimento.model_dump()
        )


        # Salvar

        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db



    # ==================================================
    # LISTAR ATENDIMENTOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        animal_id: int | None = None,
        usuario_id: int | None = None,
        diagnostico: str | None = None,
        data: datetime | None = None,
        sort_by: str = "data_atendimento",
        order: str = "asc",
    ):
        """
        Lista atendimentos.

        Recursos:

        - Paginação
        - Filtro por animal
        - Filtro por veterinário
        - Filtro por diagnóstico
        - Filtro por data
        - Ordenação
        """

        query = select(Atendimentos)



        # ==================================================
        # FILTROS
        # ==================================================

        if animal_id is not None:

            query = query.where(
                Atendimentos.animal_id == animal_id
            )


        if usuario_id is not None:

            query = query.where(
                Atendimentos.usuario_id == usuario_id
            )


        if diagnostico:

            query = query.where(
                Atendimentos.diagnostico.ilike(
                    f"%{diagnostico}%"
                )
            )


        if data:

            query = query.where(
                Atendimentos.data_atendimento == data
            )



        # ==================================================
        # ORDENAÇÃO
        # ==================================================

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



        # ==================================================
        # PAGINAÇÃO
        # ==================================================

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
        id: int,
        atendimento: AtendimentoUpdate
    ):
        """
        Atualiza informações
        de um atendimento.

        Permite alterar:

        - Diagnóstico
        - Observações

        Não altera:

        - Animal
        - Veterinário
        - Data
        """

        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Atendimento não encontrado."
            )


        dados = atendimento.model_dump(
            exclude_unset=True
        )


        # Validar diagnóstico

        if "diagnostico" in dados:

            self.validar_diagnostico(
                dados["diagnostico"]
            )


        # Validar observações

        if "observacoes" in dados:

            self.validar_observacoes(
                dados["observacoes"]
            )


        # Aplicar alterações

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
    # DELETE BLOQUEADO
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        """
        Atendimentos não devem
        ser removidos.

        Motivo:

        O histórico veterinário
        precisa ser preservado.
        """

        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Atendimento não encontrado."
            )


        raise HTTPException(
            status_code=409,
            detail=
            "Atendimentos não podem ser excluídos. "
            "O histórico deve ser preservado."
        )



    # ==================================================
    # HISTÓRICO COMPLETO DO ANIMAL
    # ==================================================

    def historico_completo(
        self,
        animal_id: int
    ):
        """
        Retorna todo histórico
        veterinário do animal.

        Inclui:

        - Dados do animal
        - Dados do cliente
        - Atendimentos
        - Veterinário
        - Diagnósticos
        """

        animal = self.session.get(
            Animais,
            animal_id
        )


        if animal is None:

            return None


        cliente = animal.cliente


        atendimentos = (
            self.session.query(
                Atendimentos
            )
            .filter(
                Atendimentos.animal_id == animal_id
            )
            .order_by(
                Atendimentos.data_atendimento.desc()
            )
            .all()
        )


        historico = []


        for atendimento in atendimentos:

            veterinario = None


            if atendimento.usuario:

                veterinario = (
                    atendimento.usuario.nome
                )


            historico.append({

                "data":
                atendimento.data_atendimento,

                "veterinario":
                veterinario,

                "diagnostico":
                atendimento.diagnostico,

                "observacoes":
                atendimento.observacoes
            })


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
            },


            "historico":
            historico
        }