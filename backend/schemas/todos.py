# from pydantic import BaseModel, ConfigDict
# from datetime import datetime


# # CREATE
# class AgendamentoCreate(BaseModel):
#     data_agendamento: datetime
#     descricao: str
#     animal_id: int



# # UPDATE
# class AgendamentoUpdate(BaseModel):
#     data_agendamento: datetime | None = None
#     descricao: str | None = None
#     status: str | None = None


# # RESPONSE
# class AgendamentoResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     data_agendamento: datetime
#     descricao: str
#     status: str
#     animal_id: int

# from pydantic import BaseModel, ConfigDict


# # CREATE
# class AnimalCreate(BaseModel):
#     nome: str
#     especie: str
#     raca: str
#     idade: int
#     cliente_id: int



# # UPDATE
# class AnimalUpdate(BaseModel):
#     nome: str | None = None
#     especie: str | None = None
#     raca: str | None = None
#     idade: int | None = None


# # RESPONSE
# class AnimalResponse(BaseModel):

#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     nome: str
#     especie: str
#     raca: str
#     idade: int
#     cliente_id: int
# from pydantic import BaseModel, ConfigDict


# # CREATE
# class AtendimentoCreate(BaseModel):
#     diagnostico: str
#     observacoes: str
#     animal_id: int
#     usuario_id: int


# # UPDATE
# class AtendimentoUpdate(BaseModel):
#     diagnostico: str | None = None
#     observacoes: str | None = None


# # RESPONSE
# class AtendimentoResponse(BaseModel):

#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     diagnostico: str
#     observacoes: str
#     animal_id: int
#     usuario_id: int
#     id: int
#     diagnostico: str
#     observacoes: str
#     animal_id: int
#     usuario_id: int
# from pydantic import BaseModel, EmailStr, ConfigDict


# # CREATE
# class CarrinhoCreate(BaseModel):
#     cliente_id: int


# # UPDATE
# class CarrinhoUpdate(BaseModel):
#     cliente_id: int | None = None


# # RESPONSE
# class CarrinhoResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     cliente_id: int


# class CompraResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     mensagem: str
#     valor_total: float
#     quantidade_itens: int

# from pydantic import BaseModel, ConfigDict


# class DashboardResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     usuarios: int
#     clientes: int
#     animais: int
#     agendamentos: int
#     atendimentos: int
#     produtos: int
#     carrinhos: int
#     itens_carrinho: int
# from datetime import datetime

# from pydantic import BaseModel, ConfigDict


# # RESPONSE DO ATENDIMENTO NO HISTÓRICO
# class HistoricoAtendimentoResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     data: datetime
#     veterinario: str | None = None
#     diagnostico: str
#     observacoes: str


# # DADOS DO ANIMAL
# class AnimalHistoricoAnimalResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     nome: str
#     especie: str
#     raca: str
#     idade: int


# # DADOS DO CLIENTE
# class AnimalHistoricoClienteResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     nome: str
#     telefone: str
#     email: str


# # RESPONSE FINAL
# class AnimalHistoricoResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     animal: AnimalHistoricoAnimalResponse
#     cliente: AnimalHistoricoClienteResponse
#     historico: list[HistoricoAtendimentoResponse]
# from pydantic import BaseModel, ConfigDict



# # CREATE
# class ItemCarrinhoCreate(BaseModel):
#     carrinho_id: int
#     produto_id: int
#     quantidade: int


# # UPDATE
# class ItemCarrinhoUpdate(BaseModel):
#     quantidade: int | None = None


# # RESPONSE
# class ItemCarrinhoResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     carrinho_id: int
#     produto_id: int
#     quantidade: int

# from datetime import datetime
# from pydantic import BaseModel, EmailStr, ConfigDict



# class UsuarioCreate(BaseModel):
#     nome: str
#     email: EmailStr
#     senha: str  # melhor nome do que senha_hash no input


# class UsuarioUpdate(BaseModel):
#     nome: str | None = None
#     email: EmailStr | None = None
#     senha: str | None = None


# class UsuarioResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
    
#     id: int
#     nome: str
#     email: EmailStr
#     criado_em: datetime

