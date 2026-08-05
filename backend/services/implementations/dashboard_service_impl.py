from datetime import date, datetime

from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session


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



class DashboardServiceImpl:


    def __init__(
        self,
        session: Session,
        usuario: Usuarios | None = None
    ):

        self.session = session
        self.usuario = usuario



    # ============================================
    # MÉTODO GENÉRICO
    # ============================================

    def _total(self, model):

        return self.session.scalar(

            select(func.count())

            .select_from(model)

        ) or 0



    # ============================================
    # USUÁRIOS
    # ============================================

    def _usuarios_por_perfil(self, perfil):

        return self.session.scalar(

            select(func.count())

            .select_from(Usuarios)

            .where(

                Usuarios.perfil == perfil

            )

        ) or 0


    # ============================================
    # ATENDIMENTOS
    # ============================================

    def _atendimentos_hoje(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Atendimentos)

            .where(

                func.date(
                    Atendimentos.data_atendimento
                ) == date.today()

            )

        ) or 0


    def _atendimentos_finalizados(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Atendimentos)

            .where(

                Atendimentos.status == "Finalizado"

            )

        ) or 0
    # ============================================
    # ANIMAIS
    # ============================================


    def _animais_por_especie(self):

        resultado = self.session.execute(

            select(

                Animais.especie,

                func.count(
                    Animais.id
                ).label("quantidade")

            )

            .group_by(
                Animais.especie
            )

        ).all()



        return {

            item.especie:
            item.quantidade

            for item in resultado

        }




    def _animal_mais_velho(self):

        animal = self.session.scalar(

            select(Animais)

            .order_by(
                desc(
                    Animais.idade
                )
            )

            .limit(1)

        )


        if not animal:

            return None



        return {

            "nome":
                animal.nome,

            "idade":
                animal.idade

        }




    def _media_idade_animais(self):


        resultado = self.session.scalar(

            select(
                func.avg(
                    Animais.idade
                )
            )

        )


        return round(
            resultado,
            2
        ) if resultado else 0






    # ============================================
    # CLIENTES
    # ============================================



    def _cliente_com_mais_animais(self):


        resultado = self.session.execute(

            select(

                Clientes.nome,

                func.count(
                    Animais.id
                ).label(
                    "quantidade"
                )

            )

            .join(

                Animais,

                Animais.cliente_id == Clientes.id

            )

            .group_by(
                Clientes.id
            )

            .order_by(
                desc("quantidade")
            )

            .limit(1)


        ).first()



        if not resultado:

            return None



        return {

            "nome":
                resultado.nome,


            "quantidade":
                resultado.quantidade

        }
        # ============================================
    # ESTOQUE
    # ============================================


    def _valor_estoque(self):

        resultado = self.session.scalar(

            select(

                func.sum(

                    Produtos.preco *
                    Produtos.estoque

                )

            )

        )


        return resultado or 0




    def _estoque_baixo(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Produtos)

            .where(

                Produtos.estoque <= 5

            )

        ) or 0





    def _produtos_sem_estoque(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Produtos)

            .where(

                Produtos.estoque == 0

            )

        ) or 0





    def _produto_mais_caro(self):

        produto = self.session.scalar(

            select(Produtos)

            .order_by(

                desc(
                    Produtos.preco
                )

            )

            .limit(1)

        )


        if not produto:

            return None



        return {

            "nome":
                produto.nome,


            "preco":
                produto.preco

        }





    def _produto_mais_barato(self):

        produto = self.session.scalar(

            select(Produtos)

            .order_by(

                Produtos.preco

            )

            .limit(1)

        )


        if not produto:

            return None



        return {

            "nome":
                produto.nome,


            "preco":
                produto.preco

        }






    # ============================================
    # AGENDA
    # ============================================



    def _agendamentos_hoje(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Agendamentos)

            .where(

                func.date(

                    Agendamentos.data_agendamento

                )

                ==
                date.today()

            )

        ) or 0





    def _agendamentos_futuros(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Agendamentos)

            .where(

                Agendamentos.data_agendamento
                >=
                date.today()

            )

        ) or 0





    def _agendamentos_cancelados(self):

        return self.session.scalar(

            select(func.count())

            .select_from(Agendamentos)

            .where(

                Agendamentos.status
                ==
                "Cancelado"

            )

        ) or 0





    def _agendamentos_semana(self):


        resultado = self.session.execute(

            select(

                func.date(

                    Agendamentos.data_agendamento

                )
                .label("dia"),


                func.count(

                    Agendamentos.id

                )
                .label("quantidade")

            )

            .where(

                Agendamentos.data_agendamento
                >=
                date.today()

            )


            .group_by(

                func.date(

                    Agendamentos.data_agendamento

                )

            )


            .order_by(

                func.date(

                    Agendamentos.data_agendamento

                )

            )


        ).all()



        return [

            {

                "dia":
                    str(item.dia),


                "quantidade":
                    item.quantidade

            }


            for item in resultado

        ]







    # ============================================
    # VACINAS
    # ============================================



    def _proximas_doses(self):

        return self.session.scalar(

            select(func.count())

            .select_from(
                AplicacoesVacina
            )

            .where(

                AplicacoesVacina.proxima_dose
                >=
                date.today()

            )

        ) or 0





    def _vacinas_aplicadas_veterinario(
        self,
        veterinario_id
    ):


        return self.session.scalar(

            select(func.count())

            .select_from(
                AplicacoesVacina
            )

            .where(

                AplicacoesVacina.veterinario_id
                ==
                veterinario_id

            )

        ) or 0





    def _vacina_mais_aplicada(self):


        resultado = self.session.execute(

            select(

                Vacinas.nome,

                func.count(

                    AplicacoesVacina.id

                )
                .label(
                    "quantidade"
                )

            )


            .join(

                AplicacoesVacina,

                AplicacoesVacina.vacina_id
                ==
                Vacinas.id

            )


            .group_by(

                Vacinas.id

            )


            .order_by(

                desc(
                    "quantidade"
                )

            )


            .limit(1)


        ).first()



        if not resultado:

            return None



        return {

            "nome":
                resultado.nome,


            "quantidade":
                resultado.quantidade

        }
        
    # ============================================
    # DADOS COMPARTILHADOS
    # ADMIN + VETERINÁRIO
    # ============================================


    def dados_compartilhados(self):

        return {


            # ===============================
            # ANIMAIS
            # ===============================


            "animais":

                self._total(
                    Animais
                ),



            "animais_por_especie":

                self._animais_por_especie(),




            "animal_mais_velho":

                self._animal_mais_velho(),




            "media_idade_animais":

                self._media_idade_animais(),




            # ===============================
            # CLIENTES
            # ===============================


            "clientes":

                self._total(
                    Clientes
                ),




            "cliente_com_mais_animais":

                self._cliente_com_mais_animais(),





            # ===============================
            # AGENDA
            # ===============================


            "agendamentos":

                self._total(
                    Agendamentos
                ),




            "agendamentos_semana":

                self._agendamentos_semana(),





            # ===============================
            # VACINAS
            # ===============================


            "vacinas":

                self._total(
                    Vacinas
                ),





            "aplicacoes_vacina":

                self._total(
                    AplicacoesVacina
                ),



            "proximas_doses":

                self._proximas_doses()



        }






    # ============================================
    # DASHBOARD ADMINISTRADOR
    # ============================================


    def dashboard_admin(self):


        dados = self.dados_compartilhados()



        return {


            **dados,



            # ===============================
            # USUÁRIOS
            # ===============================


            "usuarios":

                self._total(
                    Usuarios
                ),




            "administradores":

                self._usuarios_por_perfil(
                    "Administrador"
                ),




            "veterinarios":

                self._usuarios_por_perfil(
                    "Veterinário"
                ),




            "clientes_sistema":

                self._usuarios_por_perfil(
                    "Cliente"
                ),





            # ===============================
            # CADASTROS
            # ===============================


            "produtos":

                self._total(
                    Produtos
                ),




            "carrinhos":

                self._total(
                    Carrinhos
                ),




            "itens_carrinho":

                self._total(
                    ItensCarrinho
                ),






            # ===============================
            # ESTOQUE
            # ===============================


            "valor_total_estoque":

                self._valor_estoque(),




            "estoque_baixo":

                self._estoque_baixo(),




            "produtos_sem_estoque":

                self._produtos_sem_estoque(),





            # ===============================
            # PRODUTOS
            # ===============================


            "produto_mais_caro":

                self._produto_mais_caro(),




            "produto_mais_barato":

                self._produto_mais_barato(),





            # ===============================
            # AGENDA
            # ===============================


            "agendamentos_hoje":

                self._agendamentos_hoje(),




            "agendamentos_futuros":

                self._agendamentos_futuros(),





            "agendamentos_cancelados":

                self._agendamentos_cancelados(),






            # ===============================
            # ATENDIMENTOS
            # ===============================


            "atendimentos":

                self._total(
                    Atendimentos
                ),




            "atendimentos_hoje":

                self._atendimentos_hoje(),




            "atendimentos_finalizados":

                self._atendimentos_finalizados(),




            "vacina_mais_aplicada":

                self._vacina_mais_aplicada()

        }
        
    # ============================================
    # CONSULTAS DO VETERINÁRIO
    # ============================================

    def _consultas_hoje_veterinario(self, veterinario_id):

        return self.session.scalar(

            select(func.count())

            .select_from(Agendamentos)

            .where(

                Agendamentos.veterinario_id == veterinario_id,

                func.date(
                    Agendamentos.data_agendamento
                ) == date.today()

            )

        ) or 0


    def _proximas_consultas_veterinario(self, veterinario_id):

        return self.session.scalar(

            select(func.count())

            .select_from(Agendamentos)

            .where(

                Agendamentos.veterinario_id == veterinario_id,

                Agendamentos.data_agendamento >= datetime.now()

            )

        ) or 0


    # ============================================
    # ATENDIMENTOS DO VETERINÁRIO
    # ============================================

    def _atendimentos_realizados_veterinario(self, veterinario_id):

        return self.session.scalar(

            select(func.count())

            .select_from(Atendimentos)

            .where(

                Atendimentos.usuario_id == veterinario_id

            )

        ) or 0


    def _animais_atendidos_veterinario(self, veterinario_id):

        return self.session.scalar(

            select(

                func.count(
                    func.distinct(
                        Atendimentos.animal_id
                    )
                )

            )

            .where(

                Atendimentos.usuario_id == veterinario_id

            )

        ) or 0   
    # ============================================
    # DASHBOARD VETERINÁRIO
    # ============================================


    def dashboard_veterinario(self):


        veterinario_id = self.usuario.id



        # Dados que qualquer veterinário pode visualizar

        dados = self.dados_compartilhados()



        return {


            **dados,



            # =================================
            # DADOS EXCLUSIVOS DO VETERINÁRIO
            # =================================



            "consultas_hoje":

                self._consultas_hoje_veterinario(
                    veterinario_id
                ),




            "proximas_consultas":

                self._proximas_consultas_veterinario(
                    veterinario_id
                ),




            "atendimentos_realizados":

                self._atendimentos_realizados_veterinario(
                    veterinario_id
                ),




            "animais_atendidos":

                self._animais_atendidos_veterinario(
                    veterinario_id
                ),




            "vacinas_aplicadas":

                self._vacinas_aplicadas_veterinario(
                    veterinario_id
                )



        }