from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from backend.models.cliente_model import Clientes
from backend.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate
)


class ClienteServiceImpl:
    """
    Service responsável pelas regras de negócio
    relacionadas aos clientes.
    """

    def __init__(
        self,
        session: Session
    ):
        self.session = session


    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    def normalizar_cpf(
        self,
        cpf: str
    ):

        if not cpf:
            return ""

        return (
            cpf
            .replace(".", "")
            .replace("-", "")
            .strip()
        )


    def normalizar_email(
        self,
        email: str
    ):

        if not email:
            return ""

        return email.lower().strip()



    # ==================================================
    # VALIDAÇÕES
    # ==================================================

    def validar_cpf(
        self,
        cpf: str
    ):

        cpf = self.normalizar_cpf(cpf)


        if len(cpf) != 11:
            return False


        if cpf == cpf[0] * 11:
            return False


        soma = sum(
            int(cpf[i]) * (10 - i)
            for i in range(9)
        )


        resto = soma % 11


        digito1 = (
            0
            if resto < 2
            else 11 - resto
        )


        soma = sum(
            int(cpf[i]) * (11 - i)
            for i in range(10)
        )


        resto = soma % 11


        digito2 = (
            0
            if resto < 2
            else 11 - resto
        )


        return (
            int(cpf[9]) == digito1
            and
            int(cpf[10]) == digito2
        )



    def validar_telefone(
        self,
        telefone: str
    ):

        if not telefone:
            return False


        numeros = (
            telefone
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )


        return (
            numeros.isdigit()
            and len(numeros) in [10, 11]
        )



    # ==================================================
    # BUSCAS
    # ==================================================

    def buscar_por_cpf(
        self,
        cpf: str
    ):

        cpf = self.normalizar_cpf(cpf)


        return self.session.scalars(
            select(Clientes)
            .where(
                Clientes.cpf == cpf
            )
        ).first()



    def buscar_por_email(
        self,
        email: str
    ):

        email = self.normalizar_email(email)


        return self.session.scalars(
            select(Clientes)
            .where(
                Clientes.email == email
            )
        ).first()



    def buscar_por_id(
        self,
        id: int
    ):

        return self.session.scalars(
            select(Clientes)
            .where(
                Clientes.id == id
            )
        ).first()



    # ==================================================
    # CRIAR CLIENTE
    # ==================================================

    def criar(
        self,
        cliente: ClienteCreate
    ):

        cpf = self.normalizar_cpf(
            cliente.cpf
        )


        email = self.normalizar_email(
            cliente.email
        )


        if not cliente.nome.strip():

            raise HTTPException(
                status_code=400,
                detail="Nome é obrigatório."
            )


        if not cpf:

            raise HTTPException(
                status_code=400,
                detail="CPF é obrigatório."
            )


        if not self.validar_cpf(cpf):

            raise HTTPException(
                status_code=400,
                detail="CPF inválido."
            )


        if not self.validar_telefone(
            cliente.telefone
        ):

            raise HTTPException(
                status_code=400,
                detail="Telefone inválido."
            )


        if not cliente.endereco.strip():

            raise HTTPException(
                status_code=400,
                detail="Endereço é obrigatório."
            )


        if self.buscar_por_cpf(cpf):

            raise HTTPException(
                status_code=409,
                detail="CPF já cadastrado."
            )


        if self.buscar_por_email(email):

            raise HTTPException(
                status_code=409,
                detail="Email já cadastrado."
            )


        dados = cliente.model_dump()


        dados["cpf"] = cpf
        dados["email"] = email


        db = Clientes(
            **dados
        )


        self.session.add(db)

        self.session.commit()

        self.session.refresh(db)


        return db



    # ==================================================
    # LISTAR CLIENTES
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        cpf: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        sort_by: str = "id",
        order: str = "asc",
    ):


        query = select(Clientes)



        if nome:

            query = query.where(
                Clientes.nome.ilike(
                    f"%{nome}%"
                )
            )


        if cpf:

            query = query.where(
                Clientes.cpf.ilike(
                    f"%{cpf}%"
                )
            )


        if telefone:

            query = query.where(
                Clientes.telefone.ilike(
                    f"%{telefone}%"
                )
            )


        if email:

            query = query.where(
                Clientes.email.ilike(
                    f"%{email}%"
                )
            )



        campos = {

            "id": Clientes.id,

            "nome": Clientes.nome,

            "cpf": Clientes.cpf,

            "telefone": Clientes.telefone,

            "email": Clientes.email
        }


        coluna = campos.get(
            sort_by,
            Clientes.id
        )


        if order.lower() == "desc":

            query = query.order_by(
                desc(coluna)
            )

        else:

            query = query.order_by(
                asc(coluna)
            )


        query = (
            query
            .offset(skip)
            .limit(limit)
        )


        return self.session.scalars(query).all()



    # ==================================================
    # ATUALIZAR CLIENTE
    # ==================================================

    def atualizar(
        self,
        id: int,
        cliente: ClienteUpdate
    ):

        db_cliente = self.buscar_por_id(id)


        if not db_cliente:
            return None


        dados = cliente.model_dump(
            exclude_unset=True
        )


        if "cpf" in dados:

            dados["cpf"] = self.normalizar_cpf(
                dados["cpf"]
            )


        if "email" in dados:

            dados["email"] = self.normalizar_email(
                dados["email"]
            )


        for campo, valor in dados.items():

            setattr(
                db_cliente,
                campo,
                valor
            )


        self.session.commit()

        self.session.refresh(db_cliente)


        return db_cliente



    # ==================================================
    # DELETAR CLIENTE
    # ==================================================

    def deletar(
        self,
        id: int
    ):

        cliente = self.buscar_por_id(id)


        if not cliente:
            return False


        self.session.delete(cliente)

        self.session.commit()


        return True