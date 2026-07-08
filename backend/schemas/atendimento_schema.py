from pydantic import BaseModel, ConfigDict


# =========================
# CREATE
# ========================= 
class AtendimentoCreate(BaseModel):
    diagnostico: str
    observacoes: str
    animal_id: int
    usuario_id: int


# =========================
# UPDATE
# =========================
class AtendimentoUpdate(BaseModel):
    diagnostico: str | None = None
    observacoes: str | None = None


# =========================
# RESPONSE
# =========================
class AtendimentoResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    diagnostico: str
    observacoes: str
    animal_id: int
    usuario_id: int
    id: int
    diagnostico: str
    observacoes: str
    animal_id: int
    usuario_id: int