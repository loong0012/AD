# API文档

## 1. 模型API

### 1.1 MultiModalADModel

```python
class MultiModalADModel(nn.Module):
    def __init__(self, dropout=0.4):
        """
        初始化多模态阿尔兹海默症诊断模型
        
        参数:
            dropout: dropout率，默认0.4
        """
    
    def forward(self, mri_data, clinical_features=None, lifestyle_features=None, molecular_features=None):
        """
        模型前向传播
        
        参数:
            mri_data: MRI影像数据，形状 [B, 1, 80, 128, 128]
            clinical_features: 临床特征，形状 [B, 15]
            lifestyle_features: 生活方式特征，形状 [B, 12]
            molecular_features: 分子特征，形状 [B, 8]
        
        返回:
            class_logits: 分类输出，形状 [B, 4]
            risk_score: 风险评分，形状 [B, 1]
            fused_features: 融合特征，形状 [B, 512]
        """
```

### 1.2 ADNIDataset

```python
class ADNIDataset(Dataset):
    def __init__(self, num_samples=200, use_real_data=False, augment=True):
        """
        初始化ADNI数据集
        
        参数:
            num_samples: 样本数量，默认200
            use_real_data: 是否使用真实数据，默认False
            augment: 是否进行数据增强，默认True
        """
    
    def __getitem__(self, idx):
        """
        获取数据项
        
        参数:
            idx: 索引
        
        返回:
            包含以下键的字典:
                'mri': MRI数据，形状 [1, 80, 128, 128]
                'clinical': 临床特征，形状 [15]
                'lifestyle': 生活方式特征，形状 [12]
                'molecular': 分子特征，形状 [8]
                'label': 标签，形状 []
        """
```

### 1.3 DataDownloader

```python
class DataDownloader:
    def __init__(self, data_dir='./data'):
        """
        初始化数据下载器
        
        参数:
            data_dir: 数据目录，默认'./data'
        """
    
    def download_real_data(self):
        """下载真实阿尔兹海默症数据"""
    
    def create_real_data_directories(self):
        """创建真实数据目录结构"""
    
    def download_adni_sample(self):
        """下载ADNI样本数据"""
    
    def download_oasis_data(self):
        """下载OASIS数据集"""
    
    def download_kaggle_data(self):
        """下载Kaggle数据集"""
    
    def download_miriad_data(self):
        """下载MIRIAD数据集"""
    
    def download_nacc_data(self):
        """下载NACC数据集"""
    
    def download_adrc_data(self):
        """下载ADRC数据集"""
    
    def download_ucsd_data(self):
        """下载UCSD数据集"""
    
    def download_harvard_data(self):
        """下载Harvard AD数据集"""
```

## 2. 工具函数API

### 2.1 check_gpu.py

```python
def check_gpu_availability():
    """
    检查GPU可用性
    
    返回:
        tuple: (是否有GPU, GPU名称, GPU内存)
    """
```

### 2.2 helpers.py

```python
def set_seed(seed=42):
    """
    设置随机种子
    
    参数:
        seed: 随机种子，默认42
    """

def save_model(model, optimizer, epoch, loss, filename='model_checkpoint.pth'):
    """
    保存模型检查点
    
    参数:
        model: 模型对象
        optimizer: 优化器对象
        epoch: 当前epoch
        loss: 当前损失
        filename: 文件名
    """

def load_model(model, optimizer, filename='model_checkpoint.pth'):
    """
    加载模型检查点
    
    参数:
        model: 模型对象
        optimizer: 优化器对象
        filename: 文件名
    
    返回:
        tuple: (epoch, loss)
    """
```

## 3. 配置API

### 3.1 config.py

```python
CONFIG = {
    'output_classes': ['CN', 'EMCI', 'LMCI', 'AD'],
    'risk_indicators': [
        '海马体萎缩', 'p-tau217浓度', 'Aβ42/Aβ40比率',
        '脑葡萄糖代谢率', '白质高信号', '脑体积减少率'
    ],
    'modalities': [
        '结构MRI (sMRI)', '弥散张量成像 (DTI)', '功能MRI (fMRI)',
        '正电子发射断层扫描 (PET)', '脑脊液生物标志物', '神经心理学评估'
    ]
}
```

