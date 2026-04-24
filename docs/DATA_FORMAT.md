# 数据格式文档

## 1. 数据集概述

本项目使用多模态数据进行阿尔兹海默症诊断，包括MRI影像数据、临床数据、生活方式数据和分子生物标志物数据。

## 2. 数据目录结构

```
data/
├── real/                  # 真实数据集
│   ├── adni/             # ADNI数据集
│   │   ├── mri/          # MRI影像数据
│   │   ├── clinical/     # 临床数据
│   │   ├── molecular/    # 分子生物标志物数据
│   │   └── lifestyle/    # 生活方式数据
│   ├── oasis/            # OASIS数据集
│   │   ├── mri/
│   │   └── clinical/
│   ├── miriad/           # MIRIAD数据集
│   │   └── mri/
│   ├── nacc/             # NACC数据集
│   │   └── clinical/
│   ├── adrc/             # ADRC数据集
│   │   └── clinical/
│   ├── ucsd/             # UCSD数据集
│   │   └── mri/
│   └── harvard/          # Harvard AD数据集
│       └── clinical/
├── processed/            # 处理后的数据
│   ├── mri/
│   ├── clinical/
│   ├── molecular/
│   └── lifestyle/
├── clinical/             # 临床数据
│   ├── clinical_records/ # 临床记录
│   ├── lifestyle_data/  # 生活方式数据
│   ├── molecular_data/  # 分子数据
│   └── neuropsychological/ # 神经心理学评估
├── demo/                # 演示数据
├── uploads/             # 上传文件
└── temp/                # 临时文件
```

## 3. MRI数据格式

### 3.1 数据格式

- **格式**: NIfTI (.nii) 或 NumPy (.npy)
- **形状**: (1, 80, 128, 128)
- **数据类型**: float32
- **预处理**: 
  - 归一化到 [-2, 2] 范围
  - 重采样到统一尺寸
  - 去除偏置场

### 3.2 示例数据

```python
import numpy as np

# 加载MRI数据
mri_data = np.load('data/demo/demo_mri.npy')
print(f"MRI数据形状: {mri_data.shape}")  # (1, 80, 128, 128)
print(f"数据类型: {mri_data.dtype}")      # float32
```

## 4. 临床数据格式

### 4.1 JSON格式

每个患者的临床数据存储为JSON文件，文件名格式: `patient_{id}.json`

```json
{
    "patient_id": "ADNI_001",
    "age": 72.5,
    "gender": 1,
    "education": 16,
    "mmse": 28,
    "cdr": 0.5,
    "family_history": 1,
    "apoe_status": 1,
    "hypertension": 1,
    "diabetes": 0,
    "heart_disease": 0,
    "smoking": 1,
    "alcohol": 0,
    "exercise_frequency": 3,
    "bmi": 24.5,
    "depression": 0,
    "diagnosis": "EMCI",
    "dataset": "adni"
}
```

### 4.2 字段说明

| 字段 | 类型 | 说明 | 范围 |
|------|------|------|------|
| patient_id | string | 患者ID | - |
| age | float | 年龄 | 50-90 |
| gender | int | 性别 (0=男, 1=女) | 0-1 |
| education | int | 教育年限 | 0-25 |
| mmse | float | MMSE评分 | 0-30 |
| cdr | float | CDR评分 | 0-3 |
| family_history | int | 家族史 | 0-1 |
| apoe_status | int | APOE ε4状态 | 0-1 |
| hypertension | int | 高血压 | 0-1 |
| diabetes | int | 糖尿病 | 0-1 |
| heart_disease | int | 心脏病 | 0-1 |
| smoking | int | 吸烟史 | 0-1 |
| alcohol | int | 饮酒史 | 0-1 |
| exercise_frequency | int | 运动频率 | 0-5 |
| bmi | float | BMI指数 | 15-40 |
| depression | int | 抑郁病史 | 0-1 |
| diagnosis | string | 诊断结果 | CN/EMCI/LMCI/AD |
| dataset | string | 数据集来源 | adni/oasis/nacc/adrc/harvard |

## 5. 生活方式数据格式

### 5.1 JSON格式

每个患者的生活方式数据存储为JSON文件，文件名格式: `lifestyle_{id}.json`

```json
{
    "patient_id": "ADNI_001",
    "sleep_hours": 7.5,
    "exercise_hours": 3.5,
    "caffeine_intake": 200,
    "social_activities": 4,
    "reading_hours": 1.5,
    "screen_hours": 3.0,
    "outdoor_hours": 2.0,
    "stress_level": 3,
    "sleep_quality": 4,
    "diet_score": 4,
    "cognitive_activities": 4,
    "social_support": 3,
    "diagnosis": "EMCI",
    "dataset": "adni"
}
```

