import logging
from fastapi import APIRouter, HTTPException
from api.models.schemas import TrainRequest, TrainResponse
from mlops.train import train_or_update_model

# Configuração de logger
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/",
    response_model=TrainResponse,
    summary="Treinar ou atualizar modelo",
    description=(
        "Executa o processo de treinamento ou atualização do modelo com base "
        "no dataset fornecido e parâmetros. "
        "Retorna o ID do experimento e o status do treinamento."
    ),
)
def train(req: TrainRequest):
    """
    Endpoint para treinar ou atualizar o modelo.
    - Valida se o caminho do dataset foi informado.
    - Executa o treinamento via função `train_or_update_model`.
    - Registra logs de sucesso ou falha.
    """
    try:
        if not req.dataset_path.strip():
            raise HTTPException(
                status_code=400,
                detail="Caminho do dataset não pode estar vazio."
            )

        result = train_or_update_model(req.dataset_path, req.params)
        logger.info(f"Treinamento concluído com sucesso. Run ID: {result.get('run_id')}")
        return result

    except HTTPException as e:
        logger.warning(f"Erro de validação no treino: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no treinamento: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno no treinamento."
        )

