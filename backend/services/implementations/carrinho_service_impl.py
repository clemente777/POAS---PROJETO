from backend.models.models import Carrinhos
from backend.services.interfaces.carrinho_service import CarrinhoService


class CarrinhoServiceImpl(CarrinhoService):

    def __init__(self, session):
        self.session = session

    def listar_carrinhos(self):
        return self.session.query(
            Carrinhos
        ).all()

    def buscar_carrinho_por_id(self, id):
        return self.session.query(
            Carrinhos
        ).get(id)

    def criar_carrinho(self, carrinho):

        self.session.add(carrinho)
        self.session.commit()
        self.session.refresh(carrinho)

        return carrinho

    def atualizar_carrinho(self, id, carrinho):

        carrinho_db = self.session.query(
            Carrinhos
        ).get(id)

        if not carrinho_db:
            return None

        self.session.query(
            Carrinhos
        ).filter(
            Carrinhos.id == id
        ).update(
            carrinho.model_dump()
        )

        self.session.commit()

        return carrinho

    def deletar_carrinho(self, id):

        carrinho = self.session.query(
            Carrinhos
        ).get(id)

        if not carrinho:
            return False

        self.session.delete(carrinho)
        self.session.commit()

        return True