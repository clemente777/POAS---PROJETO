from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AgendamentoCreate(BaseModel):

    data_agendamento: datetime

    descricao: str

    animal_id: int

    # opcional
    # será preenchido depois pelo administrador/veterinário
    veterinario_id: int | None = None



class AgendamentoUpdate(BaseModel):

    data_agendamento: datetime | None = None

    descricao: str | None = None

    status: str | None = None

    veterinario_id: int | None = None



class AgendamentoResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    data_agendamento: datetime

    descricao: str

    status: str

    animal_id: int

    veterinario_id: int | None