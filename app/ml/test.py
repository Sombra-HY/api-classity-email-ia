import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

device = "cuda" if torch.cuda.is_available() else "cpu"

# Caminho relativo correto dentro de test.py
model_path = os.path.join(os.path.dirname(__file__), "modelo_emails")

# Carregar modelo local
model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model.to(device)

def is_productive(texto: str) -> str:
    inputs = tokenizer([texto], return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        pred = model(**inputs).logits.argmax(dim=1).item()
    return "Produtivo" if pred == 0 else "Improdutivo"

# Teste
if __name__ == "__main__":
    email = "Olá, Mariana! Feliz aniversário! Lembre-se de revisar o relatório do projeto Beta."
    print(is_productive(email))
