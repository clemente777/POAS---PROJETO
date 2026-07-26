from pydantic import BaseModel, ConfigDict
from datetime import datetime



# ===============================
# CREATE
# ===============================

class AtendimentoCreate(BaseModel):

    diagnostico: str

    observacoes: str | None = None

    animal_id: int

    usuario_id: int

    data_atendimento: datetime | None = None




# ===============================
# UPDATE
# ===============================

class AtendimentoUpdate(BaseModel):

    diagnostico: str | None = None

    observacoes: str | None = None

    data_atendimento: datetime | None = None

    usuario_id: int | None = None




# ===============================
# RESPONSE
# ===============================

class AtendimentoResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    data_atendimento: datetime

    diagnostico: str

    observacoes: str | None

    status: str

    animal_id: int

    usuario_id: int