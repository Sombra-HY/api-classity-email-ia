import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# =========================
# 1. Carregar Dataset CSV
# =========================
df = pd.read_csv("emails_classificacao_200.csv")
df["label"] = df["label"].map({"produtivo": 0, "improdutivo": 1})

# =========================
# 2. Split treino / validação
# =========================
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

# =========================
# 3. Tokenização
# =========================
tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")

def tokenize(batch):
    return tokenizer(batch["texto"], padding="max_length", truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

# Renomear coluna label e ajustar formato
train_dataset = train_dataset.rename_column("label", "labels")
val_dataset = val_dataset.rename_column("label", "labels")

train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
val_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

# =========================
# 4. Carregar Modelo
# =========================
model = AutoModelForSequenceClassification.from_pretrained(
    "neuralmind/bert-base-portuguese-cased",
    num_labels=2
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# =========================
# 5. Definir Métricas
# =========================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    return {"accuracy": accuracy_score(labels, predictions)}

# =========================
# 6. Definir Treinamento
# =========================
training_args = TrainingArguments(
    output_dir="resultado_treinamento",
    save_strategy="epoch",          # salva o modelo a cada época
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    learning_rate=5e-5,
    logging_steps=10,
    save_total_limit=1,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

# =========================
# 7. Treinar o Modelo
# =========================
trainer.train()

# Salvar modelo e tokenizer
trainer.save_model("./modelo_emails")
tokenizer.save_pretrained("./modelo_emails")

# =========================
# 8. Testar o Modelo
# =========================
texto_teste = [
    "Parabéns pelo seu aniversário!",
    "Segue o relatório do projeto.",
    "Promoção imperdível! Compre agora.",
    "Reunião confirmada para amanhã às 9h."
]

inputs = tokenizer(texto_teste, return_tensors="pt", padding=True, truncation=True).to(device)

with torch.no_grad():
    outputs = model(**inputs)
    predicoes = outputs.logits.argmax(dim=1)

for txt, pred in zip(texto_teste, predicoes):
    classe = "Produtivo" if pred.item() == 0 else "Improdutivo"
    print(f"Email: {txt} -> Classe: {classe}")
