# 阿尔茨海默病诊断系统演示数据

本文件夹包含用于演示系统的模拟数据，按照数据类型分类存储。

## 数据分类

### 1. MRI影像数据 (MRI/)
- `patient_001_mri.npy` - 模拟的大脑MRI扫描数据（轻度认知障碍）
- `patient_002_mri.npy` - 模拟的大脑MRI扫描数据（认知正常）
- `patient_003_mri.npy` - 模拟的大脑MRI扫描数据（阿尔茨海默病）
- `patient_004_mri.npy` - 模拟的大脑MRI扫描数据（认知正常）
- `patient_005_mri.npy` - 模拟的大脑MRI扫描数据（重度阿尔茨海默病）
- 格式：NumPy数组 (.npy)
- 说明：包含不同认知状态患者的脑部MRI扫描数据

### 2. 临床数据 (Clinical/)
- `patient_001_clinical.json` - 患者PAT_001的临床信息（轻度认知障碍）
- `patient_002_clinical.json` - 患者PAT_002的临床信息（认知正常）
- `patient_003_clinical.json` - 患者PAT_003的临床信息（阿尔茨海默病）
- `patient_004_clinical.json` - 患者PAT_004的临床信息（认知正常）
- `patient_005_clinical.json` - 患者PAT_005的临床信息（重度阿尔茨海默病）
- 格式：JSON
- 内容：患者基本信息、病史、认知评估分数(MMSE/CDR)、基因信息(APOE)等

### 3. 分子数据 (Molecular/)
- `patient_001_molecular.csv` - 患者PAT_001的生物标志物数据（轻度认知障碍）
- `patient_002_molecular.csv` - 患者PAT_002的生物标志物数据（认知正常）
- `patient_003_molecular.csv` - 患者PAT_003的生物标志物数据（阿尔茨海默病）
- `patient_004_molecular.csv` - 患者PAT_004的生物标志物数据（认知正常）
- `patient_005_molecular.csv` - 患者PAT_005的生物标志物数据（重度阿尔茨海默病）
- 格式：CSV
- 内容：Aβ42、Tau蛋白、pTau蛋白、PET扫描结果、APOE基因型等

### 4. 生活方式数据 (Lifestyle/)
- `patient_001_lifestyle.json` - 患者PAT_001的生活方式信息（中等健康）
- `patient_002_lifestyle.json` - 患者PAT_002的生活方式信息（非常健康）
- `patient_003_lifestyle.json` - 患者PAT_003的生活方式信息（不健康）
- `patient_004_lifestyle.json` - 患者PAT_004的生活方式信息（健康）
- `patient_005_lifestyle.json` - 患者PAT_005的生活方式信息（非常不健康）
- 格式：JSON
- 内容：运动频率、睡眠时长、饮食习惯、社交活动、认知活动、吸烟饮酒情况等

## 使用说明

1. **上传演示**：在系统诊断界面，您可以选择这些文件进行上传演示
2. **多模态诊断**：系统支持同时上传多种类型的数据进行综合分析
3. **数据格式**：所有数据文件都符合系统的输入要求

## 数据说明

- 这些数据是基于真实医学研究的模拟数据
- 患者信息已匿名化处理
- 数据结构与系统诊断模型的输入要求完全匹配
- 可用于演示系统的完整工作流程

## 数据来源说明

- 临床数据基于ADNI（阿尔茨海默病神经影像计划）的标准格式
- 分子数据基于真实的生物标志物检测结果
- 生活方式数据基于流行病学研究的常见模式
- MRI数据结构符合标准的NIfTI格式要求

## 注意事项

- 这些数据仅用于系统演示和测试
- 请勿将模拟数据用于实际临床诊断
- 如需真实数据，请联系相关医学研究机构获取