from sqlmodel import SQLModel


class AtendimentoCreate(SQLModel):
    diagnostico: str
    observacoes: str
    animal_id: int
    usuario_id: int


class AtendimentoUpdate(SQLModel):
    diagnostico: str | None = None
    observacoes: str | None = None


class AtendimentoResponse(SQLModel):
    id: int
    diagnostico: str
    observacoes: str
    animal_id: int
    usuario_id: int