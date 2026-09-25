FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY docs ./docs
COPY ingest.py .
COPY retrieve.py .
COPY models.py .
COPY prompts.py .
COPY graph.py .
COPY main.py .

# Download the embedding model and create the ChromaDB database
RUN python ingest.py

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]