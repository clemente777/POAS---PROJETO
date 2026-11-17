from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AplicacaoVacinaCreate(BaseModel):
    animal_id: int

    vacina_id: int

    lote: str | None = None

    observacoes: str | None = None

    proxima_dose: datetime | None = None


class AplicacaoVacinaUpdate(BaseModel):
    lote: str | None = None

    observacoes: str | None = None

    proxima_dose: datetime | None = None


class AplicacaoVacinaClienteResponse(BaseModel):
    """
    Carteira de vacinação vista pelo Cliente: já traz os nomes
    (o Cliente não tem acesso às rotas de vacinas nem de usuários).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    animal_id: int

    vacina_id: int

    vacina_nome: str

    fabricante: str

    veterinario_nome: str | None = None

    data_aplicacao: datetime

    proxima_dose: datetime | None = None

    lote: str | None = None

    observacoes: str | None = None


class AplicacaoVacinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    animal_id: int

    vacina_id: int

    veterinario_id: int

    data_aplicacao: datetime

    proxima_dose: datetime | None = None

    lote: str | None = None

    observacoes: str | None = None
