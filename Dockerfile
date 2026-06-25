# 阿尔兹海默症诊断系统 - Docker镜像构建文件
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir -p data results reports uploaded_img temp demodata logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

CMD uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8888}