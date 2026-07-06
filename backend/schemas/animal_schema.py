from pydantic import BaseModel


# =========================
# CREATE
# =========================
class AnimalCreate(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: int
    cliente_id: int


# =========================
# UPDATE
# =========================
class AnimalUpdate(BaseModel):
    nome: str | None = None
    especie: str | None = None
    raca: str | None = None
    idade: int | None = None


# =========================
# RESPONSE
# =========================
class AnimalResponse(BaseModel):
    id: int
    nome: str
    especie: str
    raca: str
    idade: int
    cliente_id: int