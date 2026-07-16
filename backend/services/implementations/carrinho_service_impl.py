from sqlalchemy import select, asc, desc
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.carrinho_model import Carrinhos
from backend.schemas.carrinho_schema import CarrinhoCreate, CarrinhoUpdate
from backend.models.item_carrinho_model import ItensCarrinho


class CarrinhoServiceImpl:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def criar(self, carrinho: CarrinhoCreate):

        db = Carrinhos(**carrinho.model_dump())

        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)

        return db



# LIST
    def listar(
        self,
        skip: int = 0,
        limit: int = 10,
        cliente_id: int | None = None,
        data_criacao: datetime | None = None,
        sort_by: str = "data_criacao",
        order: str = "desc",
    ):

        query = select(Carrinhos)

        # ==========================
        # FILTROS
        # ==========================

        if cliente_id is not None:
            query = query.where(
                Carrinhos.cliente_id == cliente_id
            )

        if data_criacao:
            query = query.where(
                Carrinhos.data_criacao == data_criacao
            )

        # ==========================
        # ORDENAÇÃO
        # ==========================

        campos = {
            "id": Carrinhos.id,
            "data_criacao": Carrinhos.data_criacao,
            "cliente_id": Carrinhos.cliente_id,
        }

        coluna = campos.get(
            sort_by,
            Carrinhos.data_criacao
        )

        if order.lower() == "desc":
            query = query.order_by(desc(coluna))
        else:
            query = query.order_by(asc(coluna))

    # ==========================
    # PAGINAÇÃO
    # ==========================

        query = query.offset(skip).limit(limit)

        return self.session.scalars(query).all()

    # GET BY ID
    def buscar_por_id(self, id: int):
        return self.session.scalars(
            select(Carrinhos).where(Carrinhos.id == id)
        ).first()

    # UPDATE
    def atualizar(self, id: int, carrinho: CarrinhoUpdate):

        db = self.session.scalars(
            select(Carrinhos).where(Carrinhos.id == id)
        ).first()

        if not db:
            return None

        dados = carrinho.model_dump(exclude_unset=True)

        for k, v in dados.items():
            setattr(db, k, v)

        self.session.commit()
        self.session.refresh(db)

        return db

    # DELETE
    def deletar(self, id: int) -> bool:

        db = self.session.scalars(
            select(Carrinhos).where(Carrinhos.id == id)
        ).first()

        if not db:
            return False

        self.session.delete(db)
        self.session.commit()

        return True
    
    def finalizar_compra(self, carrinho_id: int):

        carrinho = (
            self.session.query(Carrinhos).filter(Carrinhos.id == carrinho_id).first())
        
        if not carrinho:
            raise Exception("Carrinho não encontrado")

        itens = (
            self.session.query(ItensCarrinho).filter(ItensCarrinho.carrinho_id == carrinho_id).all())


        if not itens:
            raise Exception("Carrinho vazio")
        
        valor_total = 0
        quantidade_itens = 0

        for item in itens:
            produto = item.produto
            if produto.estoque < item.quantidade:
                raise Exception(f"Estoque insuficiente para {produto.nome}")


            produto.estoque -= item.quantidade
            valor_total += (produto.preco * item.quantidade)
            quantidade_itens += item.quantidade



        for item in itens:
            self.session.delete(item)


        self.session.commit()


        return {
            "mensagem": "Compra finalizada com sucesso.",
            "valor_total": valor_total,
            "quantidade_itens": quantidade_itens
        }