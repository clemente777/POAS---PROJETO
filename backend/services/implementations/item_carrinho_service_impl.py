from backend.models.models import ItensCarrinho
from backend.services.interfaces.item_carrinho_service import (
    ItemCarrinhoService
)


class ItemCarrinhoServiceImpl(
    ItemCarrinhoService
):

    def __init__(self, session):
        self.session = session

    def listar_itens(self):
        return self.session.query(
            ItensCarrinho
        ).all()

    def buscar_item_por_id(self, id):
        return self.session.query(
            ItensCarrinho
        ).get(id)

    def criar_item(self, item):

        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)

        return item

    def atualizar_item(self, id, item):

        item_db = self.session.query(
            ItensCarrinho
        ).get(id)

        if not item_db:
            return None

        self.session.query(
            ItensCarrinho
        ).filter(
            ItensCarrinho.id == id
        ).update(
            item.model_dump()
        )

        self.session.commit()

        return item

    def deletar_item(self, id):

        item = self.session.query(
            ItensCarrinho
        ).get(id)

        if not item:
            return False

        self.session.delete(item)
        self.session.commit()

        return True