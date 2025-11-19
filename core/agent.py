import json
import os
import joblib
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self, dataset_path: str = "data/faq.json"):
        self.dataset_path = dataset_path
        self.label_to_answer = self._load_answers()
        try:
            self.vectorizer = joblib.load("artifacts/tfidf_vectorizer.pkl")
            self.model = joblib.load("artifacts/classifier.pkl")
        except Exception as e:
            logger.warning(f"Modelo não carregado: {e}")
            self.vectorizer = None
            self.model = None

    def _load_answers(self):
        if not os.path.exists(self.dataset_path):
            logger.warning("Dataset não encontrado.")
            return {}
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {item["label"]: item.get("answer", "") for item in data}

    def answer_question(self, question: str, user_id: str = None) -> Tuple[str, list]:
        if not self.model or not self.vectorizer:
            return "Modelo não treinado ainda. Execute /train primeiro.", []

        try:
            X = self.vectorizer.transform([question])
            label = self.model.predict(X)[0]
            answer = self.label_to_answer.get(label, "Desculpe, não encontrei uma resposta para isso.")
        except Exception as e:
            logger.error(f"Erro na classificação: {e}")
            answer = "Erro interno ao processar sua pergunta. Encaminhe para suporte humano."
            label = None

        sources = [self.dataset_path] if label else []
        return answer, sources
