from fastapi import HTTPException

from backend.models.animal_model import Animais
from backend.models.cliente_model import Clientes
from backend.models.usuario_model import Usuarios

from backend.schemas.animal_schema import (
    AnimalCreate,
    AnimalUpdate
)

from backend.repositories.animal_repository import (
    AnimalRepository
)


class AnimalServiceImpl:

    def __init__(
        self,
        repository: AnimalRepository,
        usuario_logado: Usuarios
    ):

        self.repository = repository
        self.usuario_logado = usuario_logado

    # ==========================================================
    # AUXILIAR
    # ==========================================================

    def obter_perfil(self):

        return self.usuario_logado.perfil

    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================

    def normalizar_texto(
        self,
        texto: str
    ) -> str:

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
    ) -> bool:

        if not nome:
            return False

        return len(nome.strip()) >= 2

    def validar_especie(
        self,
        especie: str
    ) -> bool:

        if not especie:
            return False

        return len(especie.strip()) >= 2

    def validar_raca(
        self,
        raca: str
    ) -> bool:

        if not raca:
            return False

        return len(raca.strip()) >= 2

    def validar_idade(
        self,
        idade: int
    ) -> bool:

        if idade is None:
            return False

        return 0 <= idade <= 100

    # ==========================================================
    # VALIDAÇÃO DOS CAMPOS
    # ==========================================================

    def validar_campos_obrigatorios(
        self,
        animal: AnimalCreate
    ) -> None:

        if not self.validar_nome(animal.nome):

            raise HTTPException(
                status_code=400,
                detail="Nome inválido."
            )

        if not self.validar_especie(animal.especie):

            raise HTTPException(
                status_code=400,
                detail="Espécie inválida."
            )

        if not self.validar_raca(animal.raca):

            raise HTTPException(
                status_code=400,
                detail="Raça inválida."
            )

        if not self.validar_idade(animal.idade):

            raise HTTPException(
                status_code=400,
                detail="Idade inválida."
            )

    # ==========================================================
    # BUSCAS
    # ==========================================================

    def buscar_animal_por_id(
        self,
        animal_id: int
    ) -> Animais:

        animal = self.repository.buscar_por_id(
            animal_id
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

        cliente = self.repository.buscar_cliente_por_id(
            cliente_id
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
    ) -> None:

        perfil = self.obter_perfil()

        # Administrador e Veterinário
        # possuem acesso total.

        if perfil in [
            "Administrador",
            "Veterinário"
        ]:

            return

        # Cliente somente acessa seus próprios animais.

        if perfil == "Cliente":

            cliente = (
                self.repository
                .buscar_cliente_por_usuario_id(
                    self.usuario_logado.id
                )
            )

            if not cliente:

                raise HTTPException(
                    status_code=403,
                    detail="Usuário sem cliente vinculado."
                )

            if animal.cliente_id != cliente.id:

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Você não possui permissão "
                        "para acessar este animal."
                    )
                )

            return

        raise HTTPException(
            status_code=403,
            detail="Perfil sem permissão."
        )

    # ==========================================================
    # CRIAR
    # ==========================================================

    def criar(
        self,
        animal: AnimalCreate
    ) -> Animais:

        self.validar_campos_obrigatorios(
            animal
        )

        cliente = self.buscar_cliente_por_id(
            animal.cliente_id
        )

        perfil = self.obter_perfil()

        # Cliente só pode cadastrar animal para si mesmo.

        if perfil == "Cliente":

            cliente_usuario = (
                self.repository
                .buscar_cliente_por_usuario_id(
                    self.usuario_logado.id
                )
            )

            if not cliente_usuario:

                raise HTTPException(
                    status_code=403,
                    detail="Usuário sem cliente vinculado."
                )

            if cliente_usuario.id != cliente.id:

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Você não pode cadastrar animal "
                        "para outro cliente."
                    )
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

        return self.repository.criar(
            novo_animal
        )

    # ==========================================================
    # LISTAR
    # ==========================================================

    def listar(
        self,
        pagina: int = 1,
        limite: int = 10,
        nome: str | None = None,
        ordem: str = "asc"
    ) -> list[Animais]:

        perfil = self.obter_perfil()

        # Corrige paginação inválida.

        if pagina < 1:
            pagina = 1

        if limite < 1:
            limite = 10

        cliente_id = None

        # Cliente só pode visualizar seus animais.

        if perfil == "Cliente":

            cliente = (
                self.repository
                .buscar_cliente_por_usuario_id(
                    self.usuario_logado.id
                )
            )

            if not cliente:

                raise HTTPException(
                    status_code=403,
                    detail="Usuário sem cliente vinculado."
                )

            cliente_id = cliente.id

        elif perfil not in [
            "Administrador",
            "Veterinário"
        ]:

            raise HTTPException(
                status_code=403,
                detail="Perfil sem permissão."
            )

        return self.repository.listar(
            pagina=pagina,
            limite=limite,
            nome=nome,
            ordem=ordem,
            cliente_id=cliente_id
        )

    # ==========================================================
    # BUSCAR POR ID
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
    # ATUALIZAR
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

        dados_dict = dados.model_dump(
            exclude_unset=True
        )

        # ------------------------------------------------------
        # NOME
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # ESPÉCIE
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # RAÇA
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # IDADE
        # ------------------------------------------------------

        if "idade" in dados_dict:

            if not self.validar_idade(
                dados.idade
            ):

                raise HTTPException(
                    status_code=400,
                    detail="Idade inválida."
                )

            animal.idade = dados.idade

        return self.repository.atualizar(
            animal
        )

    # ==========================================================
    # DELETAR
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

        possui_atendimento = (
            self.repository
            .possui_atendimento(
                animal.id
            )
        )

        if possui_atendimento:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Não é possível excluir animal "
                    "com histórico de atendimento."
                )
            )

        self.repository.deletar(
            animal
        )

        return {
            "message": "Animal removido com sucesso."
        }