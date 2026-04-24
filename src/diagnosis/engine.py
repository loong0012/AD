"""
诊断引擎 - 核心诊断逻辑实现
"""

import torch
import numpy as np
from src.utils.model_manager import model_manager
from src.utils.log_manager import log_manager as logger
from src.utils.config_manager import config_manager
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from scipy.ndimage import gaussian_filter
import cv2
import os
import random


class DiagnosisEngine:
    """诊断引擎类 - 处理核心诊断逻辑"""
    
    def __init__(self):
        self.model = model_manager.get_model()
        self.output_classes = config_manager.get('diagnosis.output_classes')
        logger.info("诊断引擎初始化完成")
    
    def predict(self, features):
        """
        执行诊断预测
        :param features: 输入特征向量
        :return: 诊断结果
        """
        try:
            # 将特征转换为张量
            input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            
            # 检查模型是否有eval方法（处理MockModel的情况）
            if hasattr(self.model, 'eval'):
                self.model.eval()
            
            # 执行预测
            try:
                # 尝试使用真实模型的预测方式
                with torch.no_grad():
                    output = self.model(input_tensor)
                    probabilities = torch.softmax(output, dim=1).numpy()[0]
            except (AttributeError, TypeError):
                # 如果是MockModel，使用其预测方法
                mock_result = self.model.predict(input_tensor)
                # 生成模拟的概率分布
                import random
                output_classes = config_manager.get('diagnosis.output_classes')
                probabilities = []
                for cls in output_classes:
                    if cls == mock_result['pred_label']:
                        probabilities.append(mock_result['confidence'])
                    else:
                        probabilities.append((1 - mock_result['confidence']) / (len(output_classes) - 1))
                probabilities = np.array(probabilities)
            
            # 获取预测结果
            predicted_class = np.argmax(probabilities)
            confidence = probabilities[predicted_class]
            
            # 构建结果
            result = {
                'prediction': self.output_classes[predicted_class],
                'confidence': float(confidence),
                'probabilities': {
                    self.output_classes[i]: float(probabilities[i])
                    for i in range(len(self.output_classes))
                }
            }
            
            logger.info(f"诊断完成: {result['prediction']}, 置信度: {confidence:.4f}")
            return result
            
        except Exception as e:
            logger.error("诊断预测失败", e)
            raise
    
    def calculate_risk_score(self, prediction_result):
        """
        计算风险评分
        :param prediction_result: 预测结果
        :return: 风险评分
        """
        try:
            # 根据预测结果计算风险评分
            risk_weights = config_manager.get('diagnosis.risk_weights', {})
            base_score = 0
            
            for class_name, probability in prediction_result['probabilities'].items():
                weight = risk_weights.get(class_name, 1.0)
                base_score += probability * weight
            
            # 归一化到0-100
            risk_score = min(100, max(0, int(base_score * 100)))
            
            logger.info(f"风险评分: {risk_score}")
            return risk_score
            
        except Exception as e:
            logger.error("风险评分计算失败", e)
            raise
    
    def generate_diagnosis_report(self, patient_data, prediction_result):
        """
        生成诊断报告
        :param patient_data: 患者数据
        :param prediction_result: 预测结果
        :return: 诊断报告
        """
        try:
            risk_score = self.calculate_risk_score(prediction_result)
            
            # 获取诊断结果
            diagnosis = prediction_result.get('diagnosis', prediction_result.get('prediction', 'CN'))
            
            # 生成每月进展风险数据
            monthly_risk = self._generate_monthly_risk(risk_score, diagnosis)
            
            # 生成关键风险指标
            risk_indicators = self._generate_risk_indicators(prediction_result, patient_data)
            
            # 导入datetime模块获取当前时间戳
            from datetime import datetime
            
            # 生成脑部图像
            brain_image = self._generate_brain_image(diagnosis, risk_indicators, patient_data=patient_data)
            
            # 生成热力图
            heatmap_image = self._generate_heatmap(diagnosis, risk_indicators, patient_data=patient_data)
            
            report = {
                'patient_info': patient_data,
                'diagnosis': prediction_result['prediction'],
                'confidence': prediction_result['confidence'],
                'risk_score': risk_score,
                'probabilities': prediction_result['probabilities'],
                'recommendations': self._generate_recommendations(risk_score),
                'monthly_risk': monthly_risk,
                'risk_indicators': risk_indicators,
                'brain_image': brain_image,
                'heatmap_image': heatmap_image,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info("诊断报告生成完成")
            return report
            
        except Exception as e:
            logger.error("诊断报告生成失败", e)
            raise
    
    def _generate_monthly_risk(self, base_risk, diagnosis=None):
        """
        生成未来12个月的进展风险数据
        :param base_risk: 基础风险评分
        :param diagnosis: 诊断结果
        :return: 每月风险数据列表
        """
        try:
            monthly_risk = []
            
            # 根据诊断结果设置初始风险值和增长速率
            if diagnosis == 'AD':
                # 阿尔茨海默病：初始风险高，增长快
                current_risk = max(0.7, base_risk / 100)  # 转换为0-1范围，最低70%
                risk_increase_rate = 0.15  # 12个月后风险增加15%
            elif diagnosis == 'LMCI':
                # 晚期轻度认知障碍：初始风险中等偏高，增长较快
                current_risk = max(0.5, base_risk / 100)  # 转换为0-1范围，最低50%
                risk_increase_rate = 0.12  # 12个月后风险增加12%
            elif diagnosis == 'EMCI':
                # 早期轻度认知障碍：初始风险中等，增长适中
                current_risk = max(0.3, base_risk / 100)  # 转换为0-1范围，最低30%
                risk_increase_rate = 0.10  # 12个月后风险增加10%
            else:  # CN
                # 认知正常：初始风险低，增长慢
                current_risk = min(0.2, base_risk / 100)  # 转换为0-1范围，最高20%
                risk_increase_rate = 0.05  # 12个月后风险增加5%
            
            for month in range(1, 13):
                # 基于基础风险生成每月风险，加入一些随机波动
                # 风险随时间逐渐增加
                risk_increase = month / 12 * risk_increase_rate  # 根据诊断结果调整增长速率
                random_factor = np.random.uniform(0.95, 1.05)  # 5%的随机波动
                monthly_risk_value = min(0.99, current_risk + risk_increase) * random_factor
                
                monthly_risk.append({
                    'month': month,
                    'risk': monthly_risk_value
                })
            
            return monthly_risk
            
        except Exception as e:
            logger.error("生成月度风险数据失败", e)
            # 返回默认数据
            return [{'month': i, 'risk': base_risk / 100} for i in range(1, 13)]
    
    def _generate_risk_indicators(self, prediction_result, patient_data):
        """
        生成关键风险指标
        :param prediction_result: 预测结果
        :param patient_data: 患者数据
        :return: 风险指标字典
        """
        try:
            # 基础风险指标 - 与前端indicatorDescriptions匹配
            indicators = {
                '海马体萎缩': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 2), 'medium': (2, 5), 'high': (5, 10)},
                    'unit': '%/年'
                },
                'p-tau217浓度': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 3.8), 'medium': (3.8, 8), 'high': (8, 20)},
                    'unit': 'pg/mL'
                },
                'Aβ42/Aβ40比率': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0.2, 0.4), 'medium': (0.15, 0.2), 'high': (0, 0.15)},
                    'unit': ''
                },
                '脑葡萄糖代谢率': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (15, 20), 'medium': (10, 15), 'high': (5, 10)},
                    'unit': 'mg/100g/min'
                },
                '白质高信号': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 1), 'medium': (1, 3), 'high': (3, 10)},
                    'unit': 'mL'
                },
                '脑体积减少率': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0.5, 1), 'medium': (1, 2), 'high': (2, 5)},
                    'unit': '%/年'
                },
                'MRI脑萎缩程度': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 5), 'medium': (5, 15), 'high': (15, 30)},
                    'unit': '%'
                },
                '脑脊液Aβ42水平': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (500, 1000), 'medium': (300, 500), 'high': (100, 300)},
                    'unit': 'pg/mL'
                },
                '脑脊液Tau蛋白': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 200), 'medium': (200, 400), 'high': (400, 800)},
                    'unit': 'pg/mL'
                },
                '海马体积': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (7, 10), 'medium': (5, 7), 'high': (3, 5)},
                    'unit': 'cm³'
                },
                '前额叶皮层厚度': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (2.5, 3.5), 'medium': (2, 2.5), 'high': (1.5, 2)},
                    'unit': 'mm'
                },
                '认知评分': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (26, 30), 'medium': (20, 26), 'high': (0, 20)},
                    'unit': '分'
                },
                'APOE基因风险': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 1), 'medium': (1, 2), 'high': (2, 4)},
                    'unit': '分'
                },
                '年龄风险因子': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 65), 'medium': (65, 75), 'high': (75, 100)},
                    'unit': '岁'
                },
                '生活方式风险': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 2), 'medium': (2, 4), 'high': (4, 10)},
                    'unit': '分'
                },
                '血管风险因素': {
                    'value': 0,
                    'risk_level': 'low',
                    'range': {'normal': (0, 1), 'medium': (1, 3), 'high': (3, 5)},
                    'unit': '分'
                }
            }
            
            # 获取预测结果和患者数据
            diagnosis = prediction_result.get('diagnosis', prediction_result.get('prediction', 'CN'))
            confidence = prediction_result['confidence']
            
            # 提取患者数据
            age = int(patient_data.get('age', 65))
            gender = patient_data.get('gender', 'male')
            lifestyle = patient_data.get('lifestyle', {})
            
            # 计算生活方式风险分数
            lifestyle_score = self._calculate_lifestyle_risk(lifestyle)
            
            # 计算血管风险分数
            vascular_score = self._calculate_vascular_risk(patient_data)
            
            # 生成APOE基因风险（基于年龄和家族史）
            apoe_risk = self._calculate_apoe_risk(patient_data)
            
            # 根据诊断结果和患者数据生成指标值
            for indicator_name, indicator in indicators.items():
                # 根据诊断结果设置基础范围
                if diagnosis == 'CN':
                    base_range = indicator['range']['normal']
                elif diagnosis == 'EMCI':
                    base_range = indicator['range']['medium']
                elif diagnosis == 'LMCI':
                    # 对于LMCI，使用medium到high之间的范围
                    base_range = ((indicator['range']['medium'][0] + indicator['range']['high'][0])/2, indicator['range']['high'][1])
                elif diagnosis == 'AD':
                    base_range = indicator['range']['high']
                else:
                    base_range = indicator['range']['normal']
                
                # 生成基础值
                base_value = np.random.uniform(base_range[0], base_range[1])
                
                # 根据患者具体情况调整
                if indicator_name == '年龄风险因子':
                    # 直接使用患者年龄
                    value = age
                elif indicator_name == '生活方式风险':
                    # 使用计算的生活方式风险分数
                    value = lifestyle_score
                elif indicator_name == '血管风险因素':
                    # 使用计算的血管风险分数
                    value = vascular_score
                elif indicator_name == 'APOE基因风险':
                    # 使用计算的APOE基因风险
                    value = apoe_risk
                else:
                    # 其他指标根据基础值和置信度调整
                    value = base_value * (0.8 + 0.4 * confidence)
                
                # 确保值在合理范围内
                min_value = min(indicator['range']['normal'][0], indicator['range']['medium'][0], indicator['range']['high'][0])
                max_value = max(indicator['range']['normal'][1], indicator['range']['medium'][1], indicator['range']['high'][1])
                value = max(min_value, min(max_value, value))
                
                # 确定风险水平
                if indicator_name == 'Aβ42/Aβ40比率' or indicator_name == '脑葡萄糖代谢率' or indicator_name == '脑脊液Aβ42水平' or indicator_name == '认知评分':
                    # 这些指标值越低风险越高
                    if value >= indicator['range']['normal'][0]:
                        risk_level = 'low'
                    elif value >= indicator['range']['medium'][0]:
                        risk_level = 'medium'
                    else:
                        risk_level = 'high'
                else:
                    # 其他指标值越高风险越高
                    if value <= indicator['range']['normal'][1]:
                        risk_level = 'low'
                    elif value <= indicator['range']['medium'][1]:
                        risk_level = 'medium'
                    else:
                        risk_level = 'high'
                
                # 更新指标值和风险水平
                indicators[indicator_name]['value'] = value
                indicators[indicator_name]['risk_level'] = risk_level
            
            # 转换为前端需要的格式（包含range和unit信息）
            result = {}
            for indicator_name, indicator in indicators.items():
                result[indicator_name] = {
                    'value': indicator['value'],
                    'risk_level': indicator['risk_level'],
                    'range': indicator['range'],
                    'unit': indicator['unit']
                }
            
            return result
            
        except Exception as e:
            logger.error("生成风险指标失败", e)
            # 返回默认数据
            return {
                '海马体萎缩': {'value': 1.5, 'risk_level': 'low', 'range': {'normal': (0, 2), 'medium': (2, 5), 'high': (5, 10)}, 'unit': '%/年'},
                'p-tau217浓度': {'value': 3.0, 'risk_level': 'low', 'range': {'normal': (0, 3.8), 'medium': (3.8, 8), 'high': (8, 20)}, 'unit': 'pg/mL'},
                'Aβ42/Aβ40比率': {'value': 0.25, 'risk_level': 'low', 'range': {'normal': (0.2, 0.4), 'medium': (0.15, 0.2), 'high': (0, 0.15)}, 'unit': ''},
                '脑葡萄糖代谢率': {'value': 18.0, 'risk_level': 'low', 'range': {'normal': (15, 20), 'medium': (10, 15), 'high': (5, 10)}, 'unit': 'mg/100g/min'},
                '白质高信号': {'value': 0.5, 'risk_level': 'low', 'range': {'normal': (0, 1), 'medium': (1, 3), 'high': (3, 10)}, 'unit': 'mL'},
                '脑体积减少率': {'value': 0.8, 'risk_level': 'low', 'range': {'normal': (0.5, 1), 'medium': (1, 2), 'high': (2, 5)}, 'unit': '%/年'},
                'MRI脑萎缩程度': {'value': 3.0, 'risk_level': 'low', 'range': {'normal': (0, 5), 'medium': (5, 15), 'high': (15, 30)}, 'unit': '%'},
                '脑脊液Aβ42水平': {'value': 600.0, 'risk_level': 'low', 'range': {'normal': (500, 1000), 'medium': (300, 500), 'high': (100, 300)}, 'unit': 'pg/mL'},
                '脑脊液Tau蛋白': {'value': 150.0, 'risk_level': 'low', 'range': {'normal': (0, 200), 'medium': (200, 400), 'high': (400, 800)}, 'unit': 'pg/mL'},
                '海马体积': {'value': 8.5, 'risk_level': 'low', 'range': {'normal': (7, 10), 'medium': (5, 7), 'high': (3, 5)}, 'unit': 'cm³'},
                '前额叶皮层厚度': {'value': 3.0, 'risk_level': 'low', 'range': {'normal': (2.5, 3.5), 'medium': (2, 2.5), 'high': (1.5, 2)}, 'unit': 'mm'},
                '认知评分': {'value': 28.0, 'risk_level': 'low', 'range': {'normal': (26, 30), 'medium': (20, 26), 'high': (0, 20)}, 'unit': '分'},
                'APOE基因风险': {'value': 1.0, 'risk_level': 'low', 'range': {'normal': (0, 1), 'medium': (1, 2), 'high': (2, 4)}, 'unit': '分'},
                '年龄风险因子': {'value': 65.0, 'risk_level': 'low', 'range': {'normal': (0, 65), 'medium': (65, 75), 'high': (75, 100)}, 'unit': '岁'},
                '生活方式风险': {'value': 1.5, 'risk_level': 'low', 'range': {'normal': (0, 2), 'medium': (2, 4), 'high': (4, 10)}, 'unit': '分'},
                '血管风险因素': {'value': 0.5, 'risk_level': 'low', 'range': {'normal': (0, 1), 'medium': (1, 3), 'high': (3, 5)}, 'unit': '分'}
            }
    
    def _calculate_lifestyle_risk(self, lifestyle):
        """
        计算生活方式风险分数
        :param lifestyle: 生活方式数据
        :return: 生活方式风险分数 (0-10)
        """
        score = 0
        
        # 运动频率（0-7次/周）
        exercise = int(lifestyle.get('exercise_frequency', 3))
        if exercise < 2:
            score += 2
        elif exercise < 4:
            score += 1
        
        # 睡眠时长（4-12小时）
        sleep = float(lifestyle.get('sleep_duration', 7))
        if sleep < 6 or sleep > 9:
            score += 2
        
        # 饮食健康频率
        diet = lifestyle.get('diet_health', 'medium')
        if diet == 'low':
            score += 2
        elif diet == 'medium':
            score += 1
        
        # 社交活动（0-10次/周）
        social = int(lifestyle.get('social_activities', 2))
        if social < 1:
            score += 2
        elif social < 3:
            score += 1
        
        # 吸烟状况
        smoking = lifestyle.get('smoking_status', 'never')
        if smoking == 'current':
            score += 3
        elif smoking == 'past':
            score += 1
        
        # 饮酒频率
        alcohol = lifestyle.get('alcohol_consumption', 'occasional')
        if alcohol == 'regular':
            score += 2
        elif alcohol == 'occasional':
            score += 0.5
        
        # 认知活动
        cognitive = lifestyle.get('cognitive_activities', '')
        if not cognitive:
            score += 1
        
        # 确保分数在0-10范围内
        return min(10, max(0, score))
    
    def _calculate_vascular_risk(self, patient_data):
        """
        计算血管风险分数
        :param patient_data: 患者数据
        :return: 血管风险分数 (0-5)
        """
        score = 0
        
        # 年龄因素
        age = int(patient_data.get('age', 65))
        if age > 70:
            score += 1
        
        # 性别因素（男性风险略高）
        gender = patient_data.get('gender', 'male')
        if gender == 'male':
            score += 0.5
        
        # 家族史
        family_history = patient_data.get('family_history', '')
        if '高血压' in family_history or '糖尿病' in family_history or '心脏病' in family_history:
            score += 1
        
        # 主要病史
        clinical_history = patient_data.get('clinical_history', '')
        if '高血压' in clinical_history:
            score += 1
        if '糖尿病' in clinical_history:
            score += 1
        if '心脏病' in clinical_history:
            score += 1
        
        # 确保分数在0-5范围内
        return min(5, max(0, score))
    
    def _calculate_apoe_risk(self, patient_data):
        """
        计算APOE基因风险
        :param patient_data: 患者数据
        :return: APOE基因风险分数 (0-4)
        """
        score = 1  # 基础风险
        
        # 年龄因素
        age = int(patient_data.get('age', 65))
        if age > 75:
            score += 1
        
        # 家族史
        family_history = patient_data.get('family_history', '')
        if '阿尔兹海默' in family_history or '老年痴呆' in family_history:
            score += 2
        
        # 确保分数在0-4范围内
        return min(4, max(0, score))
    
    def _generate_recommendations(self, risk_score):
        """
        根据风险评分生成建议
        :param risk_score: 风险评分
        :return: 建议列表
        """
        try:
            recommendations = []
            
            if risk_score< 30:
                recommendations.extend([
                    "风险较低，建议保持健康生活方式",
                    "定期进行认知功能检查",
                    "保持社交活动和智力刺激"
                ])
            elif risk_score < 60:
                recommendations.extend([
                    "中等风险，建议加强监测",
                    "考虑咨询神经科医生",
                    "进行更详细的认知评估",
                    "优化生活方式，包括饮食和运动"
                ])
            else:
                recommendations.extend([
                    "高风险，建议立即就医",
                    "咨询神经科专家进行全面评估",
                    "考虑进行进一步的影像学检查",
                    "制定个性化的干预计划"
                ])
            
            return recommendations
            
        except Exception as e:
            logger.error("建议生成失败", e)
            return ["无法生成建议，请咨询专业医生"]
    
    def _generate_brain_image(self, diagnosis, risk_indicators, show_original=False, patient_data=None):
        """
        生成脑部图像，标记出患病点
        :param diagnosis: 诊断结果
        :param risk_indicators: 风险指标
        :param show_original: 是否显示原始MRI影像
        :param patient_data: 患者数据（包含上传的图像路径信息）
        :return: 图像的base64编码
        """
        try:
            import os
            import numpy as np
            import cv2
            import random
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            
            img = None
            image_source = "合成图像"
            
            # 优先使用患者上传的图像
            if patient_data and 'uploaded_image_path' in patient_data:
                uploaded_path = patient_data['uploaded_image_path']
                if os.path.exists(uploaded_path):
                    logger.info(f"使用患者上传的图像: {uploaded_path}")
                    img = cv2.imread(uploaded_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        image_source = "患者上传的MRI图像"
            
            # 如果没有患者上传的图像，尝试从augmented_balanced_ADNI_v3目录加载
            if img is None:
                adni_dir = './data/augmented_balanced_ADNI_v3'
                diagnosis_folder_map = {
                    'AD': 'AD',
                    'LMCI': 'LMCI',
                    'EMCI': 'EMCI',
                    'CN': 'CN'
                }
                
                folder = diagnosis_folder_map.get(diagnosis, 'CN')
                diagnosis_dir = os.path.join(adni_dir, folder)
                
                if os.path.exists(diagnosis_dir):
                    image_files = [f for f in os.listdir(diagnosis_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
                    if image_files:
                        # 随机选择一张图像
                        random.seed()
                        selected_image = random.choice(image_files)
                        image_path = os.path.join(diagnosis_dir, selected_image)
                        logger.info(f"使用ADNI真实图像: {image_path}")
                        img = cv2.imread(image_path)
                        if img is not None:
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            image_source = "ADNI数据库MRI图像"
            
            # 如果找到了图像，创建带标记的图像
            if img is not None:
                # 创建matplotlib图像
                fig, ax = plt.subplots(figsize=(10, 8))
                ax.imshow(img)
                
                # 如果不是显示原始影像，则标记患病点
                if not show_original:
                    h, w = img.shape[:2]
                    
                    # 根据诊断结果和风险指标标记患病点
                    if diagnosis == 'AD':
                        # 阿尔茨海默病：标记多个区域（高风险-红色）
                        # 标记海马体区域（大脑中部两侧）
                        hippocampus_radius = int(min(h, w) * 0.1)
                        ax.add_patch(patches.Circle((w//4, h//2), hippocampus_radius, facecolor='red', edgecolor='darkred', linewidth=2, alpha=0.5))
                        ax.add_patch(patches.Circle((3*w//4, h//2), hippocampus_radius, facecolor='red', edgecolor='darkred', linewidth=2, alpha=0.5))
                        
                        # 标记前额叶区域（顶部）
                        prefrontal_width = int(w * 0.4)
                        prefrontal_height = int(h * 0.25)
                        ax.add_patch(patches.Rectangle((w//2 - prefrontal_width//2, h - prefrontal_height - 10), prefrontal_width, prefrontal_height, facecolor='red', edgecolor='darkred', linewidth=2, alpha=0.5))
                        
                        # 标记颞叶区域（中部两侧）
                        temporal_radius = int(min(h, w) * 0.12)
                        ax.add_patch(patches.Ellipse((w//5, h//2), temporal_radius, int(temporal_radius*1.6), facecolor='orange', edgecolor='darkorange', linewidth=2, alpha=0.4))
                        ax.add_patch(patches.Ellipse((4*w//5, h//2), temporal_radius, int(temporal_radius*1.6), facecolor='orange', edgecolor='darkorange', linewidth=2, alpha=0.4))
                        
                        # 标记顶叶区域
                        parietal_width = int(w * 0.2)
                        parietal_height = int(h * 0.25)
                        ax.add_patch(patches.Rectangle((w//2 - parietal_width//2, h//2 - parietal_height//2), parietal_width, parietal_height, facecolor='darkred', edgecolor='darkred', linewidth=2, alpha=0.3))
                        
                        # 添加关键脑区文字标注
                        ax.annotate('海马体\n(萎缩)', xy=(w//4, h//2), xytext=(w//4 - 60, h//2 - 80),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('海马体\n(萎缩)', xy=(3*w//4, h//2), xytext=(3*w//4 + 20, h//2 - 80),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('颞叶\n(病变)', xy=(w//5, h//2), xytext=(w//5 - 80, h//2 + 50),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='orange', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('颞叶\n(病变)', xy=(4*w//5, h//2), xytext=(4*w//5 + 20, h//2 + 50),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='orange', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('前额叶\n(萎缩)', xy=(w//2, h - prefrontal_height//2), xytext=(w//2 + 80, h - prefrontal_height - 30),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('顶叶\n(受累)', xy=(w//2, h//2), xytext=(w//2 - 80, h//2 - 60),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        
                    elif diagnosis == 'LMCI':
                        # 晚期轻度认知障碍：中等风险区域（黄色）
                        hippocampus_radius = int(min(h, w) * 0.06)
                        ax.add_patch(patches.Circle((w//4, h//2), hippocampus_radius, facecolor='yellow', edgecolor='olive', linewidth=2, alpha=0.5))
                        ax.add_patch(patches.Circle((3*w//4, h//2), hippocampus_radius, facecolor='yellow', edgecolor='olive', linewidth=2, alpha=0.5))
                        
                        # 颞叶区域
                        temporal_radius = int(min(h, w) * 0.08)
                        ax.add_patch(patches.Ellipse((w//5, h//2), temporal_radius, int(temporal_radius*1.3), facecolor='yellow', edgecolor='olive', linewidth=2, alpha=0.4))
                        ax.add_patch(patches.Ellipse((4*w//5, h//2), temporal_radius, int(temporal_radius*1.3), facecolor='yellow', edgecolor='olive', linewidth=2, alpha=0.4))
                        
                        # 添加关键脑区文字标注
                        ax.annotate('海马体\n(轻度萎缩)', xy=(w//4, h//2), xytext=(w//4 - 70, h//2 - 70),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#b8860b', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('海马体\n(轻度萎缩)', xy=(3*w//4, h//2), xytext=(3*w//4 + 10, h//2 - 70),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#b8860b', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('颞叶\n(轻度病变)', xy=(w//5, h//2), xytext=(w//5 - 80, h//2 + 40),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#b8860b', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('颞叶\n(轻度病变)', xy=(4*w//5, h//2), xytext=(4*w//5 + 20, h//2 + 40),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#b8860b', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        
                    elif diagnosis == 'EMCI':
                        # 早期轻度认知障碍：低风险区域（浅黄色/绿色）
                        hippocampus_radius = int(min(h, w) * 0.04)
                        ax.add_patch(patches.Circle((w//4, h//2), hippocampus_radius, facecolor='#90EE90', edgecolor='green', linewidth=2, alpha=0.5))
                        ax.add_patch(patches.Circle((3*w//4, h//2), hippocampus_radius, facecolor='#90EE90', edgecolor='green', linewidth=2, alpha=0.5))
                        
                        # 添加关键脑区文字标注
                        ax.annotate('海马体\n(轻微改变)', xy=(w//4, h//2), xytext=(w//4 - 75, h//2 - 60),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='green', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        ax.annotate('海马体\n(轻微改变)', xy=(3*w//4, h//2), xytext=(3*w//4 + 5, h//2 - 60),
                                   fontsize=12, color='white', fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='green', alpha=0.9),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                        
                    # 添加标签
                    ax.set_title('脑部图像分析 - 关键脑区标注', fontsize=16, fontweight='bold', color='#1e40af')
                    diagnosis_labels = {'AD': '阿尔茨海默病', 'LMCI': '晚期轻度认知障碍', 'EMCI': '早期轻度认知障碍', 'CN': '认知正常'}
                    ax.text(w//2, 30, f'诊断结果: {diagnosis_labels.get(diagnosis, diagnosis)}', ha='center', fontsize=14, color='white', fontweight='bold', bbox=dict(facecolor='black', alpha=0.7))
                    
                    # 添加图例
                    if diagnosis != 'CN':
                        legend_elements = []
                        if diagnosis == 'AD':
                            legend_elements = [
                                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=15, label='海马体病变 (高风险)', markeredgecolor='darkred'),
                                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='orange', markersize=15, label='颞叶病变 (高风险)', markeredgecolor='darkorange'),
                                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='darkred', markersize=15, label='前额叶/顶叶病变', markeredgecolor='darkred')
                            ]
                        elif diagnosis == 'LMCI':
                            legend_elements = [
                                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=15, label='海马体病变 (中风险)', markeredgecolor='olive'),
                                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='yellow', markersize=15, label='颞叶病变 (中风险)', markeredgecolor='olive')
                            ]
                        elif diagnosis == 'EMCI':
                            legend_elements = [
                                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#90EE90', markersize=15, label='轻度海马体改变 (低风险)', markeredgecolor='green')
                            ]
                        ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)
                    else:
                        # 显示原始MRI影像
                        ax.set_title('原始MRI影像', fontsize=16, fontweight='bold', color='#1e40af')
                    
                    # 添加图像来源说明
                    plt.figtext(0.5, 0.02, f'图像来源: {image_source} | 数据类型: 核磁共振成像 (MRI)', 
                               ha='center', fontsize=10, color='#666666')
                    
                    # 关闭坐标轴
                    ax.axis('off')
                    
                    # 保存图像到内存
                    buf = BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight')
                    buf.seek(0)
                    
                    # 转换为base64编码
                    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    
                    # 关闭图像
                    plt.close(fig)
                    
                    return image_base64
            
            # 如果没有找到任何图像文件，返回None
            logger.warning("未找到任何可用图像")
            return None
            
        except Exception as e:
            logger.error("生成脑部图像失败", e)
            return None
    
    def _generate_heatmap(self, diagnosis, risk_indicators, patient_data=None):
        """
        生成脑区风险热力图
        :param diagnosis: 诊断结果
        :param risk_indicators: 风险指标
        :param patient_data: 患者数据（包含上传的图像路径信息）
        :return: 热力图的base64编码
        """
        try:
            import os
            import numpy as np
            import cv2
            import random
            from PIL import Image
            from scipy.ndimage import gaussian_filter
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            
            # 创建热力图 - 3个视角
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            
            # 定义不同视角的标题
            views = ['横断面视图', '矢状面视图', '冠状面视图']
            view_descriptions = ['水平切面，显示大脑顶部结构', '垂直切面，显示大脑侧面结构', '前后切面，显示大脑正面结构']
            
            # 尝试加载图像
            img = None
            image_source = "合成图像"
            
            # 优先使用患者上传的图像
            if patient_data and 'uploaded_image_path' in patient_data:
                uploaded_path = patient_data['uploaded_image_path']
                if os.path.exists(uploaded_path):
                    logger.info(f"使用患者上传的图像生成热力图: {uploaded_path}")
                    img = cv2.imread(uploaded_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        image_source = "患者上传的MRI图像"
            
            # 如果没有患者上传的图像，从ADNI目录加载
            if img is None:
                adni_dir = './data/augmented_balanced_ADNI_v3'
                diagnosis_folder_map = {
                    'AD': 'AD',
                    'LMCI': 'LMCI',
                    'EMCI': 'EMCI',
                    'CN': 'CN'
                }
                
                folder = diagnosis_folder_map.get(diagnosis, 'CN')
                diagnosis_dir = os.path.join(adni_dir, folder)
                
                if os.path.exists(diagnosis_dir):
                    image_files = [f for f in os.listdir(diagnosis_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
                    if image_files:
                        # 随机选择一张图像
                        random.seed()
                        selected_image = random.choice(image_files)
                        image_path = os.path.join(diagnosis_dir, selected_image)
                        logger.info(f"使用ADNI真实图像生成热力图: {image_path}")
                        img = cv2.imread(image_path)
                        if img is not None:
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            image_source = "ADNI数据库MRI图像"
            
            # 为每个视角创建热力图
            for i, view in enumerate(views):
                ax = axes[i]
                
                if img is not None:
                    # 调整图像大小
                    img_resized = cv2.resize(img, (400, 300))
                    h, w, _ = img_resized.shape
                    
                    # 根据视角类型生成不同的切片
                    if i == 0:  # 横断面（水平切面）
                        # 模拟水平切面 - 中间区域
                        slice_img = img_resized.copy()
                        
                    elif i == 1:  # 矢状面（侧面）
                        # 模拟矢状面 - 垂直切片
                        center_col = w // 2
                        slice_img = np.zeros((h, w, 3), dtype=np.uint8)
                        # 创建矢状面效果
                        for y in range(h):
                            for x in range(w):
                                # 模拟深度信息
                                depth = abs(x - center_col) / (w // 2)
                                intensity = 1 - depth * 0.7
                                slice_img[y, x] = img_resized[y, center_col] * intensity
                        
                    else:  # 冠状面（前后切面）
                        # 模拟冠状面 - 前后切片
                        center_row = h // 2
                        slice_img = np.zeros((h, w, 3), dtype=np.uint8)
                        # 创建冠状面效果
                        for y in range(h):
                            for x in range(w):
                                # 模拟深度信息
                                depth = abs(y - center_row) / (h // 2)
                                intensity = 1 - depth * 0.7
                                slice_img[y, x] = img_resized[center_row, x] * intensity
                    
                    ax.imshow(slice_img)
                    
                    # 根据诊断结果和风险指标生成热力图
                    risk_scores = self._calculate_risk_scores(risk_indicators, diagnosis)
                    
                    # 生成热力图叠加
                    heatmap = self._generate_heatmap_overlay(slice_img, risk_scores, i)
                    ax.imshow(heatmap, alpha=0.6, cmap='jet')
                    
                else:
                    # 如果没有图像，创建合成大脑图像
                    h, w = 300, 400
                    slice_img = np.zeros((h, w, 3), dtype=np.uint8)
                    
                    # 生成大脑轮廓
                    center_x, center_y = w // 2, h // 2
                    radius = min(w, h) // 3
                    
                    # 绘制大脑轮廓
                    for y in range(h):
                        for x in range(w):
                            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                            if distance < radius:
                                # 大脑内部
                                slice_img[y, x] = [100, 100, 150]  # 灰色
                            elif distance < radius + 5:
                                # 大脑边界
                                slice_img[y, x] = [150, 150, 200]
                    
                    ax.imshow(slice_img)
                    
                    # 生成热力图叠加
                    risk_scores = self._calculate_risk_scores(risk_indicators, diagnosis)
                    heatmap = self._generate_heatmap_overlay(slice_img, risk_scores, i)
                    ax.imshow(heatmap, alpha=0.6, cmap='jet')
                
                # 添加标题
                ax.set_title(f"{view}\n{view_descriptions[i]}", fontsize=14, fontweight='bold', color='#1e40af')
                
                # 添加关键脑区标注
                if img is not None:
                    h, w, _ = img_resized.shape
                else:
                    h, w = 300, 400
                
                # 根据不同视角添加不同的脑区标注
                if i == 0:  # 横断面（水平切面）
                    # 标注海马体（两侧）
                    ax.annotate('海马体\n(高风险)', xy=(w//4, h//2), xytext=(w//4 - 60, h//2 - 80),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    ax.annotate('海马体\n(高风险)', xy=(3*w//4, h//2), xytext=(3*w//4 + 20, h//2 - 80),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    # 标注前额叶（顶部）
                    ax.annotate('前额叶\n(风险区域)', xy=(w//2, h//4), xytext=(w//2 + 60, h//4 - 30),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    # 标注顶叶（中部）
                    ax.annotate('顶叶\n(风险区域)', xy=(w//2, h//2), xytext=(w//2 - 80, h//2 - 60),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                elif i == 1:  # 矢状面（侧面）
                    # 标注海马体（中部）
                    ax.annotate('海马体\n(高风险)', xy=(w//2, h//2), xytext=(w//2 - 80, h//2 - 60),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    # 标注颞叶（下部）
                    ax.annotate('颞叶\n(风险区域)', xy=(w//2, 3*h//4), xytext=(w//2 + 20, 3*h//4 + 40),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='orange', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    # 标注前额叶（上部）
                    ax.annotate('前额叶\n(风险区域)', xy=(w//2, h//4), xytext=(w//2 + 60, h//4 - 30),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                else:  # 冠状面（前后切面）
                    # 标注海马体（两侧）
                    ax.annotate('海马体\n(高风险)', xy=(w//4, h//2), xytext=(w//4 - 60, h//2 - 80),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    ax.annotate('海马体\n(高风险)', xy=(3*w//4, h//2), xytext=(3*w//4 + 20, h//2 - 80),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                    # 标注前额叶（顶部）
                    ax.annotate('前额叶\n(风险区域)', xy=(w//2, h//4), xytext=(w//2 + 60, h//4 - 30),
                               fontsize=11, color='white', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='darkred', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#FFD700', lw=3))
                
                # 关闭坐标轴
                ax.axis('off')
            
            # 添加总标题
            fig.suptitle('脑区风险热力图分析', fontsize=18, fontweight='bold', color='#1e40af')
            
            # 添加图例和说明
            legend_elements = [
                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#34d399', markersize=12, label='低风险 (< 30%)'),
                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#fbbf24', markersize=12, label='中风险 (30-60%)'),
                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#f87171', markersize=12, label='高风险 (> 60%)')
            ]
            
            fig.legend(handles=legend_elements, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=12)
            
            # 添加图像来源说明
            fig.text(0.5, 0.02, f'图像来源: {image_source} | 数据类型: 核磁共振成像 (MRI)', 
                    ha='center', fontsize=10, color='#666666')
            
            # 调整布局
            plt.tight_layout(rect=[0, 0.15, 1, 0.95])
            
            # 保存图像到内存
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            
            # 转换为base64编码
            heatmap_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # 关闭图像
            plt.close(fig)
            
            return heatmap_base64
            
        except Exception as e:
            logger.error("生成热力图失败", e)
            return None
    
    def _calculate_risk_scores(self, risk_indicators, diagnosis):
        """
        根据风险指标计算各脑区的风险分数
        :param risk_indicators: 风险指标
        :param diagnosis: 诊断结果
        :return: 风险分数字典
        """
        risk_scores = {
            'hippocampus': 0,  # 海马体
            'temporal': 0,     # 颞叶
            'frontal': 0,      # 前额叶
            'parietal': 0,     # 顶叶
            'occipital': 0     # 枕叶
        }
        
        # 基础风险分数
        base_risk = {
            'AD': 80,
            'LMCI': 50,
            'EMCI': 30,
            'CN': 10
        }
        
        # 设置基础风险
        base_score = base_risk.get(diagnosis, 10)
        
        # 根据风险指标调整风险分数
        if risk_indicators:
            for indicator, data in risk_indicators.items():
                if 'risk_level' in data:
                    risk_level = data['risk_level']
                    if risk_level == 'high':
                        if '海马体' in indicator:
                            risk_scores['hippocampus'] += 30
                        elif 'tau' in indicator.lower() or '淀粉样蛋白' in indicator:
                            risk_scores['temporal'] += 25
                            risk_scores['hippocampus'] += 20
                        elif '葡萄糖' in indicator or '代谢' in indicator:
                            risk_scores['frontal'] += 20
                            risk_scores['parietal'] += 15
                        elif '白质' in indicator:
                            risk_scores['parietal'] += 20
                            risk_scores['occipital'] += 15
                    elif risk_level == 'medium':
                        if '海马体' in indicator:
                            risk_scores['hippocampus'] += 15
                        elif 'tau' in indicator.lower() or '淀粉样蛋白' in indicator:
                            risk_scores['temporal'] += 12
                        elif '葡萄糖' in indicator or '代谢' in indicator:
                            risk_scores['frontal'] += 10
                        elif '白质' in indicator:
                            risk_scores['parietal'] += 10
        
        # 应用基础风险
        for region in risk_scores:
            risk_scores[region] = min(100, base_score + risk_scores[region])
        
        return risk_scores
    
    def _generate_heatmap_overlay(self, img, risk_scores, view_index):
        """
        生成热力图叠加效果
        :param img: 原始图像
        :param risk_scores: 风险分数
        :param view_index: 视角索引（0: 横断面, 1: 矢状面, 2: 冠状面）
        :return: 热力图
        """
        h, w, _ = img.shape
        
        # 创建热力图基础
        heatmap = np.zeros((h, w))
        
        # 根据视角设置不同的脑区位置
        if view_index == 0:  # 横断面
            # 海马体（两侧）
            center_y = h // 2
            center_x1 = w // 4
            center_x2 = 3 * w // 4
            
            # 颞叶（两侧）
            temporal_x1 = w // 5
            temporal_x2 = 4 * w // 5
            
            # 前额叶（顶部）
            frontal_y = h // 4
            
            # 顶叶（中部）
            parietal_y = h // 2
            
            # 枕叶（底部）
            occipital_y = 3 * h // 4
            
            # 绘制脑区热力图
            self._draw_heatmap_region(heatmap, center_x1, center_y, risk_scores['hippocampus'], 0.1)
            self._draw_heatmap_region(heatmap, center_x2, center_y, risk_scores['hippocampus'], 0.1)
            self._draw_heatmap_region(heatmap, temporal_x1, center_y, risk_scores['temporal'], 0.15)
            self._draw_heatmap_region(heatmap, temporal_x2, center_y, risk_scores['temporal'], 0.15)
            self._draw_heatmap_region(heatmap, w//2, frontal_y, risk_scores['frontal'], 0.2)
            self._draw_heatmap_region(heatmap, w//2, parietal_y, risk_scores['parietal'], 0.18)
            self._draw_heatmap_region(heatmap, w//2, occipital_y, risk_scores['occipital'], 0.15)
            
        elif view_index == 1:  # 矢状面
            # 海马体（中部）
            center_x = w // 2
            center_y = h // 2
            
            # 颞叶（下部）
            temporal_y = 2 * h // 3
            
            # 前额叶（上部）
            frontal_y = h // 4
            
            # 顶叶（中部偏上）
            parietal_y = h // 3
            
            # 枕叶（下部）
            occipital_y = 3 * h // 4
            
            self._draw_heatmap_region(heatmap, center_x, center_y, risk_scores['hippocampus'], 0.12)
            self._draw_heatmap_region(heatmap, center_x, temporal_y, risk_scores['temporal'], 0.15)
            self._draw_heatmap_region(heatmap, center_x, frontal_y, risk_scores['frontal'], 0.2)
            self._draw_heatmap_region(heatmap, center_x, parietal_y, risk_scores['parietal'], 0.18)
            self._draw_heatmap_region(heatmap, center_x, occipital_y, risk_scores['occipital'], 0.15)
            
        else:  # 冠状面
            # 海马体（两侧）
            center_y = h // 2
            center_x1 = w // 3
            center_x2 = 2 * w // 3
            
            # 颞叶（两侧）
            temporal_x1 = w // 4
            temporal_x2 = 3 * w // 4
            
            # 前额叶（上部）
            frontal_y = h // 4
            
            # 顶叶（中部）
            parietal_y = h // 2
            
            # 枕叶（下部）
            occipital_y = 3 * h // 4
            
            self._draw_heatmap_region(heatmap, center_x1, center_y, risk_scores['hippocampus'], 0.1)
            self._draw_heatmap_region(heatmap, center_x2, center_y, risk_scores['hippocampus'], 0.1)
            self._draw_heatmap_region(heatmap, temporal_x1, center_y, risk_scores['temporal'], 0.15)
            self._draw_heatmap_region(heatmap, temporal_x2, center_y, risk_scores['temporal'], 0.15)
            self._draw_heatmap_region(heatmap, w//2, frontal_y, risk_scores['frontal'], 0.2)
            self._draw_heatmap_region(heatmap, w//2, parietal_y, risk_scores['parietal'], 0.18)
            self._draw_heatmap_region(heatmap, w//2, occipital_y, risk_scores['occipital'], 0.15)
        
        # 应用高斯模糊使热力图更自然
        heatmap = gaussian_filter(heatmap, sigma=5)
        
        return heatmap
    
    def _draw_heatmap_region(self, heatmap, center_x, center_y, intensity, radius_factor):
        """
        在热力图上绘制脑区
        :param heatmap: 热力图数组
        :param center_x: 中心x坐标
        :param center_y: 中心y坐标
        :param intensity: 强度（0-100）
        :param radius_factor: 半径因子
        """
        h, w = heatmap.shape
        radius = int(min(h, w) * radius_factor)
        
        for y in range(max(0, center_y - radius), min(h, center_y + radius)):
            for x in range(max(0, center_x - radius), min(w, center_x + radius)):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= radius:
                    # 距离衰减
                    weight = 1 - (distance / radius)
                    heatmap[y, x] = max(heatmap[y, x], intensity * weight)
