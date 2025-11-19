import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api.routes.ask import router as ask_router
from api.routes.train import router as train_router
from api.routes.metrics import router as metrics_router

# -----------------------------
# Configuração de logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("agente-inteligente")

# -----------------------------
# Configurações externas (via variáveis de ambiente)
# -----------------------------
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
APP_VERSION = os.getenv("APP_VERSION", "0.2.0")

# -----------------------------
# Inicialização da aplicação
# -----------------------------
app = FastAPI(
    title="Agente Inteligente de Atendimento",
    version=APP_VERSION,
    description="API para atendimento inteligente com endpoints de perguntas, treinamento e métricas."
)

# -----------------------------
# Configuração de CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Registro dos routers
# -----------------------------
app.include_router(ask_router, prefix="/ask", tags=["Perguntas"])
app.include_router(train_router, prefix="/train", tags=["Treinamento"])
app.include_router(metrics_router, prefix="/metrics", tags=["Métricas"])

# -----------------------------
# Endpoints básicos
# -----------------------------
@app.get("/", tags=["Root"], summary="Root endpoint")
def root():
    """Endpoint raiz para verificar se a API está online."""
    logger.info("Root endpoint acessado.")
    return {"status": "ok", "message": "Agente Inteligente de Atendimento API"}

@app.get("/health", tags=["Health"], summary="Healthcheck")
def health():
    """Endpoint simples para monitoramento de saúde do serviço."""
    logger.info("Healthcheck acessado.")
    return {"status": "healthy"}

# -----------------------------
# Instrumentação Prometheus
# -----------------------------
Instrumentator().instrument(app).expose(app)
