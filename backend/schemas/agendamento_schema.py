from pydantic import BaseModel, ConfigDict
from datetime import datetime


# =========================
# CREATE
# =========================
class AgendamentoCreate(BaseModel):
    data_agendamento: datetime
    descricao: str
    animal_id: int


# =========================
# UPDATE
# =========================
class AgendamentoUpdate(BaseModel):
    data_agendamento: datetime | None = None
    descricao: str | None = None
    status: str | None = None


# =========================
# RESPONSE
# =========================
class AgendamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_agendamento: datetime
    descricao: str
    status: str
    animal_id: int