## 4. 训练API

### 4.1 train_model.py

```python
def train_epoch(model, dataloader, optimizer, criterion, device):
    """
    训练一个epoch
    
    参数:
        model: 模型对象
        dataloader: 数据加载器
        optimizer: 优化器
        criterion: 损失函数
        device: 设备
    
    返回:
        tuple: (平均损失, 准确率)
    """

def validate_epoch(model, dataloader, criterion, device):
    """
    验证一个epoch
    
    参数:
        model: 模型对象
        dataloader: 数据加载器
        criterion: 损失函数
        device: 设备
    
    返回:
        tuple: (平均损失, 准确率)
    """

def train_model(model, train_loader, val_loader, optimizer, criterion, scheduler, 
                device, num_epochs=50, patience=8):
    """
    训练模型
    
    参数:
        model: 模型对象
        train_loader: 训练数据加载器
        val_loader: 验证数据加载器
        optimizer: 优化器
        criterion: 损失函数
        scheduler: 学习率调度器
        device: 设备
        num_epochs: 训练轮数
        patience: 早停耐心值
    
    返回:
        tuple: (训练损失列表, 训练准确率列表, 验证损失列表, 验证准确率列表)
    """
```

## 5. 命令行接口

### 5.1 数据下载

```bash
# 下载所有真实数据
python utils/data_downloader.py --real

# 下载特定数据集
python utils/data_downloader.py --adni --oasis --kaggle
```

### 5.2 模型训练

```bash
# 使用默认参数训练
python src/train_model.py

# 使用真实数据训练
python src/train_model.py --use-real-data

# 自定义训练参数
python src/train_model.py --epochs 100 --batch-size 4 --lr 1e-4 --dropout 0.3
```

### 5.3 模型测试

```bash
# 运行单元测试
python -m unittest discover tests
```

## 6. 诊断类别说明

| 类别代码 | 类别名称 | 描述 |
|---------|---------|------|
| CN | Cognitive Normal | 认知正常 |
| EMCI | Early Mild Cognitive Impairment | 早期轻度认知障碍 |
| LMCI | Late Mild Cognitive Impairment | 晚期轻度认知障碍 |
| AD | Alzheimer's Disease | 阿尔兹海默症 |

## 7. 数据特征说明

### 7.1 临床特征 (15维)

1. 年龄
2. 性别 (0=男, 1=女)
3. 教育年限
4. MMSE评分 (简易精神状态检查表)
5. CDR评分 (临床痴呆评定量表)
6. 家族史 (0=无, 1=有)
7. APOE ε4基因状态 (0=无, 1=有)
8. 高血压 (0=无, 1=有)
9. 糖尿病 (0=无, 1=有)
10. 心脏病 (0=无, 1=有)
11. 吸烟史 (0=无, 1=有)
12. 饮酒史 (0=无, 1=有)
13. 运动频率 (0-5)
14. BMI指数
15. 抑郁病史 (0=无, 1=有)

### 7.2 生活方式特征 (12维)

1. 每日睡眠时间
2. 每周运动时间(小时)
3. 每日咖啡因摄入量(mg)
4. 每周社交活动次数
5. 每日阅读时间(小时)
6. 每日屏幕时间(小时)
7. 每周户外活动时间(小时)
8. 压力水平 (1-5)
9. 睡眠质量 (1-5)
10. 饮食习惯评分 (1-5)
11. 认知活动频率 (1-5)
12. 社会支持评分 (1-5)

### 7.3 分子特征 (8维)

1. Aβ42浓度
2. Aβ40浓度
3. Aβ42/Aβ40比率
4. p-tau181浓度
5. p-tau217浓度
6. p-tau231浓度
7. 总tau蛋白浓度
8. NFL浓度
```
