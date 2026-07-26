from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.carrinho_model import Carrinhos
from backend.models.cliente_model import Clientes

from backend.schemas.carrinho_schema import (
    CarrinhoCreate,
    CarrinhoUpdate
)


class CarrinhoServiceImpl:


    """
    Service responsável pelas regras
    de negócio do carrinho.


    Regras:

    - Cliente possui apenas um carrinho.
    - Cliente só acessa seu próprio carrinho.
    - Administrador possui acesso total.
    - Carrinho vazio não finaliza compra.
    - Produto sem estoque bloqueia compra.
    - Carrinho com itens não pode ser excluído.
    """



    def __init__(
        self,
        session: Session,
        usuario_logado
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





    def is_admin(self):

        return (
            self.obter_perfil()
            ==
            "Administrador"
        )






    # ==================================================
    # BUSCAR CARRINHO
    # ==================================================


    def buscar_por_id(
        self,
        id: int
    ):


        carrinho = self.session.scalar(

            select(Carrinhos)
            .where(
                Carrinhos.id == id
            )

        )


        if not carrinho:


            raise HTTPException(

                status_code=404,

                detail="Carrinho não encontrado"

            )



        self.validar_proprietario(

            carrinho

        )



        return carrinho






    def buscar_por_cliente(
        self,
        cliente_id: int
    ):


        return self.session.scalar(

            select(Carrinhos)

            .where(

                Carrinhos.cliente_id
                ==
                cliente_id

            )

        )







    def validar_cliente(
        self,
        cliente_id: int
    ):


        cliente = self.session.scalar(

            select(Clientes)

            .where(

                Clientes.id
                ==
                cliente_id

            )

        )


        if not cliente:


            raise HTTPException(

                status_code=404,

                detail="Cliente não encontrado."

            )


        return cliente







    # ==================================================
    # REGRA DE PROPRIEDADE
    # ==================================================


    def validar_proprietario(
        self,
        carrinho: Carrinhos
    ):



        if self.is_admin():

            return





        if not carrinho.cliente:


            raise HTTPException(

                status_code=404,

                detail="Cliente do carrinho não encontrado."

            )





        if carrinho.cliente.usuario_id != self.usuario_logado.id:


            raise HTTPException(

                status_code=403,

                detail=
                "Você não possui acesso a este carrinho."

            )
    
    
    # ==================================================
    # CRIAR CARRINHO
    # ==================================================

    def criar(
        self,
        carrinho: CarrinhoCreate
    ):


        cliente = self.validar_cliente(

            carrinho.cliente_id

        )



        if not self.is_admin():


            if cliente.usuario_id != self.usuario_logado.id:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Você só pode criar seu próprio carrinho."

                )




        existente = self.buscar_por_cliente(

            carrinho.cliente_id

        )



        if existente:


            raise HTTPException(

                status_code=409,

                detail=
                "Cliente já possui um carrinho."

            )




        novo = Carrinhos(

            **carrinho.model_dump()

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
                "Erro ao criar carrinho."

            )







    # ==================================================
    # LISTAR CARRINHOS
    # ==================================================

    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        cliente_id: int | None = None,
        data_criacao: datetime | None = None,
        sort_by: str = "data_criacao",
        order: str = "desc"
    ):


        query = select(
            Carrinhos
        )



        if not self.is_admin():


            query = (

                query

                .join(
                    Clientes,
                    Carrinhos.cliente_id ==
                    Clientes.id
                )

                .where(

                    Clientes.usuario_id ==
                    self.usuario_logado.id

                )

            )


        else:


            if cliente_id is not None:


                query = query.where(

                    Carrinhos.cliente_id ==
                    cliente_id

                )






        if data_criacao:


            query = query.where(

                Carrinhos.data_criacao ==
                data_criacao

            )






        campos = {


            "id":
            Carrinhos.id,


            "cliente_id":
            Carrinhos.cliente_id,


            "data_criacao":
            Carrinhos.data_criacao


        }





        coluna = campos.get(

            sort_by,

            Carrinhos.data_criacao

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
    # ATUALIZAR CARRINHO
    # ==================================================

    def atualizar(
        self,
        id: int,
        carrinho: CarrinhoUpdate
    ):


        db = self.buscar_por_id(

            id

        )



        dados = carrinho.model_dump(

            exclude_unset=True

        )




        if "cliente_id" in dados:



            cliente = self.validar_cliente(

                dados["cliente_id"]

            )




            if not self.is_admin():



                if cliente.usuario_id != self.usuario_logado.id:



                    raise HTTPException(

                        status_code=403,

                        detail=
                        "Você não pode transferir este carrinho."

                    )






            outro = self.buscar_por_cliente(

                dados["cliente_id"]

            )




            if outro and outro.id != id:



                raise HTTPException(

                    status_code=409,

                    detail=
                    "Cliente já possui outro carrinho."

                )







        try:


            for campo, valor in dados.items():


                setattr(

                    db,

                    campo,

                    valor

                )





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
                "Erro ao atualizar carrinho."

            )
    
    # ==================================================
    # DELETAR CARRINHO
    # ==================================================

    def deletar(
        self,
        id: int
    ):


        carrinho = self.buscar_por_id(

            id

        )



        if carrinho.itens:


            raise HTTPException(

                status_code=409,

                detail=
                "Carrinho possui itens. Remova os produtos antes."

            )




        try:


            self.session.delete(

                carrinho

            )


            self.session.commit()



            return True





        except Exception:


            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao excluir carrinho."

            )







    # ==================================================
    # FINALIZAR COMPRA
    # ==================================================

    def finalizar_compra(
        self,
        carrinho_id: int
    ):


        """
        Finaliza a compra do carrinho.


        Regras:

        - Usuário deve ser dono do carrinho.
        - Administrador pode finalizar qualquer carrinho.
        - Carrinho não pode estar vazio.
        - Produto precisa ter estoque.
        - Estoque é reduzido.
        - Itens são removidos após compra.
        """



        carrinho = self.buscar_por_id(

            carrinho_id

        )




        if not carrinho.itens:


            raise HTTPException(

                status_code=400,

                detail=
                "Carrinho vazio."

            )





        valor_total = 0

        quantidade_itens = 0





        try:




            # ==========================================
            # VALIDAR ESTOQUE
            # ==========================================


            for item in carrinho.itens:


                produto = item.produto




                if produto.estoque < item.quantidade:



                    raise HTTPException(

                        status_code=409,

                        detail=(

                            f"Estoque insuficiente "
                            f"para {produto.nome}."

                        )

                    )








            # ==========================================
            # ATUALIZAR ESTOQUE
            # ==========================================


            for item in carrinho.itens:



                produto = item.produto



                produto.estoque -= item.quantidade




                valor_total += (

                    produto.preco *

                    item.quantidade

                )




                quantidade_itens += (

                    item.quantidade

                )







            # ==========================================
            # REMOVER ITENS
            # ==========================================


            for item in list(carrinho.itens):


                self.session.delete(

                    item

                )







            self.session.commit()






        except HTTPException:


            self.session.rollback()


            raise






        except Exception:



            self.session.rollback()



            raise HTTPException(

                status_code=500,

                detail=
                "Erro ao finalizar compra."

            )







        return {


            "mensagem":

            "Compra finalizada com sucesso.",



            "valor_total":

            valor_total,



            "quantidade_itens":

            quantidade_itens


        }