from datetime import datetime

from pydantic import BaseModel, ConfigDict


# RESPONSE DO ATENDIMENTO NO HISTÓRICO
class HistoricoAtendimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: datetime
    veterinario: str | None = None
    diagnostico: str
    observacoes: str


# DADOS DO ANIMAL
class AnimalHistoricoAnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    especie: str
    raca: str
    idade: int


# DADOS DO CLIENTE
class AnimalHistoricoClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    telefone: str
    email: str


# RESPONSE FINAL
class AnimalHistoricoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    animal: AnimalHistoricoAnimalResponse
    cliente: AnimalHistoricoClienteResponse
    historico: list[HistoricoAtendimentoResponse]