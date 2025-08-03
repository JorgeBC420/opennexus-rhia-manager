# Dockerfile para OpenNexus RHIA Manager
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables de entorno para PostgreSQL y Ollama
ENV DATABASE_URI=postgresql://postgres:admin@db:5432/opennexus_rh_db
ENV OLLAMA_API_URL=http://ollama:11434/api/generate
ENV OLLAMA_MODEL=llama3

CMD ["python", "main_app.py"]
