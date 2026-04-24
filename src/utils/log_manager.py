"""
日志管理器 - 统一的日志记录功能
"""

import logging
import os
from datetime import datetime

class LogManager:
    """日志管理器类"""
    
    def __init__(self, name='alzheimer-diagnostic', log_dir='logs'):
        """
        初始化日志管理器
        :param name: 日志名称
        :param log_dir: 日志目录
        """
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成日志文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'{name}_{timestamp}.log')
        
        # 配置根日志
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 清除现有处理器
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 定义日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def info(self, message, *args):
        """记录信息日志"""
        self.logger.info(message, *args)
    
    def error(self, message, *args):
        """记录错误日志"""
        self.logger.error(message, *args)
    
    def warning(self, message, *args):
        """记录警告日志"""
        self.logger.warning(message, *args)
    
    def debug(self, message, *args):
        """记录调试日志"""
        self.logger.debug(message, *args)

# 创建全局日志管理器实例
log_manager = LogManager()