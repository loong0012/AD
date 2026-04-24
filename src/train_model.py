import os
import argparse
import logging
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.cuda.amp import autocast, GradScaler
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model import MultiModalADModel
from config.config import CONFIG
from data.adni_dataset import AugmentedADNIDataset

# 解决OpenMP库冲突问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def train_epoch(model, dataloader, optimizer, criterion, device, scaler=None):
    """训练一个epoch"""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    
    for batch_idx, batch in enumerate(dataloader):
        mri_data = batch['mri'].to(device)
        clinical_features = batch['clinical'].to(device)
        lifestyle_features = batch['lifestyle'].to(device)
        molecular_features = batch['molecular'].to(device)
        labels = batch['label'].to(device)
        
        optimizer.zero_grad()
        
        # 使用混合精度训练
        with autocast():
            class_logits, risk_score, _ = model(
                mri_data, 
                clinical_features, 
                lifestyle_features, 
                molecular_features
            )
            
            loss = criterion(class_logits, labels)
        
        if scaler:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        
        total_loss += loss.item()
        _, predicted = torch.max(class_logits.data, 1)
        total += labels.size(0)
        correct += predicted.eq(labels.data).cpu().sum().item()
        
        # 每10个批次记录一次
        if (batch_idx + 1) % 10 == 0:
            logger.info(f'Batch [{batch_idx}/{len(dataloader)}], Loss: {loss.item():.4f}, Acc: {100.*correct/total:.2f}%')
    
    return total_loss / len(dataloader), 100.*correct/total


def validate_epoch(model, dataloader, criterion, device):
    """验证一个epoch"""
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch in dataloader:
            mri_data = batch['mri'].to(device)
            clinical_features = batch['clinical'].to(device)
            lifestyle_features = batch['lifestyle'].to(device)
            molecular_features = batch['molecular'].to(device)
            labels = batch['label'].to(device)
            
            # 使用混合精度推理
            with autocast():
                class_logits, risk_score, _ = model(
                    mri_data, 
                    clinical_features, 
                    lifestyle_features, 
                    molecular_features
                )
                
                loss = criterion(class_logits, labels)
            
            total_loss += loss.item()
            _, predicted = torch.max(class_logits.data, 1)
            total += labels.size(0)
            correct += predicted.eq(labels.data).cpu().sum().item()
    
    return total_loss / len(dataloader), 100.*correct/total


import signal
import sys
import time

def signal_handler(sig, frame):
    """信号处理函数，用于优雅终止训练"""
    logger.info('收到中断信号，正在保存模型...')
    torch.save(model.state_dict(), 'model_interrupted.pth')
    logger.info('模型已保存为 model_interrupted.pth')
    sys.exit(0)

