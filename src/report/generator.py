"""
报告生成器 - 生成诊断报告和可视化结果
"""

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from src.utils.log_manager import log_manager as logger
from src.utils.config_manager import config_manager


class ReportGenerator:
    """报告生成器类 - 生成诊断报告和可视化"""
    
    def __init__(self):
        self.output_dir = config_manager.get('report.output_directory', 'results')
        self._ensure_output_dir()
        logger.info("报告生成器初始化完成")
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"创建输出目录: {self.output_dir}")
    
    def generate_json_report(self, diagnosis_report):
        """
        生成JSON格式报告
        :param diagnosis_report: 诊断报告数据
        :return: 报告文件路径
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"diagnosis_report_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(diagnosis_report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON报告生成完成: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error("JSON报告生成失败", e)
            raise
    
    def generate_visualization(self, prediction_result):
        """
        生成可视化图表
        :param prediction_result: 预测结果
        :return: 图表文件路径列表
        """
        try:
            chart_paths = []
            
            # 生成概率分布图
            probability_chart = self._generate_probability_chart(prediction_result)
            if probability_chart:
                chart_paths.append(probability_chart)
            
            # 生成风险评分图表
            risk_chart = self._generate_risk_chart(prediction_result)
            if risk_chart:
                chart_paths.append(risk_chart)
            
            logger.info(f"可视化图表生成完成，生成了 {len(chart_paths)} 个图表")
            return chart_paths
            
        except Exception as e:
            logger.error("可视化图表生成失败", e)
            return []
    
    def _generate_probability_chart(self, prediction_result):
        """生成概率分布柱状图"""
        try:
            classes = list(prediction_result['probabilities'].keys())
            probabilities = list(prediction_result['probabilities'].values())
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(classes, probabilities, color=['#3b82f6', '#ef4444', '#10b981', '#f59e0b'])
            
            plt.xlabel('诊断类别')
            plt.ylabel('概率')
            plt.title('诊断概率分布')
            plt.ylim(0, 1.1)
            
            # 在柱子上显示数值
            for bar, prob in zip(bars, probabilities):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{prob:.3f}', ha='center', va='bottom')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"probability_chart_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error("概率分布图生成失败", e)
            plt.close()
            return None
    
    def _generate_risk_chart(self, prediction_result):
        """生成风险评分图表"""
        try:
            # 计算风险评分
            risk_weights = config_manager.get('diagnosis.risk_weights', {})
            base_score = 0
            
            for class_name, probability in prediction_result['probabilities'].items():
                weight = risk_weights.get(class_name, 1.0)
                base_score += probability * weight
            
            risk_score = min(100, max(0, int(base_score * 100)))
            
            plt.figure(figsize=(8, 4))
            
            # 创建风险评分仪表盘
            plt.bar(['风险评分'], [risk_score], color='#3b82f6')
            plt.ylim(0, 100)
            plt.ylabel('风险评分')
            plt.title('阿尔茨海默病风险评估')
            
            # 添加风险等级标签
            if risk_score< 30:
                plt.text(0, risk_score + 2, '低风险', ha='center', va='bottom', color='#10b981', fontweight='bold')
            elif risk_score < 60:
                plt.text(0, risk_score + 2, '中等风险', ha='center', va='bottom', color='#f59e0b', fontweight='bold')
            else:
                plt.text(0, risk_score + 2, '高风险', ha='center', va='bottom', color='#ef4444', fontweight='bold')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"risk_chart_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error("风险评分图表生成失败", e)
            plt.close()
            return None
    
    def generate_summary_report(self, diagnosis_report, chart_paths=None):
        """
        生成综合报告
        :param diagnosis_report: 诊断报告数据
        :param chart_paths: 图表文件路径列表
        :return: 综合报告数据
        """
        try:
            summary = {
                'patient_info': diagnosis_report.get('patient_info', {}),
                'diagnosis': diagnosis_report.get('diagnosis'),
                'confidence': diagnosis_report.get('confidence'),
                'risk_score': diagnosis_report.get('risk_score'),
                'timestamp': diagnosis_report.get('timestamp', datetime.now().isoformat()),
                'charts': chart_paths or [],
                'recommendations': diagnosis_report.get('recommendations', [])
            }
            
            logger.info("综合报告生成完成")
            return summary
            
        except Exception as e:
            logger.error("综合报告生成失败", e)
            raise
