CONFIG = {
    'project': {
        'name': '阿尔兹海默症诊断系统',
        'version': '3.0.0',
    },
    'model': {
        'input_size': 64,
        'hidden_size': 128,
        'num_classes': 4,
        'dropout': 0.3,
    },
    'training': {
        'epochs': 300,
        'batch_size': 4,
        'learning_rate': 5e-6,
        'weight_decay': 5e-5,
        'patience': 15,
    },
    'data': {
        'data_dir': './data/augmented_balanced_ADNI_v3',
        'train_split': 0.8,
    },
    'diagnosis': {
        'output_classes': ['CN', 'EMCI', 'LMCI', 'AD'],
        'risk_indicators': ['Aβ42', 'p-tau217', 't-tau', 'BMI', 'Hypertension'],
    },
}