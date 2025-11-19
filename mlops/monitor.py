import os
import time
from typing import Dict

# Mock simples de métricas em memória
_METRICS = {
    "latency_ms_avg": 120.0,
    "requests_count": 0,
    "model_version": os.getenv("MODEL_NAME", "gpt2"),
    "satisfaction_score_avg": 4.3,
}

def record_request(latency_ms: float):
    _METRICS["requests_count"] += 1
    # média móvel simples
    _METRICS["latency_ms_avg"] = (_METRICS["latency_ms_avg"] * 0.9) + (latency_ms * 0.1)

def get_service_metrics() -> Dict[str, float]:
    # Poderia integrar com Prometheus client aqui
    return _METRICS
