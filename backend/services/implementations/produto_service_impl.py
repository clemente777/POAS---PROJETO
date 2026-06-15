from backend.models.models import Produtos
from backend.services.interfaces.produto_service import ProdutoService


class ProdutoServiceImpl(ProdutoService):

    def __init__(self, session):
        self.session = session

    def listar_produtos(self):
        return self.session.query(Produtos).all()

    def buscar_produto_por_id(self, id):
        return self.session.query(Produtos).get(id)

    def criar_produto(self, produto):
        self.session.add(produto)
        self.session.commit()
        self.session.refresh(produto)

        return produto

    def atualizar_produto(self, id, produto):

        produto_db = self.session.query(
            Produtos
        ).get(id)

        if not produto_db:
            return None

        self.session.query(Produtos).filter(
            Produtos.id == id
        ).update(produto.model_dump())

        self.session.commit()

        return produto

    def deletar_produto(self, id):

        produto = self.session.query(
            Produtos
        ).get(id)

        if not produto:
            return False

        self.session.delete(produto)
        self.session.commit()

        return True