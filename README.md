# 📧 Classificador de E-mails com IA (FastAPI + BERT)

Este projeto é uma **API REST desenvolvida com FastAPI** para **classificação de e-mails como "produtivo" ou "improdutivo"**.  
A API utiliza um **modelo de IA baseado em BERT** treinado em português, com dados contidos no arquivo `emails_classificacao_200.csv`.

---

## ✅ **Como Funciona**
- Treina um modelo **BERT-base-portuguese** usando Hugging Face Transformers.
- Classifica e-mails via:
  - **Upload de arquivo (.txt ou .pdf)**
  - **Envio de texto diretamente no corpo da requisição**
- Mantém um modelo salvo localmente para não precisar re-treinar toda vez.

---

## ✅ **Estrutura do Projeto**
```
api-classity-ia/
│── app/
│   ├── exceptions/               # Tratamento de exceções personalizadas
│   ├── ml/                       # Modelo e scripts de treinamento
│   │   ├── modelo_emails/        # Modelo treinado salvo
│   │   ├── resultado_treinamento # Checkpoints do treinamento
│   │   ├── create_model.py       # Script de treinamento do modelo
│   │   ├── emails_classificacao_200.csv # Dataset usado no treinamento
│   │   ├── test.py               # Testes do modelo
│   ├── routes/                   # Rotas da API
│   ├── schemas/                  # DTOs para respostas
│   ├── services/                 # Lógica de classificação
│── main.py                       # Inicialização da aplicação FastAPI
│── requirements.txt              # Dependências
│── Dockerfile                    # Configuração para container
│── start.sh                      # Script para inicialização e treino automático
```

---

## ✅ **Como Rodar o Projeto**

### **1. Clonar o repositório**
```bash
git clone https://github.com/seuusuario/api-classity-ia.git
cd api-classity-ia
```

### **2. Criar ambiente virtual e instalar dependências**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### **3. Iniciar o projeto**
O projeto possui um script `start.sh` que:
- Verifica se o modelo já existe
- Caso não exista, **treina automaticamente** com o CSV padrão (`emails_classificacao_200.csv`)
- Inicia o servidor FastAPI

Para executar:
```bash
chmod +x start.sh
./start.sh
```
A API estará disponível em:  
**http://127.0.0.1:8000/docs** (Swagger UI)

---

## ✅ **Retraining do Modelo**
Caso queira re-treinar com outro dataset:
- Substitua o arquivo CSV dentro de `app/ml/` por outro com o mesmo formato.
- Ou exclua as pastas `app/ml/modelo_emails` e `app/ml/resultado_treinamento`.
- Execute novamente:
```bash
python app/ml/create_model.py
```
Ou simplesmente rode o `start.sh` que fará o processo automaticamente.

---

## ✅ **Endpoints Disponíveis**
### **1. Classificação via arquivo**
```
POST /classity-email/file
```
**Parâmetro:** `file` (UploadFile) → Arquivo `.txt` ou `.pdf`  
**Resposta:**
```json
{
  "filename": "email.txt",
  "length": 120,
  "classification": "produtivo"
}
```

### **2. Classificação via texto**
```
POST /classity-email/text
```
**Parâmetro:** `text` (Form) → Texto do e-mail  
**Resposta:**
```json
{
  "text_length": 85,
  "text_preview": "Segue o relatório do projeto...",
  "classification": "produtivo"
}
```

---

## ✅ **Tecnologias Utilizadas**
- **Python 3.x**
- **FastAPI**
- **Hugging Face Transformers**
- **PyTorch**
- **scikit-learn**
- **pandas**
- **Docker**

---

Email: "Parabéns pelo seu aniversário!" -> Classe: Improdutivo
Email: "Segue o relatório do projeto."   -> Classe: Produtivo
```
