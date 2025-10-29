FROM python:3.10-slim

# Evita prompts interativos e atualiza pacotes
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 🛠️ Instale dependências do sistema, inclusive libgomp1
RUN apt-get update && apt-get install -y \
    gcc \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
