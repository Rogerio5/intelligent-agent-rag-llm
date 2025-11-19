# Guia de instalação e execução

## Pré-requisitos
- Python 3.11
- Docker e Docker Compose (opcional, recomendado)
- VS Code (recomendado)

## Ambiente local (sem Docker)
1. Crie venv e instale dependências:
python -m venv .venv source .venv/bin/activate # Windows: .venv\Scripts\activate pip install -r requirements.txt

2. Rode a API:
uvicorn api.main:app --reload

3. Acesse:
- http://localhost:8000
- http://localhost:8000/docs

## Com Docker Compose
1. Na raiz do projeto:
docker compose up --build

2. Acesse:
- API: http://localhost:8000
- MLflow: http://localhost:5000

## Index RAG
- Adicione documentos em `data/docs/*.txt` e escreva um script simples para carregar e construir índice usando `RAGStore.build_or_load_index()` e `save_index()`.

## Testes
pytest -q