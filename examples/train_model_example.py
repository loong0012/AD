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

from src.models.model import MultiModalADModel
from src.data.adni_dataset import AugmentedADNIDataset as ADNIDataset
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
    dataset = ADNIDataset(data_dir='./data/augmented_balanced_ADNI_v3', augment=True)
    
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
    
    # 训练循环
    print("\n开始训练...")
    train_losses, train_accs, val_losses, val_accs = [], [], [], []
    best_val_acc = 0.0
    epochs_no_improve = 0

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for batch in train_loader:
            mri_data = batch['mri'].to(device)
            clinical_features = batch['clinical'].to(device)
            lifestyle_features = batch['lifestyle'].to(device)
            molecular_features = batch['molecular'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            class_logits, risk_score, _ = model(
                mri_data, clinical_features, lifestyle_features, molecular_features
            )
            loss = criterion(class_logits, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            _, predicted = torch.max(class_logits.data, 1)
            total += labels.size(0)
            correct += predicted.eq(labels.data).cpu().sum().item()

        train_loss = total_loss / len(train_loader)
        train_acc = 100. * correct / total
        train_losses.append(train_loss)
        train_accs.append(train_acc)

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for batch in val_loader:
                mri_data = batch['mri'].to(device)
                clinical_features = batch['clinical'].to(device)
                lifestyle_features = batch['lifestyle'].to(device)
                molecular_features = batch['molecular'].to(device)
                labels = batch['label'].to(device)

                class_logits, risk_score, _ = model(
                    mri_data, clinical_features, lifestyle_features, molecular_features
                )
                loss = criterion(class_logits, labels)

                val_loss += loss.item()
                _, predicted = torch.max(class_logits.data, 1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels.data).cpu().sum().item()

        val_loss = val_loss / len(val_loader)
        val_acc = 100. * val_correct / val_total
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        scheduler.step()

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        print(f"Epoch {epoch+1}/{num_epochs} - Train Loss: {train_loss:.4f}, "
              f"Train Acc: {train_acc:.2f}%, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")

        if epochs_no_improve >= patience:
            print(f"早停触发，在第 {epoch+1} 轮停止训练")
            break
    
    print("\n训练完成!")
    print(f"最佳验证准确率: {max(val_accs):.2f}%")
    
    # 保存最佳模型
    torch.save(model.state_dict(), 'model_best.pth')
    print("模型已保存为: model_best.pth")

if __name__ == '__main__':
    main()