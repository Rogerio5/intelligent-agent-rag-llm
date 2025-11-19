# intelligent-agent-rag-llm

# 🤖 AGENTE-INTELIGENTE  
## 🚀 FastAPI + LangChain + RAG + MLflow + Hugging Face


---

## 🏅 Badges

- 📦 Tamanho do repositório:  
  ![GitHub repo size](https://img.shields.io/github/repo-size/Rogerio5/AGENTE-INTELIGENTE)

- 📄 Licença do projeto:  
  ![GitHub license](https://img.shields.io/github/license/Rogerio5/AGENTE-INTELIGENTE)

---

## 📋 Índice / Table of Contents

- [📖 Descrição / Description](#-descrição--description)  
- [📌 Status do Projeto / Project-Status](#-status-do-projeto--project-status)  
- [⚙️ Arquitetura / Architecture](#-arquitetura--architecture)  
- [🚀 Guia de Instalação / Installation Guide](#-guia-de-instalação--installation-guide)  
- [🧪 Testes / Tests](#-testes--tests)  
- [🧰 Tecnologias / Technologies](#-tecnologias--technologies)  
- [👨‍💻 Desenvolvedor / Developer](#-desenvolvedor--developer)  
- [📜 Licença / License](#-licença--license)  
- [🏁 Conclusão / Conclusion](#-conclusão--conclusion)

---

## 📖 Descrição / Description

Este projeto é um agente inteligente que utiliza **LLMs** e técnicas de **RAG (Retrieval-Augmented Generation)** para responder perguntas com contexto.  
A arquitetura combina **FastAPI**, **LangChain**, **MLflow**, **Docker** e **Hugging Face**, com foco em automação, rastreabilidade e escalabilidade.

---

## 📌 Status do Projeto / Project Status

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)

---

## ⚙️ Arquitetura / Architecture

- API FastAPI expõe os endpoints: `/ask`, `/train`, `/metrics`  
- Orquestração com LangChain e RAG (FAISS + embeddings)  
- LLM via Hugging Face (`gpt2` como modelo base)  
- MLOps com MLflow para tracking de runs, métricas e artefatos  
- Deploy via Dockerfile e docker-compose com serviço MLflow  
- Futuro: Prometheus/Grafana + Kubernetes (`infra/k8s`)  

### 🔁 Fluxo de execução

1. Usuário chama `/ask`  
2. Agente consulta RAG e monta prompt com contexto  
3. LLM gera resposta  
4. Logging de inferência no MLflow  
5. Métricas expostas em `/metrics`

---

## 🚀 Guia de Instalação / Installation Guide

### ✅ Pré-requisitos

- Python 3.11  
- Docker e Docker Compose (opcional, recomendado)  
- VS Code (recomendado)

### 🔧 Ambiente local (sem Docker)

```bash
python -m venv .venv  
source .venv/bin/activate  # Windows: .venv\Scripts\activate  
pip install -r requirements.txt  
uvicorn api.main:app --reload

Acesse:

http://localhost:8000

http://localhost:8000/docs
```
🐳 Com Docker Compose
```
docker compose up --build

Acesse:

API: http://localhost:8000

MLflow: http://localhost:5000
```

📚 Index RAG
Adicione documentos em data/docs/*.txt

Use RAGStore.build_or_load_index() e save_index() para construir o índice

---

🧪 Testes / Tests

pytest -q

---

🧰 Tecnologias / Technologies

<p align="left"> <img alt="Python" title="Python" width="50px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"/>
<img alt="FastAPI" title="FastAPI" width="50px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg"/>
<img alt="Docker" title="Docker" width="50px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg"/>
<img alt="LangChain" title="LangChain" width="50px" src="https://avatars.githubusercontent.com/u/139903294?s=200&v=4"/>
<img alt="MLflow" title="MLflow" width="50px" src="https://raw.githubusercontent.com/mlflow/mlflow/master/assets/logo-white.svg"/>
<img alt="Hugging Face" title="Hugging Face" width="50px" src="https://huggingface.co/front/assets/huggingface_logo.svg"/> </p>

---

## 📜 Licença / License

Este projeto está sob licença MIT. Para mais detalhes, veja o arquivo `LICENSE`.  

This project is under the MIT license. For more details, see the `LICENSE` file.

---

🏁 Conclusão / Conclusion

Este projeto representa uma aplicação prática de LLMs e MLOps, integrando componentes modernos de IA para criar um agente inteligente capaz de responder com contexto, rastrear inferências e escalar via Docker/Kubernetes. Ideal para uso em sistemas de atendimento, assistentes virtuais ou plataformas de conhecimento interno.
