"""
辅助函数模块 - 提供各种实用工具函数
"""

import socket
import json
import os
from datetime import datetime

def find_available_port(start_port=8888, max_attempts=100):
    """
    查找可用的端口
    :param start_port: 起始端口
    :param max_attempts: 最大尝试次数
    :return: 可用的端口号
    """
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                continue
    raise Exception(f"在端口范围 {start_port} 到 {start_port + max_attempts} 中没有找到可用端口")

def check_port_available(port):
    """
    检查端口是否可用
    :param port: 端口号
    :return: 布尔值
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return True
        except OSError:
            return False

def preprocess_nifti_data(nifti_data):
    """
    预处理NIfTI格式的MRI数据
    :param nifti_data: NIfTI数据
    :return: 预处理后的数据
    """
    # 这里是一个示例实现，实际处理可能更复杂
    import numpy as np
    
    # 假设nifti_data是一个numpy数组
    if isinstance(nifti_data, np.ndarray):
        # 标准化数据
        mean = np.mean(nifti_data)
        std = np.std(nifti_data)
        if std > 0:
            nifti_data = (nifti_data - mean) / std
        
        # 确保数据维度正确
        if len(nifti_data.shape) == 3:
            # 添加批次维度
            nifti_data = np.expand_dims(nifti_data, axis=0)
        elif len(nifti_data.shape) == 4:
            # 已经有批次维度
            pass
        else:
            raise ValueError(f"数据维度不正确: {nifti_data.shape}")
    
    return nifti_data

def save_json_data(data, file_path):
    """
    保存数据到JSON文件
    :param data: 要保存的数据
    :param file_path: 文件路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json_data(file_path):
    """
    从JSON文件加载数据
    :param file_path: 文件路径
    :return: 加载的数据
    """
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def generate_timestamp():
    """
    生成时间戳
    :return: 时间戳字符串
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def ensure_directory(directory):
    """
    确保目录存在
    :param directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True)

def get_file_size(file_path):
    """
    获取文件大小
    :param file_path: 文件路径
    :return: 文件大小（字节）
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0

def format_file_size(size_in_bytes):
    """
    格式化文件大小
    :param size_in_bytes: 字节大小
    :return: 格式化后的大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"