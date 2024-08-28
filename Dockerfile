# Usar uma imagem base do Python
FROM python:3.12

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o restante do código da aplicação
COPY . /app

# Comando para executar a aplicação Streamlit
CMD ["streamlit", "run", "app.py"]
