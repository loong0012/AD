#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型推理示例脚本
演示如何使用训练好的模型进行阿尔兹海默症诊断
"""

import sys
import os
import torch
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model import MultiModalADModel
from config.config import CONFIG

def load_model(model_path='checkpoints/model_best.pth'):
    """
    加载训练好的模型
    
    参数:
        model_path: 模型文件路径
    
    返回:
        model: 加载好的模型
    """
    model = MultiModalADModel(dropout=0.4)
    
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(model_path))
    else:
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    
    model.eval()
    return model

def prepare_sample_data():
    """
    准备示例数据
    
    返回:
        dict: 包含MRI、临床、生活方式和分子数据的字典
    """
    # 创建示例MRI数据
    mri_data = torch.randn(1, 1, 80, 128, 128)
    
    # 创建示例临床特征（15维）
    clinical_features = torch.tensor([[72.5, 1, 16, 28, 0.5, 1, 1, 1, 0, 0, 1, 0, 3, 24.5, 0]], dtype=torch.float32)
    
    # 创建示例生活方式特征（12维）
    lifestyle_features = torch.tensor([[7.5, 3.5, 200, 4, 1.5, 3.0, 2.0, 3, 4, 4, 4, 3]], dtype=torch.float32)
    
    # 创建示例分子特征（8维）
    molecular_features = torch.tensor([[500, 2000, 0.25, 80, 45, 60, 300, 1500]], dtype=torch.float32)
    
    return {
        'mri': mri_data,
        'clinical': clinical_features,
        'lifestyle': lifestyle_features,
        'molecular': molecular_features
    }

def predict(model, data):
    """
    使用模型进行预测
    
    参数:
        model: 训练好的模型
        data: 输入数据字典
    
    返回:
        dict: 预测结果
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 将数据移动到设备
    mri_data = data['mri'].to(device)
    clinical_features = data['clinical'].to(device)
    lifestyle_features = data['lifestyle'].to(device)
    molecular_features = data['molecular'].to(device)
    
    # 前向传播
    with torch.no_grad():
        class_logits, risk_score, _ = model(
            mri_data,
            clinical_features,
            lifestyle_features,
            molecular_features
        )
    
    # 获取预测结果
    probabilities = torch.softmax(class_logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    
    return {
        'predicted_class': CONFIG['output_classes'][predicted_class],
        'probabilities': probabilities.cpu().numpy()[0],
        'risk_score': risk_score.cpu().numpy()[0][0],
        'class_logits': class_logits.cpu().numpy()[0]
    }

def main():
    """主函数"""
    print("=== 阿尔兹海默症诊断模型推理示例 ===")
    
    # 加载模型
    print("加载模型...")
    try:
        model = load_model()
        print("模型加载成功!")
    except Exception as e:
        print(f"模型加载失败: {e}")
        print("请确保模型文件存在于指定路径")
        return
    
    # 准备示例数据
    print("\n准备示例数据...")
    data = prepare_sample_data()
    
    # 进行预测
    print("进行预测...")
    result = predict(model, data)
    
    # 显示结果
    print("\n=== 预测结果 ===")
    print(f"预测类别: {result['predicted_class']}")
    print(f"风险评分: {result['risk_score']:.4f}")
    
    print("\n各类别概率:")
    for i, cls in enumerate(CONFIG['output_classes']):
        print(f"  {cls}: {result['probabilities'][i]:.4f}")
    
    # 解释结果
    print("\n=== 结果解释 ===")
    predicted_class = result['predicted_class']
    
    if predicted_class == 'CN':
        print("患者认知功能正常，未检测到阿尔兹海默症风险。")
    elif predicted_class == 'EMCI':
        print("患者处于早期轻度认知障碍阶段，建议定期监测。")
    elif predicted_class == 'LMCI':
        print("患者处于晚期轻度认知障碍阶段，建议进行进一步评估和干预。")
    elif predicted_class == 'AD':
        print("患者已确诊阿尔兹海默症，建议立即进行医疗干预。")
    
    # 风险评估
    risk_score = result['risk_score']
    if risk_score < 0.3:
        print(f"12个月内疾病进展风险较低 ({risk_score:.2f})")
    elif risk_score < 0.7:
        print(f"12个月内疾病进展风险中等 ({risk_score:.2f})")
    else:
        print(f"12个月内疾病进展风险较高 ({risk_score:.2f})")

if __name__ == '__main__':
    main()
