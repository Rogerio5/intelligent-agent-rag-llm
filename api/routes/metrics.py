import logging
from fastapi import APIRouter, HTTPException
from api.models.schemas import MetricsResponse
from mlops.monitor import get_service_metrics

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/",
    response_model=MetricsResponse,
    summary="Obter métricas do serviço",
    description="Retorna métricas agregadas como número total de requisições e latência média."
)
def metrics():
    try:
        metrics_data = get_service_metrics()
        logger.info("Métricas consultadas com sucesso.")
        return MetricsResponse(**metrics_data)
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao obter métricas.")
