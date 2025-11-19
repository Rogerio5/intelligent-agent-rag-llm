import pytest
import json
import os

@pytest.fixture
def small_dataset(tmp_path):
    """Cria um dataset pequeno de teste em JSON."""
    data = [
        {"text": "Qual é o horário de atendimento?", "label": "horario", "answer": "Das 8h às 18h."},
        {"text": "Vocês atendem online?", "label": "online", "answer": "Sim, via chat e e-mail."}
    ]
    dataset_path = tmp_path / "faq.json"
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(dataset_path)
