"""
配置管理器
管理系统配置参数
"""


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config = {
            'project': {
                'name': '阿尔兹海默症诊断系统',
                'version': '3.0.0',
                'release_date': '2024-01-01'
            },
            'diagnosis': {
                'output_classes': ['CN', 'EMCI', 'LMCI', 'AD'],
                'risk_indicators': ['Aβ42', 'p-tau217', 't-tau', 'BMI', 'Hypertension']
            },
            'model': {
                'version': '1.0',
                'input_size': 64,
                'hidden_size': 128,
                'num_classes': 4
            }
        }
    
    def get(self, key, default=None):
        """
        获取配置值
        :param key: 配置键，支持点号分隔的路径
        :param default: 默认值
        :return: 配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self):
        """
        获取所有配置
        :return: 所有配置
        """
        return self.config


# 创建全局配置管理器实例
config_manager = ConfigManager()
CONFIG = config_manager.config
