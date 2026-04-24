"""
配置模块 - 存放所有系统配置参数
"""

import os

# ==================== 配置区域 ====================
CONFIG = {
    'project_name': '基于深度学习的阿尔兹海默症分类与进展预测系统',
    'project_name_en': 'DL-AD-CPredSys',
    'version': '3.0.0',
    'release_date': '2025年10月',
    'port': 6009,
    'input_shape': (1, 1, 160, 256, 256),
    'output_classes': ['CN', 'EMCI', 'LMCI', 'AD'],
    'risk_indicators': [
        '海马体萎缩',
        'p-tau217浓度',
        'Aβ42/Aβ40比率',
        '脑葡萄糖代谢率',
        '白质高信号',
        '脑体积减少率'
    ],
    'modalities': [
        '结构MRI (sMRI)',
        '弥散张量成像 (DTI)',
        '功能MRI (fMRI)',
        '正电子发射断层扫描 (PET)',
        '脑脊液生物标志物',
        '神经心理学评估'
    ]
}

# 目录结构配置
DIRECTORIES = [
    "./uploaded_img",
    "./demodata",
    "./models",
    "./static",
    "./static/images",
    "./static/css",
    "./static/js",
    "./grad_cam_results",
    "./clinical_data",
    "./risk_maps",
    "./results",
    "./reports",
    "./temp"
]

# 模型配置
MODEL_CONFIG = {
    'model_path': "./models/multimodal_ad_model.pth",
    'input_shape': (1, 1, 160, 256, 256),
    'dropout_rate': 0.4,
    'num_modalities': 3,
    'hidden_dim': 256,
    'lstm_hidden_dim': 128
}

# Web服务器配置
SERVER_CONFIG = {
    'host': 'localhost',
    'port': 6008,
    'max_port_attempts': 20,
    'static_dir': './static'
}

# 诊断类别映射
DIAGNOSIS_MAPPING = {
    'CN': {'chinese': '认知正常', 'color': '#10b981', 'icon': '', 'risk': '低风险'},
    'EMCI': {'chinese': '早期轻度认知障碍', 'color': '#f59e0b', 'icon': '', 'risk': '中风险'},
    'LMCI': {'chinese': '晚期轻度认知障碍', 'color': '#f97316', 'icon': '', 'risk': '高风险'},
    'AD': {'chinese': '阿尔茨海默病', 'color': '#ef4444', 'icon': '', 'risk': '极高风险'}
}

# 医学建议模板
MEDICAL_ADVICE = {
    'CN': [
        "认知功能正常，继续保持健康生活方式",
        "建议每年进行一次认知功能筛查",
        "保持地中海式饮食，多摄入Omega-3脂肪酸",
        "每周至少150分钟中等强度运动",
        "参与社交和认知训练活动"
    ],
    'EMCI': [
        "发现早期认知变化，建议密切监测",
        "每6个月进行一次神经心理学评估",
        "开始认知训练，特别是记忆和执行功能",
        "控制血管危险因素（血压、血糖、血脂）",
        "考虑进行ApoE基因检测"
    ],
    'LMCI': [
        "认知功能明显下降，需要积极干预",
        "建议神经科专科就诊",
        "进行全面的生物标志物检测",
        "开始药物和非药物治疗方案",
        "制定长期护理计划"
    ],
    'MCI': [
        "轻度认知障碍，需要定期随访",
        "每3-6个月评估一次认知状态",
        "加强认知康复训练",
        "控制阿尔茨海默病风险因素",
        "建立健康档案，记录认知变化"
    ],
    'AD': [
        "高度怀疑阿尔茨海默病，立即就医",
        "尽快进行PET-CT或脑脊液检查确诊",
        "开始药物治疗（胆碱酯酶抑制剂等）",
        "制定全面的护理和支持计划",
        "参与临床试验和新治疗方案"
    ]
}

# 环境变量
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'