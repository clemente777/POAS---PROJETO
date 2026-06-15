from datetime import datetime
from sqlmodel import SQLModel


class AgendamentoCreate(SQLModel):
    data_agendamento: datetime
    descricao: str
    animal_id: int


class AgendamentoUpdate(SQLModel):
    data_agendamento: datetime | None = None
    descricao: str | None = None
    status: str | None = None


class AgendamentoResponse(SQLModel):
    id: int
    data_agendamento: datetime
    descricao: str
    status: str
    animal_id: int