def main():
    """优化的训练函数，添加异常处理和稳定性"""
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    parser = argparse.ArgumentParser(description='训练优化的多模态阿尔兹海默症诊断模型')
    parser.add_argument('--epochs', type=int, default=300, help='训练轮数（增加训练轮数）')
    parser.add_argument('--batch-size', type=int, default=4, help='批次大小')
    parser.add_argument('--lr', type=float, default=5e-6, help='学习率（降低学习率以促进收敛）')
    parser.add_argument('--dropout', type=float, default=0.3, help='dropout率')
    parser.add_argument('--weight-decay', type=float, default=5e-5, help='权重衰减')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu', help='训练设备')
    parser.add_argument('--resume', type=str, default=None, help='从检查点恢复训练')
    args = parser.parse_args()
    
    logger.info(f'开始训练优化模型，配置: {args}')
    
    # 强制使用GPU（如果可用）
    if torch.cuda.is_available():
        device = torch.device('cuda')
        logger.info(f'检测到GPU: {torch.cuda.get_device_name(0)}')
        logger.info(f'GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024 / 1024 / 1024:.2f} GB')
    else:
        device = torch.device('cpu')
        logger.warning('未检测到GPU，使用CPU训练（速度较慢）')
    
    logger.info(f'使用设备: {device}')
    
    # 创建增强的数据集和数据加载器，使用新上传的augmented_balanced_ADNI_v3数据
    train_dataset = AugmentedADNIDataset(data_dir='./data/augmented_balanced_ADNI_v3', augment=True)
    val_dataset = AugmentedADNIDataset(data_dir='./data/augmented_balanced_ADNI_v3', augment=False)
    
    # 计算训练和验证数据的分割比例
    total_size = len(train_dataset)
    train_size = int(0.8 * total_size)
    val_size = total_size - train_size
    
    # 分割数据集
    train_dataset, val_dataset = torch.utils.data.random_split(
        AugmentedADNIDataset(data_dir='./data/augmented_balanced_ADNI_v3'),
        [train_size, val_size]
    )
    
    # 重新设置增强参数
    train_dataset.dataset.augment = True
    val_dataset.dataset.augment = False
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=4)
    
    logger.info(f'训练数据集大小: {len(train_dataset)}')
    logger.info(f'验证数据集大小: {len(val_dataset)}')
    
    # 创建优化的模型
    model = MultiModalADModel(dropout=args.dropout).to(device)
    logger.info(f'模型创建成功，参数数量: {sum(p.numel() for p in model.parameters())}')
    
    # 定义优化的损失函数和优化器
    criterion = nn.CrossEntropyLoss()  # 去掉标签平滑以简化训练
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, 0.999))
    
    # 添加余弦退火学习率调度器
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-7)
    
    # 初始化混合精度训练的GradScaler
    scaler = GradScaler() if device.type == 'cuda' else None
    
    # 早停机制配置
    patience = 15
    epochs_no_improve = 0
    best_val_acc = 0.0
    
    # 从检查点恢复
    if args.resume:
        try:
            checkpoint = torch.load(args.resume, map_location=device)
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            best_val_acc = checkpoint.get('best_val_acc', 0.0)
            start_epoch = checkpoint.get('epoch', 0)
            logger.info(f'从检查点恢复训练，从epoch {start_epoch} 开始')
        except Exception as e:
            logger.error(f'恢复检查点失败: {e}')
            start_epoch = 0
    else:
        start_epoch = 0
    
    # 训练循环
    for epoch in range(start_epoch, args.epochs):
        logger.info(f'\nEpoch [{epoch+1}/{args.epochs}]')
        
        try:
            # 训练
            train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device, scaler)
            logger.info(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
            
            # 验证
            val_loss, val_acc = validate_epoch(model, val_loader, criterion, device)
            logger.info(f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
            
            # 更新学习率（余弦退火调度）
            scheduler.step()
            
            # 早停机制
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                epochs_no_improve = 0
                # 保存最佳模型
                torch.save(model.state_dict(), f'model_best.pth')
                logger.info(f'保存最佳模型，验证准确率: {best_val_acc:.2f}%')
                
                # 保存完整的最佳检查点
                checkpoint = {
                    'epoch': epoch + 1,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'best_val_acc': best_val_acc,
                    'train_loss': train_loss,
                    'val_loss': val_loss
                }
                torch.save(checkpoint, 'checkpoint_best.pth')
            else:
                epochs_no_improve += 1
                logger.info(f'验证准确率未提升，已连续 {epochs_no_improve} 个epoch')
                
                # 如果连续多个epoch没有提升，提前停止训练
                if epochs_no_improve >= patience:
                    logger.info(f'早停触发，在epoch {epoch+1} 停止训练')
                    break
            
            # 每5个epoch保存检查点
            if (epoch + 1) % 5 == 0:
                checkpoint = {
                    'epoch': epoch + 1,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'best_val_acc': best_val_acc,
                    'train_loss': train_loss,
                    'val_loss': val_loss
                }
                torch.save(checkpoint, f'checkpoint_epoch_{epoch+1}.pth')
                logger.info(f'保存检查点: checkpoint_epoch_{epoch+1}.pth')
            
            # 打印当前学习率
            current_lr = optimizer.param_groups[0]['lr']
            logger.info(f'当前学习率: {current_lr:.6f}')
            
        except Exception as e:
            logger.error(f'Epoch {epoch+1} 训练失败: {e}')
            # 保存当前状态
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_val_acc': best_val_acc
            }, 'model_error.pth')
            logger.info('训练异常，已保存当前状态到 model_error.pth')
            raise
    
    logger.info(f'训练完成！最佳验证准确率: {best_val_acc:.2f}%')


if __name__ == '__main__':
    main()
