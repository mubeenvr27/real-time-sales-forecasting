FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY app/ app/
COPY data/processed/ data/processed/

EXPOSE 8050

CMD ["python", "app/dashboard.py"]