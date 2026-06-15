from sqlmodel import Session

from backend.models.models import Clientes
from backend.services.interfaces.cliente_service import ClienteService

class ClienteServiceImpl(ClienteService):

    def __init__(self, session: Session):
        self.session = session

    def listar_clientes(self):
        return self.session.query(Clientes).all()

    def buscar_cliente_por_id(self, id):
        return self.session.query(Clientes).get(id)

    def criar_cliente(self, cliente):
        self.session.add(cliente)
        self.session.commit()
        self.session.refresh(cliente)

        return cliente

    def atualizar_cliente(self, id, cliente):
        self.session.query(Clientes).filter(
            Clientes.id == id
        ).update(cliente.model_dump())

        self.session.commit()

        return cliente

    def deletar_cliente(self, id):
        cliente = self.session.query(Clientes).get(id)

        if cliente:
            self.session.delete(cliente)
            self.session.commit()

        return cliente