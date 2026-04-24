# 阿尔兹海默症诊断系统 - Docker镜像构建文件
# 基于Python 3.11-slim镜像

FROM python:3.11-slim as base

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 创建应用目录
WORKDIR /app

# 创建必要的目录
RUN mkdir -p ./demodata ./data ./results ./reports ./uploaded_img ./temp

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY models/ ./models/
COPY config/ ./config/
COPY static/ ./static/
COPY demodata/ ./demodata/
COPY data/ ./data/
COPY results/ ./results/
COPY reports/ ./reports/
COPY uploaded_img/ ./uploaded_img/
COPY temp/ ./temp/

# 设置目录权限
RUN chmod -R 755 /app && \
    chmod -R 775 /app/uploaded_img && \
    chmod -R 775 /app/results && \
    chmod -R 775 /app/reports && \
    chmod -R 775 /app/temp

# 复制Nginx和Supervisor配置
COPY deployment/nginx.conf /etc/nginx/nginx.conf
COPY deployment/supervisord.conf /etc/supervisord.conf
COPY deployment/gunicorn_config.py /app/gunicorn_config.py

# 暴露端口
EXPOSE 8888 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8888/health || exit 1

# 启动命令
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]