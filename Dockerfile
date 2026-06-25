# 阿尔兹海默症诊断系统 - Docker镜像构建文件
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ninja-build libgl1-mesa-glx libglib2.0-0 \
    fonts-wqy-microhei fonts-wqy-zenhei fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir -p data results reports uploaded_img temp demodata logs static/fonts

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY . .

# 下载中文字体并清除matplotlib缓存
RUN python build_font.py && \
    python -c "import matplotlib, glob, os; [os.remove(f) for f in glob.glob(os.path.join(matplotlib.get_cachedir(), 'fontlist*.json'))]"

EXPOSE 8888

# 启动前验证字体
CMD python pre_start.py && uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8888}