### 5.2 字段说明

| 字段 | 类型 | 说明 | 范围 |
|------|------|------|------|
| patient_id | string | 患者ID | - |
| sleep_hours | float | 每日睡眠时间 | 4-12 |
| exercise_hours | float | 每周运动时间(小时) | 0-20 |
| caffeine_intake | int | 每日咖啡因摄入量(mg) | 0-500 |
| social_activities | int | 每周社交活动次数 | 0-7 |
| reading_hours | float | 每日阅读时间(小时) | 0-5 |
| screen_hours | float | 每日屏幕时间(小时) | 0-12 |
| outdoor_hours | float | 每周户外活动时间(小时) | 0-20 |
| stress_level | int | 压力水平 | 1-5 |
| sleep_quality | int | 睡眠质量 | 1-5 |
| diet_score | int | 饮食习惯评分 | 1-5 |
| cognitive_activities | int | 认知活动频率 | 1-5 |
| social_support | int | 社会支持评分 | 1-5 |
| diagnosis | string | 诊断结果 | CN/EMCI/LMCI/AD |
| dataset | string | 数据集来源 | adni/oasis/nacc/adrc/harvard |

## 6. 分子生物标志物数据格式

### 6.1 JSON格式

每个患者的分子生物标志物数据存储为JSON文件，文件名格式: `molecular_{id}.json`

```json
{
    "patient_id": "ADNI_001",
    "abeta42": 500,
    "abeta40": 2000,
    "abeta_ratio": 0.25,
    "ptau181": 80,
    "ptau217": 45,
    "ptau231": 60,
    "total_tau": 300,
    "nfl": 1500,
    "diagnosis": "EMCI",
    "dataset": "adni"
}
```

### 6.2 字段说明

| 字段 | 类型 | 说明 | 范围 |
|------|------|------|------|
| patient_id | string | 患者ID | - |
| abeta42 | float | Aβ42浓度(pg/mL) | 0-1000 |
| abeta40 | float | Aβ40浓度(pg/mL) | 0-5000 |
| abeta_ratio | float | Aβ42/Aβ40比率 | 0-1 |
| ptau181 | float | p-tau181浓度(pg/mL) | 0-200 |
| ptau217 | float | p-tau217浓度(pg/mL) | 0-100 |
| ptau231 | float | p-tau231浓度(pg/mL) | 0-150 |
| total_tau | float | 总tau蛋白浓度(pg/mL) | 0-1000 |
| nfl | float | NFL浓度(pg/mL) | 0-5000 |
| diagnosis | string | 诊断结果 | CN/EMCI/LMCI/AD |
| dataset | string | 数据集来源 | adni/oasis/nacc/adrc/harvard |

## 7. 数据预处理流程

### 7.1 MRI数据预处理

1. **重采样**: 将MRI数据重采样到统一尺寸 (80, 128, 128)
2. **归一化**: 将数据归一化到 [-2, 2] 范围
3. **数据增强**: 
   - 添加高斯噪声
   - 随机对比度调整
   - 随机亮度调整
   - 随机翻转

### 7.2 临床数据预处理

1. **缺失值处理**: 使用均值填充缺失值
2. **标准化**: 将数值特征标准化到均值为0，标准差为1
3. **分类特征编码**: 将分类特征转换为one-hot编码

### 7.3 生活方式数据预处理

1. **缺失值处理**: 使用均值填充缺失值
2. **标准化**: 将数值特征标准化到均值为0，标准差为1

### 7.4 分子数据预处理

1. **缺失值处理**: 使用均值填充缺失值
2. **标准化**: 将数值特征标准化到均值为0，标准差为1

## 8. 数据划分

### 8.1 训练集/验证集/测试集划分

- **训练集**: 70%
- **验证集**: 15%
- **测试集**: 15%

### 8.2 划分策略

使用分层抽样确保每个类别在各个数据集中的比例相同。

## 9. 数据质量控制

### 9.1 数据验证

- 检查数据范围是否合理
- 检查缺失值比例
- 检查数据分布是否符合预期

### 9.2 异常值处理

- 使用IQR方法检测异常值
- 对异常值进行截断或替换

## 10. 数据安全与隐私

- 所有患者数据均已匿名化处理
- 敏感信息已被移除或加密
- 严格遵守HIPAA等隐私法规

## 11. 数据更新策略

- 定期下载最新的公开数据集
- 定期更新数据预处理流程
- 定期验证数据质量
```
