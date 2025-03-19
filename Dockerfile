# Usa uma imagem oficial do Python como base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Baixa o modelo de linguagem do spaCy
RUN python -m spacy download pt_core_news_sm
RUN python -m nltk.downloader punkt

# Define as variáveis de ambiente para desativar WebSocket e configurar CORS
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKETS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=true
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_SERVER_ALLOWED_ORIGINS=*

# Expõe a porta que o Streamlit vai rodar
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "streamlitApp.py", "--server.port=8501", "--server.address=0.0.0.0"]
