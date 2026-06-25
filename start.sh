#!/bin/bash
# 阿尔兹海默症诊断系统 - 云部署启动脚本

PORT=${PORT:-8888}
HOST=${HOST:-0.0.0.0}
WORKERS=${WORKERS:-2}

echo "============================================"
echo "  AD-CPredSys 阿尔兹海默症诊断系统"
echo "  Version: 3.1.0"
echo "  Port: $PORT"
echo "  Workers: $WORKERS"
echo "============================================"

# 创建必要的目录
mkdir -p ./data ./results ./reports ./uploaded_img ./temp ./demodata ./logs

# 注册中文字体并验证
echo "正在验证中文字体..."
python -c "
import os, matplotlib.font_manager as fm
font_path = 'static/fonts/NotoSansCJKsc-Regular.otf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    print(f'字体验证成功: {prop.get_name()}')
else:
    print('项目字体文件不存在，使用系统字体')
fm._load_fontmanager(try_read_cache=False)
cn_fonts = [f.name for f in fm.fontManager.ttflist if any(
    k in f.name.lower() for k in ['yahei','simhei','wqy','noto','cjk','hei','song','kai','ming']
)]
print(f'可用中文字体: {cn_fonts[:8]}')
" || echo "字体验证失败，但继续启动服务"

# 启动服务
exec uvicorn src.app:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level info \
    --no-access-log