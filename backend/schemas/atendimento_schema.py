from pydantic import BaseModel


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
    id: int
    diagnostico: str
    observacoes: str
    animal_id: int
    usuario_id: int