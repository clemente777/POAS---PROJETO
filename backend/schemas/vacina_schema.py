from pydantic import BaseModel, ConfigDict, Field


class VacinaCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)

    fabricante: str = Field(min_length=2, max_length=100)

    quantidade_doses: int = Field(ge=1)

    intervalo_dias: int = Field(ge=1)

    descricao: str | None = Field(default=None, max_length=300)


class VacinaUpdate(BaseModel):
    nome: str | None = None

    fabricante: str | None = None

    quantidade_doses: int | None = None

    intervalo_dias: int | None = None

    descricao: str | None = None


class VacinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    nome: str

    fabricante: str

    quantidade_doses: int

    intervalo_dias: int

    descricao: str | None
