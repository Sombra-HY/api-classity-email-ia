import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class EmailClassificationService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Caminho correto para a pasta do modelo
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml", "modelo_emails"))

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Diretório do modelo não encontrado: {self.model_path}")

        # Carregar modelo e tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

        self.model.to(self.device)

    def classify_email(self, texto: str) -> str:
        inputs = self.tokenizer([texto], return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            pred = self.model(**inputs).logits.argmax(dim=1).item()
        return "Produtivo" if pred == 0 else "Improdutivo"


# Teste rápido
if __name__ == "__main__":
    service = EmailClassificationService()
    email = "Olá, Mariana! Feliz aniversário! Lembre-se de revisar o relatório do projeto Beta."
    print(service.classify_email(email))
