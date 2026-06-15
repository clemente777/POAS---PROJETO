from sqlmodel import SQLModel


class AnimalCreate(SQLModel):
    nome: str
    especie: str
    raca: str
    idade: int
    cliente_id: int


class AnimalUpdate(SQLModel):
    nome: str | None = None
    especie: str | None = None
    raca: str | None = None
    idade: int | None = None


class AnimalResponse(SQLModel):
    id: int
    nome: str
    especie: str
    raca: str
    idade: int
    cliente_id: int