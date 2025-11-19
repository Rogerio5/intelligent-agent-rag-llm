from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        description="Pergunta feita pelo usuário ao agente inteligente.",
        example="Qual é o horário de atendimento?"
    )
    user_id: Optional[str] = Field(
        None,
        description="Identificador opcional do usuário que fez a pergunta.",
        example="user_123"
    )

class AskResponse(BaseModel):
    answer: str = Field(
        ...,
        description="Resposta gerada pelo agente inteligente.",
        example="Nosso horário de atendimento é das 8h às 18h."
    )
    sources: List[str] = Field(
        default=[],
        description="Lista de fontes utilizadas para gerar a resposta.",
        example=["faq.json", "manual_atendimento.pdf"]
    )

class TrainRequest(BaseModel):
    dataset_path: str = Field(
        ...,
        description="Caminho para o dataset de treinamento em formato JSON.",
        example="/data/faq.json"
    )
    params: Dict[str, Any] = Field(
        default={"epochs": 5, "learning_rate": 0.01},
        description="Parâmetros de treinamento do modelo.",
        example={"epochs": 10, "learning_rate": 0.001}
    )

class TrainResponse(BaseModel):
    status: str = Field(
        ...,
        description="Status do treinamento.",
        example="success"
    )
    run_id: str = Field(
        ...,
        description="ID do experimento registrado no MLflow.",
        example="12345"
    )
    metrics: Dict[str, Any] = Field(
        ...,
        description="Métricas resultantes do treinamento.",
        example={"accuracy": 0.92, "loss": 0.08}
    )

class MetricsResponse(BaseModel):
    total_requests: int = Field(
        ...,
        description="Número total de requisições recebidas pelo serviço.",
        example=152
    )
    avg_latency_ms: float = Field(
        ...,
        description="Latência média das requisições em milissegundos.",
        example=123.45
    )
