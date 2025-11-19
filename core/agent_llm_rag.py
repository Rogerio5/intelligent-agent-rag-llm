import time
import logging
from typing import List, Tuple
from core.llm_pipeline import LLMPipeline
from core.rag import RAGStore
from mlops.mlflow_tracking import log_inference

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Você é um agente de atendimento ao cliente.
Responda de forma objetiva e educada.
Se não tiver certeza, explique as limitações e sugira encaminhamento para suporte humano."""

def build_prompt(question: str, context_chunks: List[str]) -> str:
    context_text = "\n\n".join([f"- {c}" for c in context_chunks])
    return f"{SYSTEM_PROMPT}\n\nContexto:\n{context_text}\n\nPergunta:\n{question}\n\nResposta:"

class AgentService:
    def __init__(self):
        self.llm = LLMPipeline()
        self.rag = RAGStore()
        try:
            self.rag.load_index_from_disk()
        except Exception as e:
            logger.warning(f"Não foi possível carregar índice: {e}")

    def answer_question(self, question: str, user_id: str = None) -> Tuple[str, List[str]]:
        t0 = time.time()
        try:
            retrieved = self.rag.retrieve(question, k=4)
            context_chunks = [c for c, _ in retrieved]
            prompt = build_prompt(question, context_chunks or ["(Sem contexto disponível)"])
            answer = self.llm.generate(prompt, max_new_tokens=180, temperature=0.6)
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            answer = "Desculpe, não consegui processar sua pergunta. Encaminhe para suporte humano."
            context_chunks = []

        latency_ms = (time.time() - t0) * 1000
        log_inference(
            inputs={"question": question},
            outputs={"answer": answer},
            metadata={"latency_ms": latency_ms, "user_id": user_id or "anonymous"}
        )
        sources = [c[:120] + "..." for c in context_chunks] if context_chunks else []
        return answer, sources
