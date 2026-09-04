from backend.models.usuario_model import Usuarios
from backend.models.cliente_model import Clientes
from backend.models.animal_model import Animais
from backend.models.agendamento_model import Agendamentos
from backend.models.atendimento_model import Atendimentos
from backend.models.produto_model import Produtos
from backend.models.carrinho_model import Carrinhos
from backend.models.item_carrinho_model import ItensCarrinho
from backend.models.aplicacao_vacina_model import AplicacoesVacina
from backend.models.vacina_model import Vacinas

from backend.repositories.dashboard_repository import DashboardRepository


class DashboardServiceImpl:

    def __init__(
        self,
        session,
        usuario: Usuarios | None = None
    ):

        self.usuario = usuario
        self.repository = DashboardRepository(session=session)

    # ============================================
    # HELPERS DE FORMATAÇÃO
    # ============================================

    def _formatar_animal(self, animal):

        if not animal:
            return None

        return {
            "nome": animal.nome,
            "idade": animal.idade
        }

    def _formatar_cliente_com_mais_animais(self, resultado):

        if not resultado:
            return None

        return {
            "nome": resultado.nome,
            "quantidade": resultado.quantidade
        }

    def _formatar_produto(self, produto):

        if not produto:
            return None

        return {
            "nome": produto.nome,
            "preco": produto.preco
        }

    def _formatar_vacina_mais_aplicada(self, resultado):

        if not resultado:
            return None

        return {
            "nome": resultado.nome,
            "quantidade": resultado.quantidade
        }

    def _formatar_animais_por_especie(self, resultado):

        return {
            item.especie: item.quantidade
            for item in resultado
        }

    def _formatar_agendamentos_semana(self, resultado):

        return [
            {
                "dia": str(item.dia),
                "quantidade": item.quantidade
            }
            for item in resultado
        ]

    def _formatar_media_idade(self, media):

        return round(media, 2) if media else 0

    # ============================================
    # DADOS COMPARTILHADOS
    # ADMIN + VETERINÁRIO
    # ============================================

    def dados_compartilhados(self):

        return {

            # ANIMAIS
            "animais": self.repository.total(Animais),

            "animais_por_especie": self._formatar_animais_por_especie(
                self.repository.animais_por_especie()
            ),

            "animal_mais_velho": self._formatar_animal(
                self.repository.animal_mais_velho()
            ),

            "media_idade_animais": self._formatar_media_idade(
                self.repository.media_idade_animais()
            ),

            # CLIENTES
            "clientes": self.repository.total(Clientes),

            "cliente_com_mais_animais": self._formatar_cliente_com_mais_animais(
                self.repository.cliente_com_mais_animais()
            ),

            # AGENDA
            "agendamentos": self.repository.total(Agendamentos),

            "agendamentos_semana": self._formatar_agendamentos_semana(
                self.repository.agendamentos_semana()
            ),

            # VACINAS
            "vacinas": self.repository.total(Vacinas),

            "aplicacoes_vacina": self.repository.total(AplicacoesVacina),

            "proximas_doses": self.repository.proximas_doses()

        }

    # ============================================
    # DASHBOARD ADMINISTRADOR
    # ============================================

    def dashboard_admin(self):

        dados = self.dados_compartilhados()

        return {

            **dados,

            # USUÁRIOS
            "usuarios": self.repository.total(Usuarios),

            "administradores": self.repository.usuarios_por_perfil(
                "Administrador"
            ),

            "veterinarios": self.repository.usuarios_por_perfil(
                "Veterinário"
            ),

            "clientes_sistema": self.repository.usuarios_por_perfil(
                "Cliente"
            ),

            # CADASTROS
            "produtos": self.repository.total(Produtos),

            "carrinhos": self.repository.total(Carrinhos),

            "itens_carrinho": self.repository.total(ItensCarrinho),

            # ESTOQUE
            "valor_total_estoque": self.repository.valor_estoque(),

            "estoque_baixo": self.repository.estoque_baixo(),

            "produtos_sem_estoque": self.repository.produtos_sem_estoque(),

            # PRODUTOS
            "produto_mais_caro": self._formatar_produto(
                self.repository.produto_mais_caro()
            ),

            "produto_mais_barato": self._formatar_produto(
                self.repository.produto_mais_barato()
            ),

            # AGENDA
            "agendamentos_hoje": self.repository.agendamentos_hoje(),

            "agendamentos_futuros": self.repository.agendamentos_futuros(),

            "agendamentos_cancelados": self.repository.agendamentos_cancelados(),

            # ATENDIMENTOS
            "atendimentos": self.repository.total(Atendimentos),

            "atendimentos_hoje": self.repository.atendimentos_hoje(),

            "atendimentos_finalizados": self.repository.atendimentos_finalizados(),

            "vacina_mais_aplicada": self._formatar_vacina_mais_aplicada(
                self.repository.vacina_mais_aplicada()
            )

        }

    # ============================================
    # DASHBOARD VETERINÁRIO
    # ============================================

    def dashboard_veterinario(self):

        veterinario_id = self.usuario.id

        # Dados que qualquer veterinário pode visualizar
        dados = self.dados_compartilhados()

        return {

            **dados,

            # DADOS EXCLUSIVOS DO VETERINÁRIO
            "consultas_hoje": self.repository.consultas_hoje_veterinario(
                veterinario_id
            ),

            "proximas_consultas": self.repository.proximas_consultas_veterinario(
                veterinario_id
            ),

            "atendimentos_realizados":
                self.repository.atendimentos_realizados_veterinario(
                    veterinario_id
                ),

            "animais_atendidos": self.repository.animais_atendidos_veterinario(
                veterinario_id
            ),

            "vacinas_aplicadas": self.repository.vacinas_aplicadas_veterinario(
                veterinario_id
            )

        }

    # ============================================
    # DASHBOARD CLIENTE
    # ============================================

    def _formatar_proxima_consulta(self, resultado):

        if not resultado:
            return None

        return {
            "data": resultado.data_agendamento.isoformat(),
            "descricao": resultado.descricao,
            "animal": resultado.animal_nome
        }

    def dashboard_cliente(self):

        cliente = self.repository.cliente_por_usuario_id(self.usuario.id)

        if not cliente:

            return {
                "meus_animais": [],
                "total_animais": 0,
                "consultas_agendadas": 0,
                "proxima_consulta": None,
                "consultas_realizadas": 0,
                "compras": 0,
                "valor_total_compras": 0,
                "proximas_doses_vacina": 0
            }

        animais = [
            self._formatar_animal(animal)
            for animal in self.repository.animais_do_cliente(cliente.id)
        ]

        return {

            "meus_animais": animais,

            "total_animais": len(animais),

            "consultas_agendadas": self.repository.consultas_agendadas_cliente(
                cliente.id
            ),

            "proxima_consulta": self._formatar_proxima_consulta(
                self.repository.proxima_consulta_cliente(cliente.id)
            ),

            "consultas_realizadas":
                self.repository.atendimentos_realizados_cliente(cliente.id),

            "compras": self.repository.total_carrinhos_cliente(cliente.id),

            "valor_total_compras":
                self.repository.valor_total_compras_cliente(cliente.id),

            "proximas_doses_vacina": self.repository.proximas_doses_cliente(
                cliente.id
            )

        }