FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY build_features.py .
COPY processor/ processor/

CMD ["python", "build_features.py"]
