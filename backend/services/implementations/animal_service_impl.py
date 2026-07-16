from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.schemas.animal_schema import (
    AnimalCreate,
    AnimalUpdate
)


class AnimalServiceImpl:
    """
    Service responsável pelas regras de negócio
    dos animais.

    Responsabilidades:

    - Validar dados do animal
    - Verificar cliente dono
    - Cadastrar animais
    - Atualizar informações
    - Listar com filtros
    - Aplicar paginação
    - Remover animais seguindo regras
    """

    def __init__(self, session: Session):
        """
        Recebe a sessão do banco.

        Usada para:

        - Consultas
        - Inserções
        - Atualizações
        - Exclusões
        """

        self.session = session


    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    def normalizar_texto(self, texto: str):
        """
        Remove espaços extras
        e padroniza texto.

        Exemplo:

        Entrada:

        "   cachorro   "

        Saída:

        "Cachorro"
        """

        if not texto:
            return ""

        return texto.strip().capitalize()


    # ==================================================
    # VALIDAÇÕES
    # ==================================================

    def validar_idade(self, idade: int):
        """
        Valida idade do animal.

        Regras:

        - Não aceita idade negativa
        - Limite máximo de 100 anos
        """

        if idade < 0:
            return False

        if idade > 100:
            return False

        return True


    def validar_campos_obrigatorios(self, animal):
        """
        Valida campos obrigatórios.

        Obrigatórios:

        - Nome
        - Espécie
        - Raça
        """

        if not animal.nome.strip():
            raise HTTPException(
                status_code=400,
                detail="Nome do animal é obrigatório."
            )

        if not animal.especie.strip():
            raise HTTPException(
                status_code=400,
                detail="Espécie é obrigatória."
            )

        if not animal.raca.strip():
            raise HTTPException(
                status_code=400,
                detail="Raça é obrigatória."
            )


    # ==================================================
    # BUSCAS
    # ==================================================

    def buscar_por_id(self, id: int):
        """
        Busca animal pelo ID.

        Retorna:

        - Animal encontrado
        - None caso não exista
        """

        return self.session.scalars(
            select(Animais)
            .where(
                Animais.id == id
            )
        ).first()


    def buscar_cliente(self, id: int):
        """
        Busca cliente dono do animal.

        Um animal precisa
        obrigatoriamente possuir
        um cliente existente.
        """

        return self.session.scalars(
            select(Clientes)
            .where(
                Clientes.id == id
            )
        ).first()
    
        # ==================================================
    # CRIAR ANIMAL
    # ==================================================

    def criar(self, animal: AnimalCreate):
        """
        Cadastra um novo animal.

        Regras:

        1 - Nome obrigatório
        2 - Espécie obrigatória
        3 - Raça obrigatória
        4 - Idade válida
        5 - Cliente dono precisa existir
        6 - Dados normalizados antes de salvar
        """

        # Validar campos obrigatórios

        self.validar_campos_obrigatorios(
            animal
        )


        # Validar idade

        if not self.validar_idade(
            animal.idade
        ):

            raise HTTPException(
                status_code=400,
                detail="Idade inválida."
            )


        # Verificar cliente

        cliente = self.buscar_cliente(
            animal.cliente_id
        )


        if not cliente:

            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )


        # Normalizar dados

        dados = animal.model_dump()


        dados["nome"] = self.normalizar_texto(
            dados["nome"]
        )

        dados["especie"] = self.normalizar_texto(
            dados["especie"]
        )

        dados["raca"] = self.normalizar_texto(
            dados["raca"]
        )


        # Criar objeto

        db = Animais(
            **dados
        )


        # Salvar

        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db



    # ==================================================
    # LISTAR ANIMAIS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        especie: str | None = None,
        raca: str | None = None,
        idade: int | None = None,
        cliente_id: int | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):
        """
        Lista animais cadastrados.

        Recursos:

        - Paginação
        - Filtro por nome
        - Filtro por espécie
        - Filtro por raça
        - Filtro por idade
        - Filtro por cliente
        - Ordenação


        Exemplo:

        GET /animais?

        especie=Cachorro

        limit=5
        """


        query = select(Animais)



        # ==================================================
        # FILTROS
        # ==================================================

        if nome:

            query = query.where(
                Animais.nome.ilike(
                    f"%{nome}%"
                )
            )


        if especie:

            query = query.where(
                Animais.especie.ilike(
                    f"%{especie}%"
                )
            )


        if raca:

            query = query.where(
                Animais.raca.ilike(
                    f"%{raca}%"
                )
            )


        if idade is not None:

            query = query.where(
                Animais.idade == idade
            )


        if cliente_id is not None:

            query = query.where(
                Animais.cliente_id == cliente_id
            )



        # ==================================================
        # ORDENAÇÃO
        # ==================================================

        campos = {

            "id":
            Animais.id,

            "nome":
            Animais.nome,

            "especie":
            Animais.especie,

            "raca":
            Animais.raca,

            "idade":
            Animais.idade,

            "cliente_id":
            Animais.cliente_id

        }


        coluna = campos.get(
            sort_by,
            Animais.id
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
    # ATUALIZAR ANIMAL
    # ==================================================

    def atualizar(
        self,
        id: int,
        animal: AnimalUpdate
    ):
        """
        Atualiza os dados de um animal.

        Permite atualização parcial.

        Exemplo:

        Enviado:

        {
            "idade": 5
        }


        Apenas a idade será alterada.
        """

        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )


        dados = animal.model_dump(
            exclude_unset=True
        )



        # ==================================================
        # VALIDAR CAMPOS VAZIOS
        # ==================================================

        for campo, valor in dados.items():

            if isinstance(valor, str):

                if not valor.strip():

                    raise HTTPException(
                        status_code=400,
                        detail=f"{campo} não pode ser vazio."
                    )



        # ==================================================
        # VALIDAR IDADE
        # ==================================================

        if "idade" in dados:

            if not self.validar_idade(
                dados["idade"]
            ):

                raise HTTPException(
                    status_code=400,
                    detail="Idade inválida."
                )



        # ==================================================
        # NORMALIZAR TEXTOS
        # ==================================================

        campos_texto = [

            "nome",

            "especie",

            "raca"

        ]


        for campo in campos_texto:

            if campo in dados:

                dados[campo] = (
                    self.normalizar_texto(
                        dados[campo]
                    )
                )



        # ==================================================
        # APLICAR ALTERAÇÕES
        # ==================================================

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
    # DELETAR ANIMAL
    # ==================================================

    def deletar(
        self,
        id: int
    ):
        """
        Remove um animal.

        Regras:

        - Animal precisa existir
        - Animal com histórico de atendimento
          não pode ser removido
        """


        db = self.buscar_por_id(id)


        if not db:

            raise HTTPException(
                status_code=404,
                detail="Animal não encontrado."
            )



        # ==================================================
        # VERIFICAR HISTÓRICO
        # ==================================================

        if db.atendimentos:

            raise HTTPException(
                status_code=409,
                detail=
                "Animal possui histórico de atendimento."
            )



        # ==================================================
        # REMOVER
        # ==================================================

        self.session.delete(db)

        self.session.commit()


        return {
            "message":
            "Animal removido com sucesso."
        }