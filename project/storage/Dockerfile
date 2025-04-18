# ใช้ภาพพื้นฐานของ Python 3.8
FROM python:3.8-slim

WORKDIR /app

# First, update the package list and install build-essential and python3-dev
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5003"]
