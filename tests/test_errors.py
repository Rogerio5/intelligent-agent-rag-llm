import pytest
from core.agent import AgentService

def test_dataset_inexistente():
    agent = AgentService(dataset_path="data/inexistente.json")
    answer, sources = agent.answer_question("Qual é o horário de atendimento?")
    assert "Modelo não treinado" in answer

def test_parametros_invalidos():
    # Simula parâmetros inválidos no treino
    with pytest.raises(Exception):
        from mlops.train import train_or_update_model
        train_or_update_model("data/faq.json", {"C": -1})  # valor inválido
