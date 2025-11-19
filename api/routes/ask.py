import time
import logging
from fastapi import APIRouter, HTTPException
from api.models.schemas import AskRequest, AskResponse
from core.agent import AgentService
from mlops.monitor import record_request

logger = logging.getLogger(__name__)
router = APIRouter()
agent = AgentService()

@router.post(
    "/",
    response_model=AskResponse,
    summary="Fazer uma pergunta ao agente",
    description="Recebe uma pergunta do usuário e retorna a resposta do agente inteligente. "
                "Também registra métricas de latência e número de requisições."
)
def ask(req: AskRequest):
    start = time.time()
    try:
        if not req.question.strip():
            raise HTTPException(status_code=400, detail="Pergunta não pode estar vazia.")

        answer, sources = agent.answer_question(req.question, user_id=req.user_id)
        latency = (time.time() - start) * 1000
        record_request(latency)

        logger.info(f"Pergunta: {req.question} | Latência: {latency:.2f}ms")
        return AskResponse(answer=answer, sources=sources)

    except HTTPException as e:
        logger.warning(f"Erro de validação: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no endpoint /ask: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar pergunta.")
