#!/bin/bash
# só cria o modelo se não existir
if [ ! -d "app/ml/resultado_treinamento" ]; then
    echo "Modelo não encontrado, criando..."
    python app/ml/create_model.py
else
    echo "Modelo já existe, pulando criação."
fi

# inicia o servidor
PORT=${PORT:-8000}  # usa $PORT se estiver definido, senão 8000 local
uvicorn main:app --host 0.0.0.0 --port $PORT
