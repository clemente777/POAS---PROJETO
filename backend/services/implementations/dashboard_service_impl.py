from datetime import date

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


class DashboardServiceImpl:

    def __init__(self, session: Session):
        self.session = session


    def _total(self, model):

        return self.session.scalar(
            select(func.count())
            .select_from(model)
        )


    def _valor_estoque(self):

        resultado = self.session.scalar(
            select(
                func.sum(
                    Produtos.preco * Produtos.estoque
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
        )



    def _produtos_sem_estoque(self):

        return self.session.scalar(
            select(func.count())
            .select_from(Produtos)
            .where(
                Produtos.estoque == 0
            )
        )



    def _produto_mais_caro(self):

        produto = self.session.scalar(
            select(Produtos)
            .order_by(
                desc(Produtos.preco)
            )
            .limit(1)
        )

        if not produto:
            return None


        return {
            "nome": produto.nome,
            "preco": produto.preco
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
            "nome": produto.nome,
            "preco": produto.preco
        }



    def _animal_mais_velho(self):

        animal = self.session.scalar(
            select(Animais)
            .order_by(
                desc(Animais.idade)
            )
            .limit(1)
        )


        if not animal:
            return None


        return {
            "nome": animal.nome,
            "idade": animal.idade
        }



    def _media_idade_animais(self):

        resultado = self.session.scalar(
            select(
                func.avg(Animais.idade)
            )
        )

        return round(resultado, 2) if resultado else 0



    def _agendamentos_hoje(self):

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                func.date(
                    Agendamentos.data_agendamento
                ) == date.today()
            )
        )



    def _agendamentos_futuros(self):

        return self.session.scalar(
            select(func.count())
            .select_from(Agendamentos)
            .where(
                Agendamentos.data_agendamento >= date.today()
            )
        )

    def _agendamentos_semana(self):

            resultado = self.session.execute(

                select(
                    func.date(
                        Agendamentos.data_agendamento
                    ).label("dia"),

                    func.count(
                        Agendamentos.id
                    ).label("quantidade")
                )

                .where(
                    Agendamentos.data_agendamento >= date.today()
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
                    "dia": str(item.dia),
                    "quantidade": item.quantidade
                }

                for item in resultado

            ]

    def _cliente_com_mais_animais(self):

        resultado = self.session.execute(
            select(
                Clientes.nome,
                func.count(Animais.id)
                .label("quantidade")
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
            "nome": resultado.nome,
            "quantidade": resultado.quantidade
        }

    def _usuarios_por_perfil(self, perfil: str):

        return self.session.scalar(

            select(func.count())
            .select_from(Usuarios)
            .where(
                Usuarios.perfil == perfil
            )

        ) or 0
    def _animais_por_especie(self):

        resultado = self.session.execute(

            select(
                Animais.especie,
                func.count(Animais.id).label("quantidade")
            )

            .group_by(
                Animais.especie
            )

        ).all()


        return {

            item.especie: item.quantidade

            for item in resultado

        }
    def dashboard(self):

        return {

            # Totais

            "usuarios": self._total(Usuarios),
            
            "administradores":
                self._usuarios_por_perfil("Administrador"),

            "veterinarios":
                self._usuarios_por_perfil("Veterinário"),

            "clientes_sistema":
                self._usuarios_por_perfil("Cliente"),

            "clientes": self._total(Clientes),

            "animais": self._total(Animais),

            "agendamentos": self._total(Agendamentos),

            "atendimentos": self._total(Atendimentos),

            "produtos": self._total(Produtos),

            "carrinhos": self._total(Carrinhos),

            "itens_carrinho": self._total(ItensCarrinho),


            # Estoque

            "valor_total_estoque":
                self._valor_estoque(),

            "estoque_baixo":
                self._estoque_baixo(),

            "produtos_sem_estoque":
                self._produtos_sem_estoque(),


            # Produtos

            "produto_mais_caro":
                self._produto_mais_caro(),

            "produto_mais_barato":
                self._produto_mais_barato(),


            # Animais

            "animal_mais_velho":
                self._animal_mais_velho(),

            "media_idade_animais":
                self._media_idade_animais(),

            "animais_por_especie":
                self._animais_por_especie(),
                
            # Clientes

            "cliente_com_mais_animais":
                self._cliente_com_mais_animais(),


            # Agenda

            "agendamentos_hoje":
                self._agendamentos_hoje(),

            "agendamentos_futuros":
                self._agendamentos_futuros(),

            "agendamentos_semana":
                self._agendamentos_semana()

}