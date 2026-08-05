from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AplicacaoVacinaCreate(BaseModel):

    animal_id: int

    vacina_id: int

    lote: Optional[str] = None

    observacoes: Optional[str] = None

    proxima_dose: Optional[datetime] = None



class AplicacaoVacinaUpdate(BaseModel):

    lote: Optional[str] = None

    observacoes: Optional[str] = None

    proxima_dose: Optional[datetime] = None



class AplicacaoVacinaResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    animal_id: int

    vacina_id: int

    veterinario_id: int

    data_aplicacao: datetime

    proxima_dose: Optional[datetime] = None

    lote: Optional[str] = None

    observacoes: Optional[str] = None