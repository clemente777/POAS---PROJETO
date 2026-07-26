from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session


from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios
from backend.models.atendimento_model import Atendimentos


from backend.schemas.animal_schema import (
    AnimalCreate,
    AnimalUpdate
)



class AnimalServiceImpl:


    def __init__(
        self,
        session: Session,
        usuario_logado: Usuarios
    ):

        self.session = session
        self.usuario_logado = usuario_logado



    # ==========================================================
    # AUXILIAR
    # ==========================================================


    def obter_perfil(self):

        if not self.usuario_logado.perfil:

            return None


        return self.usuario_logado.perfil




    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================


    def normalizar_texto(
        self,
        texto: str
    ):

        if not texto:

            return ""


        return (
            " ".join(
                texto.strip().split()
            )
            .title()
        )



    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================


    def validar_nome(
        self,
        nome: str
    ):

        if not nome:

            return False


        return len(
            nome.strip()
        ) >= 2




    def validar_especie(
        self,
        especie: str
    ):

        if not especie:

            return False


        return len(
            especie.strip()
        ) >= 2




    def validar_raca(
        self,
        raca: str
    ):

        if not raca:

            return False


        return len(
            raca.strip()
        ) >= 2




    def validar_idade(
        self,
        idade: int
    ):

        if idade is None:

            return False


        return 0 <= idade <= 100




    def validar_peso(
        self,
        peso: float | None
    ):

        if peso is None:

            return True


        return (
            peso > 0
            and
            peso <= 300
        )



    # ==========================================================
    # VALIDAR CLIENTE
    # ==========================================================


    def validar_cliente(
        self,
        cliente_id: int
    ):


        cliente = self.session.scalar(

            select(Clientes)
            .where(
                Clientes.id == cliente_id
            )

        )


        if not cliente:


            raise HTTPException(

                status_code=404,

                detail="Cliente não encontrado."

            )


        return cliente




    def validar_campos_obrigatorios(
        self,
        animal: AnimalCreate
    ):


        if not self.validar_nome(
            animal.nome
        ):

            raise HTTPException(
                status_code=400,
                detail="Nome inválido."
            )



        if not self.validar_especie(
            animal.especie
        ):

            raise HTTPException(
                status_code=400,
                detail="Espécie inválida."
            )



        if not self.validar_raca(
            animal.raca
        ):

            raise HTTPException(
                status_code=400,
                detail="Raça inválida."
            )



        if not self.validar_idade(
            animal.idade
        ):

            raise HTTPException(
                status_code=400,
                detail="Idade inválida."
            )



        if hasattr(animal, "peso"):


            if not self.validar_peso(
                animal.peso
            ):


                raise HTTPException(
                    status_code=400,
                    detail="Peso inválido."
                )
        # ==========================================================
    # BUSCAS
    # ==========================================================


    def buscar_animal_por_id(
        self,
        animal_id: int
    ) -> Animais:


        animal = self.session.scalar(

            select(Animais)
            .where(
                Animais.id == animal_id
            )

        )


        if not animal:


            raise HTTPException(

                status_code=404,

                detail="Animal não encontrado."

            )


        return animal




    def buscar_cliente_por_id(
        self,
        cliente_id: int
    ) -> Clientes:


        cliente = self.session.scalar(

            select(Clientes)
            .where(
                Clientes.id == cliente_id
            )

        )


        if not cliente:


            raise HTTPException(

                status_code=404,

                detail="Cliente não encontrado."

            )


        return cliente





    # ==========================================================
    # CONTROLE DE PERMISSÃO
    # ==========================================================


    def verificar_acesso_animal(
        self,
        animal: Animais
    ):


        perfil = self.obter_perfil()



        # Administrador e Veterinário
        # possuem acesso total

        if perfil in [

            "Administrador",

            "Veterinário"

        ]:

            return




        # Cliente somente seus animais

        if perfil == "Cliente":



            cliente = self.session.scalar(

                select(Clientes)
                .where(
                    Clientes.usuario_id
                    ==
                    self.usuario_logado.id
                )

            )



            if not cliente:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Usuário sem cliente vinculado."

                )




            if animal.cliente_id != cliente.id:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Você não possui permissão para acessar este animal."

                )


            return





        raise HTTPException(

            status_code=403,

            detail="Perfil sem permissão."

        )






    # ==========================================================
    # CRIAR ANIMAL
    # ==========================================================


    def criar(
        self,
        animal: AnimalCreate
    ) -> Animais:



        self.validar_campos_obrigatorios(
            animal
        )



        cliente = self.validar_cliente(

            animal.cliente_id

        )



        perfil = self.obter_perfil()



        # Cliente só cria para ele mesmo

        if perfil == "Cliente":



            cliente_usuario = self.session.scalar(

                select(Clientes)
                .where(

                    Clientes.usuario_id
                    ==
                    self.usuario_logado.id

                )

            )



            if not cliente_usuario:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Usuário sem cliente vinculado."

                )



            if cliente_usuario.id != cliente.id:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Você não pode cadastrar animal para outro cliente."

                )





        novo_animal = Animais(


            nome=self.normalizar_texto(

                animal.nome

            ),



            especie=self.normalizar_texto(

                animal.especie

            ),



            raca=self.normalizar_texto(

                animal.raca

            ),



            idade=animal.idade,


            cliente_id=cliente.id

        )




        self.session.add(
            novo_animal
        )


        self.session.commit()


        self.session.refresh(
            novo_animal
        )


        return novo_animal






    # ==========================================================
    # LISTAR ANIMAIS
    # ==========================================================


    def listar(

        self,

        pagina: int = 1,

        limite: int = 10,

        nome: str | None = None,

        ordem: str = "asc"

    ) -> list[Animais]:



        query = select(
            Animais
        )



        perfil = self.obter_perfil()



        # Cliente vê apenas seus animais

        if perfil == "Cliente":



            cliente = self.session.scalar(

                select(Clientes)
                .where(

                    Clientes.usuario_id
                    ==
                    self.usuario_logado.id

                )

            )



            if not cliente:


                raise HTTPException(

                    status_code=403,

                    detail=
                    "Usuário sem cliente vinculado."

                )



            query = query.where(

                Animais.cliente_id
                ==
                cliente.id

            )





        # filtro nome

        if nome:


            query = query.where(

                Animais.nome.ilike(

                    f"%{nome.strip()}%"

                )

            )





        # ordenação

        if ordem.lower() == "desc":


            query = query.order_by(

                desc(
                    Animais.nome
                )

            )


        else:


            query = query.order_by(

                asc(
                    Animais.nome
                )

            )





        # paginação

        if pagina < 1:

            pagina = 1



        if limite < 1:

            limite = 10



        offset = (

            pagina - 1

        ) * limite



        query = (

            query

            .offset(offset)

            .limit(limite)

        )



        return self.session.scalars(
            query
        ).all()
        
        # ==========================================================
    # BUSCAR ANIMAL POR ID
    # ==========================================================


    def buscar_por_id(
        self,
        animal_id: int
    ) -> Animais:


        animal = self.buscar_animal_por_id(
            animal_id
        )


        self.verificar_acesso_animal(
            animal
        )


        return animal






    # ==========================================================
    # ATUALIZAR ANIMAL
    # ==========================================================


    def atualizar(
        self,
        animal_id: int,
        dados: AnimalUpdate
    ) -> Animais:



        animal = self.buscar_animal_por_id(
            animal_id
        )



        self.verificar_acesso_animal(
            animal
        )



        perfil = self.obter_perfil()



        dados_dict = dados.model_dump(
            exclude_unset=True
        )



        # ======================================================
        # ALTERAR CLIENTE DO ANIMAL
        # ======================================================


        if "cliente_id" in dados_dict:



            novo_cliente_id = dados_dict["cliente_id"]



            if novo_cliente_id != animal.cliente_id:



                if perfil == "Cliente":


                    raise HTTPException(

                        status_code=403,

                        detail=
                        "Cliente não pode alterar proprietário do animal."

                    )



                self.validar_cliente(
                    novo_cliente_id
                )



                animal.cliente_id = novo_cliente_id






        # ======================================================
        # ALTERAR NOME
        # ======================================================


        if "nome" in dados_dict:


            if not self.validar_nome(
                dados.nome
            ):


                raise HTTPException(

                    status_code=400,

                    detail="Nome inválido."

                )



            animal.nome = self.normalizar_texto(
                dados.nome
            )






        # ======================================================
        # ALTERAR ESPÉCIE
        # ======================================================


        if "especie" in dados_dict:



            if not self.validar_especie(
                dados.especie
            ):


                raise HTTPException(

                    status_code=400,

                    detail="Espécie inválida."

                )



            animal.especie = self.normalizar_texto(
                dados.especie
            )






        # ======================================================
        # ALTERAR RAÇA
        # ======================================================


        if "raca" in dados_dict:



            if not self.validar_raca(
                dados.raca
            ):


                raise HTTPException(

                    status_code=400,

                    detail="Raça inválida."

                )



            animal.raca = self.normalizar_texto(
                dados.raca
            )






        # ======================================================
        # ALTERAR IDADE
        # ======================================================


        if "idade" in dados_dict:



            if not self.validar_idade(
                dados.idade
            ):


                raise HTTPException(

                    status_code=400,

                    detail="Idade inválida."

                )



            animal.idade = dados.idade






        # ======================================================
        # ALTERAR PESO
        # ======================================================


        if "peso" in dados_dict:



            if not self.validar_peso(
                dados.peso
            ):


                raise HTTPException(

                    status_code=400,

                    detail="Peso inválido."

                )



            animal.peso = dados.peso






        self.session.commit()



        self.session.refresh(
            animal
        )



        return animal






    # ==========================================================
    # DELETAR ANIMAL
    # ==========================================================


    def deletar(
        self,
        animal_id: int
    ):



        animal = self.buscar_animal_por_id(
            animal_id
        )



        self.verificar_acesso_animal(
            animal
        )



        atendimento = self.session.scalar(

            select(Atendimentos)
            .where(

                Atendimentos.animal_id
                ==
                animal.id

            )

        )



        if atendimento:



            raise HTTPException(

                status_code=400,

                detail=
                "Não é possível excluir animal com histórico de atendimento."

            )





        self.session.delete(
            animal
        )



        self.session.commit()



        return {

            "message":
            "Animal removido com sucesso."

        }