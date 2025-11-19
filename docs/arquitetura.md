# Arquitetura

- API FastAPI expõe `/ask`, `/train`, `/metrics`.
- Orquestração com LangChain e RAG (FAISS + embeddings).
- LLM via Hugging Face (modelo base `gpt2` por simplicidade).
- MLOps: MLflow para tracking de runs, métricas e artefatos.
- Deploy: Dockerfile e docker-compose com serviço de MLflow.
- Futuro: Prometheus/Grafana, Kubernetes (manifests em `infra/k8s`).

Fluxo:
1. Usuário chama `/ask`.
2. Agente consulta RAG e monta prompt com contexto.
3. LLM gera resposta.
4. Logging de inferência no MLflow.
5. Métricas expostas em `/metrics`.
