#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型训练示例脚本
演示如何使用阿尔兹海默症诊断系统进行模型训练
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.train_model import train_model, ADNIDataset, MultiModalADModel
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split

def main():
    """主函数"""
    print("=== 阿尔兹海默症诊断模型训练示例 ===")
    
    # 设备配置
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    # 超参数设置
    batch_size = 2
    lr = 5e-5
    dropout = 0.4
    num_epochs = 50
    patience = 8
    
    # 创建数据集
    print("创建数据集...")
    dataset = ADNIDataset(num_samples=200, use_real_data=False, augment=True)
    
    # 划分训练集和验证集
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(val_dataset)}")
    
    # 创建模型
    print("创建模型...")
    model = MultiModalADModel(dropout=dropout)
    model.to(device)
    
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    
    # 学习率调度器
    scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=10, T_mult=2)
    
    # 训练模型
    print("\n开始训练...")
    train_losses, train_accs, val_losses, val_accs = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        criterion=criterion,
        scheduler=scheduler,
        device=device,
        num_epochs=num_epochs,
        patience=patience
    )
    
    print("\n训练完成!")
    print(f"最佳验证准确率: {max(val_accs):.2f}%")
    
    # 保存最佳模型
    torch.save(model.state_dict(), 'model_best.pth')
    print("模型已保存为: model_best.pth")

if __name__ == '__main__':
    main()
