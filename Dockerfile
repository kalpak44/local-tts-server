FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy voices definitions and download script first
COPY voices_definitions.yaml .
COPY download_models.py .

# Pre-download all models during build time for offline use
RUN python download_models.py

# Copy the rest of the application
COPY . .

EXPOSE 5003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5003"]
