"""
数据处理器 - 处理数据加载、预处理和特征提取
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.utils.log_manager import log_manager as logger
from src.utils.config_manager import config_manager


class DataProcessor:
    """数据处理器类 - 处理数据加载和预处理"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
        logger.info("数据处理器初始化完成")
    
    def load_data(self, file_path):
        """
        加载数据文件
        :param file_path: 文件路径
        :return: 加载的数据
        """
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                raise ValueError("不支持的文件格式")
            
            logger.info(f"成功加载数据文件: {file_path}, 数据形状: {data.shape}")
            return data
            
        except Exception as e:
            logger.error(f"数据加载失败: {file_path}", e)
            raise
    
    def preprocess_features(self, features):
        """
        预处理特征数据
        :param features: 特征数据
        :return: 预处理后的特征
        """
        try:
            # 转换为numpy数组
            features_array = np.array(features, dtype=np.float32)
            
            # 标准化处理
            if not self.is_fitted:
                self.scaler.fit(features_array)
                self.is_fitted = True
            
            scaled_features = self.scaler.transform(features_array)
            
            logger.info(f"特征预处理完成，输入形状: {features_array.shape}, 输出形状: {scaled_features.shape}")
            return scaled_features
            
        except Exception as e:
            logger.error("特征预处理失败", e)
            raise
    
    def encode_categorical(self, categorical_data):
        """
        编码分类数据
        :param categorical_data: 分类数据
        :return: 编码后的数据
        """
        try:
            encoded_data = self.label_encoder.fit_transform(categorical_data)
            logger.info(f"分类数据编码完成，类别数量: {len(self.label_encoder.classes_)}")
            return encoded_data
            
        except Exception as e:
            logger.error("分类数据编码失败", e)
            raise
    
    def extract_features_from_files(self, files):
        """
        从文件中提取特征
        :param files: 文件列表
        :return: 提取的特征
        """
        try:
            features = []
            
            for file in files:
                if file.endswith('.csv'):
                    file_features = self._extract_from_csv(file)
                elif file.endswith('.txt'):
                    file_features = self._extract_from_text(file)
                else:
                    logger.warning(f"不支持的文件类型: {file}")
                    continue
                
                features.extend(file_features)
            
            logger.info(f"从文件中提取特征完成，特征数量: {len(features)}")
            return features
            
        except Exception as e:
            logger.error("特征提取失败", e)
            raise
    
    def _extract_from_csv(self, file_path):
        """从CSV文件提取特征"""
        try:
            df = pd.read_csv(file_path)
            # 提取数值列作为特征
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            features = df[numeric_columns].mean().values.tolist()
            return features
            
        except Exception as e:
            logger.error(f"从CSV文件提取特征失败: {file_path}", e)
            return []
    
    def _extract_from_text(self, file_path):
        """从文本文件提取特征"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的文本特征提取
            word_count = len(content.split())
            char_count = len(content)
            line_count = len(content.split('\n'))
            
            features = [word_count, char_count, line_count]
            return features
            
        except Exception as e:
            logger.error(f"从文本文件提取特征失败: {file_path}", e)
            return []
    
    def validate_data(self, data):
        """
        验证数据有效性
        :param data: 要验证的数据
        :return: 验证结果
        """
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': []
            }
            
            # 检查数据是否为空
            if data is None or len(data) == 0:
                validation_result['is_valid'] = False
                validation_result['errors'].append("数据为空")
            
            # 检查数据类型
            if not isinstance(data, (list, np.ndarray)):
                validation_result['is_valid'] = False
                validation_result['errors'].append("数据类型不正确")
            
            # 检查NaN值
            if isinstance(data, np.ndarray):
                if np.isnan(data).any():
                    validation_result['warnings'].append("数据包含NaN值")
            
            logger.info(f"数据验证完成，结果: {validation_result}")
            return validation_result
            
        except Exception as e:
            logger.error("数据验证失败", e)
            return {
                'is_valid': False,
                'errors': [str(e)],
                'warnings': []
            }
