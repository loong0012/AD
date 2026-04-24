guig"""
启动脚本
使用FastAPI运行阿尔兹海默症诊断系统
"""

import os
import sys
import uvicorn
from src.app import app
from src.utils.helpers import find_available_port
from src.utils.log_manager import log_manager as logger

if __name__ == "__main__":
    # 查找可用端口
    port = find_available_port(8889)
    logger.info(f"Starting Alzheimer Diagnostic System on port {port}")
    logger.info(f"Access address: http://localhost:{port}")
    
    # 启动FastAPI服务器
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
