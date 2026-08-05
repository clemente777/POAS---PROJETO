from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VacinaCreate(BaseModel):

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    fabricante: str = Field(
        min_length=2,
        max_length=100
    )

    quantidade_doses: int = Field(
        ge=1
    )

    intervalo_dias: int = Field(
        ge=1
    )

    descricao: Optional[str] = Field(
        default=None,
        max_length=300
    )


class VacinaUpdate(BaseModel):

    nome: Optional[str] = None

    fabricante: Optional[str] = None

    quantidade_doses: Optional[int] = None

    intervalo_dias: Optional[int] = None

    descricao: Optional[str] = None


class VacinaResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    nome: str

    fabricante: str

    quantidade_doses: int

    intervalo_dias: int

    descricao: Optional[str]