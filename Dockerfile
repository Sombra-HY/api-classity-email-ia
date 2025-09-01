# Usa imagem oficial Python 3.10
FROM python:3.10.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia todo o projeto para o container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Dá permissão de execução para start.sh
RUN chmod +x start.sh

# Expõe a porta padrão
EXPOSE 8080

# Comando para iniciar o servidor
# Cloud Run define a porta via variável de ambiente $PORT
CMD ["./start.sh"]
