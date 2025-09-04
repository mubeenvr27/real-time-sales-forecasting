FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Increase timeout and retries for slow networks
RUN pip install --no-cache-dir --default-timeout=100 scipy==1.12.0 \
    && pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY app/ app/
COPY data/processed/ data/processed/

EXPOSE 8050

CMD ["python", "app/dashboard.py"]