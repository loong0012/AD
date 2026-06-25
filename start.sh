#!/bin/bash
# 阿尔兹海默症诊断系统 - 云部署启动脚本

PORT=${PORT:-8888}
HOST=${HOST:-0.0.0.0}
WORKERS=${WORKERS:-2}

echo "============================================"
echo "  AD-CPredSys 阿尔兹海默症诊断系统"
echo "  Version: 3.0.0"
echo "  Port: $PORT"
echo "  Workers: $WORKERS"
echo "============================================"

# 创建必要的目录
mkdir -p ./data ./results ./reports ./uploaded_img ./temp ./demodata ./logs

# 启动服务
exec uvicorn src.app:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level info \
    --no-access-log