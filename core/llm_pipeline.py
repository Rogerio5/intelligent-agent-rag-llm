import os
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Configuração de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DEFAULT_MODEL_NAME = os.getenv("MODEL_NAME", "gpt2")  # modelo leve para começar

class LLMPipeline:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME, device: str = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        try:
            logger.info(f"Carregando modelo {self.model_name} no dispositivo {self.device}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.model.to(self.device)
            logger.info("Modelo carregado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo {self.model_name}: {e}")
            self.tokenizer, self.model = None, None

    def generate(self, prompt: str, max_new_tokens: int = 128, temperature: float = 0.7) -> str:
        if not self.model or not self.tokenizer:
            return "Erro: modelo não carregado."

        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return text[len(prompt):].strip() if text.startswith(prompt) else text.strip()
        except Exception as e:
            logger.error(f"Erro na geração de texto: {e}")
            return "Desculpe, houve um erro ao gerar a resposta."
