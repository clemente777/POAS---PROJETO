from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.database import get_session
from backend.schemas.dashboard_schema import DashboardResponse
from backend.services.implementations.dashboard_service_impl import DashboardServiceImpl

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])


def get_service(session: Session = Depends(get_session)):
    return DashboardServiceImpl(session)


@router.get(
    "/",
    response_model=DashboardResponse,
    summary="Dashboard do sistema",
    description="Retorna estatísticas gerais da clínica veterinária."
)
def dashboard(
    service: DashboardServiceImpl = Depends(get_service),
):
    return service.dashboard()