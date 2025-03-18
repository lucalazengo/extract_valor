FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download pt_core_news_sm
RUN python -m nltk.downloader punkt

EXPOSE 8501

# 7. Comando para iniciar o Streamlit
CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
