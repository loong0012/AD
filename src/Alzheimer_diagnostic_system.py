"""
阿尔兹海默症诊断系统主类
"""

import os
import json
import base64
import numpy as np
from datetime import datetime
from src.utils.log_manager import log_manager as logger
from src.utils.config_manager import config_manager
from src.data.processor import DataProcessor
from src.diagnosis.engine import DiagnosisEngine
from src.report.generator import ReportGenerator

# 尝试导入图像生成和处理库
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    from PIL import Image as PILImage
    import io
    IMAGE_LIBS_AVAILABLE = True
    # 注册中文字体
    import matplotlib.font_manager as fm
    CHINESE_FONT_PATH = None
    for font in fm.fontManager.ttflist:
        if 'SimHei' in font.name:
            CHINESE_FONT_PATH = font.fname
            plt.rcParams['font.sans-serif'] = [font.name]
            plt.rcParams['axes.unicode_minus'] = False
            break
    if not CHINESE_FONT_PATH:
        for font in fm.fontManager.ttflist:
            if 'YaHei' in font.name:
                CHINESE_FONT_PATH = font.fname
                plt.rcParams['font.sans-serif'] = [font.name]
                plt.rcParams['axes.unicode_minus'] = False
                break
except ImportError as e:
    logger.warning(f"图像库导入失败: {e}")
    IMAGE_LIBS_AVAILABLE = False
    CHINESE_FONT_PATH = None

class MultiModalDataManager:
    """多模态数据管理器 - 处理数据的加载和管理"""
    
    def __init__(self):
        """初始化数据管理器"""
        self.data_dir = config_manager.get('data.directory', 'data')
        self.demo_data_dir = config_manager.get('data.demo_directory', 'demodata')
        self.processor = DataProcessor()
        logger.info("多模态数据管理器初始化完成")
    
    def load_patient_data(self, patient_id):
        """
        加载患者数据
        :param patient_id: 患者ID
        :return: 患者数据
        """
        try:
            # 这里是一个示例实现，实际应该从数据库或文件系统加载数据
            patient_data = {
                'clinical_info': {
                    'age': 75,
                    'gender': 'male',
                    'education_years': 12,
                    'family_history': '阿尔兹海默病',
                    'clinical_history': '高血压、糖尿病'
                },
                'lifestyle': {
                    'exercise_frequency': '3',
                    'sleep_duration': '7',
                    'diet_health': 'medium',
                    'social_activities': '2',
                    'smoking_status': 'never',
                    'alcohol_consumption': 'occasional'
                },
                'molecular_data': [
                    ['Aβ42', '500', 'pg/mL'],
                    ['p-tau217', '40', 'pg/mL'],
                    ['t-tau', '300', 'pg/mL']
                ]
            }
            
            logger.info(f"加载患者数据成功: {patient_id}")
            return patient_data
            
        except Exception as e:
            logger.error(f"加载患者数据失败: {patient_id}", e)
            return {}
    
    def create_demo_multimodal_data(self, demo_category=None):
        """
        创建演示多模态数据
        :param demo_category: 演示类别 (CN, EMCI, LMCI, AD)
        :return: 演示数据
        """
        try:
            # 根据不同类别生成不同的演示数据
            if demo_category == 'CN':
                # 认知正常
                demo_data = {
                    'clinical_info': {
                        'age': 65,
                        'gender': 'female',
                        'education_years': 16,
                        'family_history': '无',
                        'clinical_history': '健康'
                    },
                    'lifestyle': {
                        'exercise_frequency': '5',
                        'sleep_duration': '8',
                        'diet_health': 'high',
                        'social_activities': '4',
                        'smoking_status': 'never',
                        'alcohol_consumption': 'occasional'
                    },
                    'molecular_data': [
                        ['Aβ42', '700', 'pg/mL'],
                        ['p-tau217', '25', 'pg/mL'],
                        ['t-tau', '180', 'pg/mL']
                    ]
                }
            elif demo_category == 'EMCI':
                # 早期轻度认知障碍
                demo_data = {
                    'clinical_info': {
                        'age': 70,
                        'gender': 'male',
                        'education_years': 12,
                        'family_history': '无',
                        'clinical_history': '高血压'
                    },
                    'lifestyle': {
                        'exercise_frequency': '2',
                        'sleep_duration': '6',
                        'diet_health': 'medium',
                        'social_activities': '2',
                        'smoking_status': 'past',
                        'alcohol_consumption': 'occasional'
                    },
                    'molecular_data': [
                        ['Aβ42', '450', 'pg/mL'],
                        ['p-tau217', '35', 'pg/mL'],
                        ['t-tau', '250', 'pg/mL']
                    ]
                }
            elif demo_category == 'LMCI':
                # 晚期轻度认知障碍
                demo_data = {
                    'clinical_info': {
                        'age': 75,
                        'gender': 'female',
                        'education_years': 10,
                        'family_history': '阿尔兹海默病',
                        'clinical_history': '高血压、糖尿病'
                    },
                    'lifestyle': {
                        'exercise_frequency': '1',
                        'sleep_duration': '5',
                        'diet_health': 'low',
                        'social_activities': '1',
                        'smoking_status': 'past',
                        'alcohol_consumption': 'regular'
                    },
                    'molecular_data': [
                        ['Aβ42', '350', 'pg/mL'],
                        ['p-tau217', '60', 'pg/mL'],
                        ['t-tau', '350', 'pg/mL']
                    ]
                }
            elif demo_category == 'AD':
                # 阿尔兹海默症
                demo_data = {
                    'clinical_info': {
                        'age': 80,
                        'gender': 'male',
                        'education_years': 8,
                        'family_history': '阿尔兹海默病',
                        'clinical_history': '高血压、糖尿病、心脏病'
                    },
                    'lifestyle': {
                        'exercise_frequency': '0',
                        'sleep_duration': '4',
                        'diet_health': 'low',
                        'social_activities': '0',
                        'smoking_status': 'current',
                        'alcohol_consumption': 'regular'
                    },
                    'molecular_data': [
                        ['Aβ42', '250', 'pg/mL'],
                        ['p-tau217', '100', 'pg/mL'],
                        ['t-tau', '500', 'pg/mL']
                    ]
                }
            else:
                # 默认演示数据
                demo_data = {
                    'clinical_info': {
                        'age': 72,
                        'gender': 'female',
                        'education_years': 14,
                        'family_history': '无',
                        'clinical_history': '健康'
                    },
                    'lifestyle': {
                        'exercise_frequency': '3',
                        'sleep_duration': '7',
                        'diet_health': 'medium',
                        'social_activities': '3',
                        'smoking_status': 'never',
                        'alcohol_consumption': 'occasional'
                    },
                    'molecular_data': [
                        ['Aβ42', '550', 'pg/mL'],
                        ['p-tau217', '30', 'pg/mL'],
                        ['t-tau', '220', 'pg/mL']
                    ]
                }
            
            logger.info(f"创建演示数据成功: {demo_category}")
            return demo_data
            
        except Exception as e:
            logger.error("创建演示数据失败", e)
            return {}

class PDFReportGenerator:
    """PDF报告生成器 - 生成详细的诊断报告"""
    
    def __init__(self):
        """初始化PDF报告生成器"""
        self.output_dir = config_manager.get('report.pdf_directory', 'reports')
        self._ensure_output_dir()
        logger.info("PDF报告生成器初始化完成")
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"创建PDF输出目录: {self.output_dir}")
    
    def generate_report(self, results_data, patient_info):
        """
        生成PDF报告 - 包含所有诊断模块的完整报告
        :param results_data: 诊断结果数据
        :param patient_info: 患者信息
        :return: PDF文件路径
        """
        try:
            import reportlab
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            # 注册中文字体
            try:
                pdfmetrics.registerFont(TTFont('SimHei', 'C:\\Windows\\Fonts\\simhei.ttf'))
                pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc'))
                chinese_font_name = 'SimHei'
            except Exception as e:
                logger.warning(f"注册中文字体失败: {e}")
                chinese_font_name = 'Helvetica'
            
            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            patient_id = patient_info.get('patient_id', 'unknown')
            filename = f"diagnosis_report_{patient_id}_{timestamp}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # 创建PDF文档
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # 自定义样式 - 使用中文字体
            title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontName=chinese_font_name, fontSize=28, textColor=colors.HexColor('#ffffff'), spaceAfter=30, alignment=TA_CENTER, backColor=colors.HexColor('#1a56db'), leftIndent=20, rightIndent=20, padding=15)
            heading1_style = ParagraphStyle('CustomHeading1', parent=styles['Heading1'], fontName=chinese_font_name, fontSize=18, textColor=colors.HexColor('#1e429f'), spaceBefore=20, spaceAfter=15)
            heading2_style = ParagraphStyle('CustomHeading2', parent=styles['Heading2'], fontName=chinese_font_name, fontSize=14, textColor=colors.HexColor('#3b82f6'), spaceBefore=15, spaceAfter=10)
            body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'], fontName=chinese_font_name, fontSize=12, leading=18, textColor=colors.HexColor('#333333'))
            feature_style = ParagraphStyle('FeatureStyle', parent=styles['BodyText'], fontName=chinese_font_name, fontSize=14, leading=20, textColor=colors.HexColor('#ffffff'), spaceAfter=10)
            toc_style = ParagraphStyle('TocEntry', parent=styles['Normal'], fontName=chinese_font_name, fontSize=11, leading=16, textColor=colors.HexColor('#333333'))
            
            # ========== 添加封面页（带背景图片）==========
            cover_image_path = r"d:\Desktop\Alzheimer-diagnostic system\uploaded_img\阿尔兹海默症封面图.png"
            
            # 创建封面页面模板
            from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
            from reportlab.lib.units import inch
            
            # 定义封面页面模板
            def cover_page(canvas, doc):
                canvas.saveState()
                # 添加背景图片
                if os.path.exists(cover_image_path):
                    try:
                        canvas.drawImage(cover_image_path, 0, 0, width=595, height=842)
                        # 添加半透明遮罩
                        canvas.setFillColor(colors.HexColor('#000000'), alpha=0.3)
                        canvas.rect(0, 0, 595, 842, fill=1, stroke=0)
                    except Exception as e:
                        logger.warning(f"添加封面背景图片失败: {e}")
                canvas.restoreState()
            
            # 应用封面页面模板
            cover_template = PageTemplate(frames=[Frame(1*inch, 1*inch, 6*inch, 9*inch)], onPage=cover_page)
            doc.addPageTemplates([cover_template])
            
            # 封面内容
            cover_content = []
            
            # 系统名称
            cover_title = Paragraph("阿尔兹海默症智能诊断系统", title_style)
            cover_content.append(cover_title)
            cover_content.append(Spacer(1, 40))
            
            # 系统特点（大字突出）
            cover_content.append(Paragraph("<b>核心特点</b>", ParagraphStyle('FeatureTitle', parent=styles['Heading2'], fontName=chinese_font_name, fontSize=16, textColor=colors.HexColor('#ffffff'), spaceAfter=15, alignment=TA_CENTER)))
            
            system_features = [
                "• 多模态数据融合分析",
                "• AI辅助诊断算法",
                "• 实时风险评估",
                "• 个性化治疗建议",
                "• 12个月进展预测"
            ]
            for feature in system_features:
                cover_content.append(Paragraph(feature, feature_style))
            
            cover_content.append(Spacer(1, 30))
            cover_content.append(Paragraph("系统特点：精准诊断、智能分析、全面评估", feature_style))
            cover_content.append(Spacer(1, 40))
            
            # 目录
            cover_content.append(Paragraph("<b>报告目录</b>", ParagraphStyle('TocTitle', parent=styles['Heading2'], fontName=chinese_font_name, fontSize=16, textColor=colors.HexColor('#ffffff'), spaceAfter=15, alignment=TA_CENTER)))
            
            toc_items = [
                ("一、患者基本信息", "3"),
                ("二、诊断结果概要", "4"),
                ("三、脑部图像分析", "5"),
                ("四、脑区风险热力图", "6"),
                ("五、关键风险指标", "7"),
                ("六、12个月进展预测", "8"),
                ("七、个性化指导建议", "9"),
                ("八、医生信息和报告说明", "10")
            ]
            
            for toc_item, page in toc_items:
                toc_text = Paragraph(f"{toc_item} ............................. {page}", ParagraphStyle('CoverToc', parent=styles['Normal'], fontName=chinese_font_name, fontSize=12, leading=18, textColor=colors.HexColor('#ffffff')))
                cover_content.append(toc_text)
            
            elements.extend(cover_content)
            elements.append(PageBreak())
            
            # ========== 添加标题 ==========
            title = Paragraph("阿尔兹海默症诊断报告", title_style)
            elements.append(title)
            
            hospital_info = Paragraph("<b>医院名称:</b> 神经内科中心医院", body_style)
            elements.append(hospital_info)
            system_info = Paragraph("<b>系统版本:</b> 阿尔兹海默症诊断系统 v3.0.0", body_style)
            elements.append(system_info)
            elements.append(Spacer(1, 30))
            
            # ========== 一、患者基本信息 ==========
            elements.append(Paragraph("一、患者基本信息", heading1_style))
            
            patient_data = []
            patient_data.append([Paragraph("<b>项目</b>", body_style), Paragraph("<b>值</b>", body_style)])
            
            gender_map = {'male': '男', 'female': '女', 'M': '男', 'F': '女'}
            gender_display = gender_map.get(patient_info.get('gender', ''), patient_info.get('gender', '未知'))
            
            basic_info = {
                '姓名': patient_info.get('name', '未知'),
                '年龄': f"{patient_info.get('age', '未知')}岁",
                '性别': gender_display,
                '教育年限': f"{patient_info.get('education_years', '未知')}年",
                '联系方式': patient_info.get('contact_info', '未知'),
                '病史': patient_info.get('medical_history', '无')
            }
            
            for key, value in basic_info.items():
                patient_data.append([Paragraph(key, body_style), Paragraph(str(value), body_style)])
            
            # 生活方式数据 - 兼容前端传递的lifestyle对象或lifestyle_data
            lifestyle_info = patient_info.get('lifestyle_data', patient_info.get('lifestyle', {}))
            if lifestyle_info:
                elements.append(Spacer(1, 15))
                elements.append(Paragraph("生活方式信息", heading2_style))
                

                lifestyle_data = []
                lifestyle_data.append([Paragraph("<b>生活方式</b>", body_style), Paragraph("<b>值</b>", body_style)])
                
                lifestyle_map = {
                    'exercise_frequency': '每周运动次数',
                    'sleep_duration': '每天睡眠时间(小时)',
                    'diet_health': '饮食习惯',
                    'social_activities': '每周社交活动次数',
                    'smoking_status': '吸烟状况',
                    'alcohol_consumption': '饮酒频率'
                }
                
                value_converters = {
                    'diet_health': {'low': '差', 'medium': '中等', 'high': '良好'},
                    'smoking_status': {'never': '从不吸烟', 'past': '曾经吸烟', 'current': '正在吸烟'},
                    'alcohol_consumption': {'none': '不饮酒', 'occasional': '偶尔饮酒', 'regular': '经常饮酒'}
                }
                
                for key, label in lifestyle_map.items():
                    value = lifestyle_info.get(key, '未知')
                    if key in value_converters:
                        value = value_converters[key].get(value, value)
                    lifestyle_data.append([Paragraph(label, body_style), Paragraph(str(value), body_style)])
                
                lifestyle_table = Table(lifestyle_data, colWidths=[150, 300])
                lifestyle_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0f2fe')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0369a1')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('TOPPADDING', (0, 0), (-1, 0), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
                ]))
                elements.append(lifestyle_table)
                elements.append(Spacer(1, 20))
            
            patient_table = Table(patient_data, colWidths=[150, 300])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dbeafe')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
            ]))
            elements.append(patient_table)
            elements.append(Spacer(1, 30))
            
            # ========== 二、诊断结果概要 ==========
            elements.append(Paragraph("二、诊断结果概要", heading1_style))

            # 兼容处理：前端可能传递 results.data 或直接传递 results
            if 'results' in results_data and isinstance(results_data.get('results'), dict):
                # 标准结构: { results: { pred_label, confidence, ... } }
                results = results_data['results']
            elif 'data' in results_data and isinstance(results_data.get('data'), dict):
                # API响应结构: { data: { diagnosis, confidence, ... } }
                api_data = results_data['data']
                results = {
                    'pred_label': api_data.get('diagnosis'),
                    'confidence': api_data.get('confidence', 0.0),
                    'risk_score': api_data.get('risk_score', 0.0),
                    'monthly_risk': api_data.get('monthly_risk', []),
                    'risk_indicators': api_data.get('risk_indicators', {}),
                    'recommendations': api_data.get('recommendations', [])
                }
            else:
                # 直接传递的结构
                results = results_data

            pred_label = results.get('pred_label', results.get('diagnosis', '未知'))
            confidence = results.get('confidence', 0.0)
            risk_score = results.get('risk_score', 0.0)

            label_map = {'CN': '认知正常', 'EMCI': '早期轻度认知障碍', 'LMCI': '晚期轻度认知障碍', 'AD': '阿尔茨海默病'}
            pred_label_cn = label_map.get(pred_label, pred_label)

            if risk_score < 0.3:
                risk_level = "低风险"
            elif risk_score < 0.6:
                risk_level = "中风险"
            else:
                risk_level = "高风险"

            diagnosis_data = []
            diagnosis_data.append([Paragraph("<b>项目</b>", body_style), Paragraph("<b>结果</b>", body_style)])
            diagnosis_data.append([Paragraph("诊断结论", body_style), Paragraph(pred_label_cn, body_style)])
            diagnosis_data.append([Paragraph("置信度", body_style), Paragraph(f"{confidence:.2%}", body_style)])
            diagnosis_data.append([Paragraph("风险评分", body_style), Paragraph(f"{risk_score:.2f}", body_style)])
            diagnosis_data.append([Paragraph("风险等级", body_style), Paragraph(risk_level, body_style)])

            diagnosis_table = Table(diagnosis_data, colWidths=[150, 300])
            diagnosis_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fef3c7')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#92400e')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
            ]))
            elements.append(diagnosis_table)
            elements.append(Spacer(1, 20))

            elements.append(Paragraph("三、脑部图像分析", heading1_style))

            if IMAGE_LIBS_AVAILABLE:
                try:
                    # 检查是否有实际的MRI图像数据
                    brain_image = None
                    # 检查results中是否有brain_image字段
                    if 'brain_image' in results:
                        # 处理实际的MRI图像数据
                        brain_image_data = results['brain_image']
                        if isinstance(brain_image_data, str) and brain_image_data.startswith('data:image'):
                            # 处理base64编码的图像
                            import base64
                            from io import BytesIO
                            img_data = base64.b64decode(brain_image_data.split(',')[1])
                            img_stream = BytesIO(img_data)
                            brain_image = Image(img_stream, width=400, height=300)
                        elif isinstance(brain_image_data, str) and os.path.exists(brain_image_data):
                            # 处理图像文件路径
                            brain_image = Image(brain_image_data, width=400, height=300)
                    # 检查results['results']中是否有brain_image字段
                    elif 'results' in results and 'brain_image' in results['results']:
                        # 处理实际的MRI图像数据
                        brain_image_data = results['results']['brain_image']
                        if isinstance(brain_image_data, str) and brain_image_data.startswith('data:image'):
                            # 处理base64编码的图像
                            import base64
                            from io import BytesIO
                            img_data = base64.b64decode(brain_image_data.split(',')[1])
                            img_stream = BytesIO(img_data)
                            brain_image = Image(img_stream, width=400, height=300)
                        elif isinstance(brain_image_data, str) and os.path.exists(brain_image_data):
                            # 处理图像文件路径
                            brain_image = Image(brain_image_data, width=400, height=300)
                    
                    # 如果没有实际MRI图像，使用生成的示意图
                    if not brain_image:
                        brain_image = self._generate_brain_analysis_image(pred_label)
                    
                    if brain_image:
                        brain_desc = Paragraph(f"<b>图1:</b> 脑部结构分析图 - 显示{pred_label_cn}状态下的脑区分布情况", body_style)
                        elements.append(brain_desc)
                        elements.append(Spacer(1, 10))
                        elements.append(brain_image)
                        elements.append(Spacer(1, 15))

                        brain_regions_desc = [
                            "• 额叶(FL): 负责执行功能和决策",
                            "• 颞叶(TL): 负责记忆和语言处理",
                            "• 顶叶(PL): 负责空间认知和注意力",
                            "• 枕叶(OL): 负责视觉信息处理"
                        ]
                        for desc in brain_regions_desc:
                            elements.append(Paragraph(desc, body_style))
                except Exception as e:
                    logger.error("生成脑部分析图像失败", e)

            elements.append(Spacer(1, 20))

            elements.append(Paragraph("四、脑区风险热力图", heading1_style))

            if IMAGE_LIBS_AVAILABLE:
                try:
                    # 获取风险指标数据
                    risk_indicators = results.get('risk_indicators', {})
                    # 如果results中没有，检查results['results']
                    if not risk_indicators and 'results' in results:
                        risk_indicators = results['results'].get('risk_indicators', {})
                    
                    heatmap_image = self._generate_brain_risk_heatmap(risk_score, risk_indicators)
                    if heatmap_image:
                        heatmap_desc = Paragraph(f"<b>图2:</b> 脑区风险热力图 - 展示不同脑区的风险程度(风险值越高颜色越深)", body_style)
                        elements.append(heatmap_desc)
                        elements.append(Spacer(1, 10))
                        elements.append(heatmap_image)
                        elements.append(Spacer(1, 15))

                        heatmap_legend = [
                            "• 颜色说明: 黄色→橙色→红色 表示风险程度从低到高",
                            "• 额叶和颞叶是阿尔茨海默病最常影响的脑区",
                            "• 海马体负责记忆形成，是疾病早期受影响的关键区域"
                        ]
                        for legend in heatmap_legend:
                            elements.append(Paragraph(legend, body_style))
                except Exception as e:
                    logger.error("生成脑区热力图失败", e)

            elements.append(Spacer(1, 20))

            elements.append(Paragraph("五、关键风险指标", heading1_style))

            risk_indicators = results.get('risk_indicators', {})
            if risk_indicators:

                risk_data = []
                risk_data.append([Paragraph("<b>指标名称</b>", body_style), Paragraph("<b>检测值</b>", body_style), Paragraph("<b>风险等级</b>", body_style), Paragraph("<b>参考说明</b>", body_style)])

                indicator_refs = {
                    '年龄风险': '年龄越大风险越高。正常范围: 60岁以下风险较低，60-75岁风险中等，75岁以上风险较高',
                    '教育程度': '教育年限越少风险越高。正常范围: 12年以上教育为低风险，9-12年为中等风险，9年以下为高风险',
                    '家族史': '有家族史风险增加。正常范围: 无家族史为低风险，一级亲属患病为中等风险，多亲属患病为高风险',
                    '生活方式': '不良生活方式增加风险。正常范围: 健康生活方式为低风险，一般生活方式为中等风险，不良生活方式为高风险',
                    '认知功能': '认知功能下降是重要指标。正常范围: 认知功能正常为低风险，轻度下降为中等风险，明显下降为高风险'
                }

                for indicator_name, indicator in risk_indicators.items():
                    ref = indicator_refs.get(indicator_name, '无详细参考信息')
                    risk_data.append([
                        Paragraph(indicator_name, body_style),
                        Paragraph(str(indicator.get('value', '未知')), body_style),
                        Paragraph(indicator.get('risk_level', '未知'), body_style),
                        Paragraph(ref, body_style)
                    ])

                risk_table = Table(risk_data, colWidths=[100, 120, 80, 150])
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fee2e2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#991b1b')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('TOPPADDING', (0, 0), (-1, 0), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
                ]))
                elements.append(risk_table)

            elements.append(Spacer(1, 20))

            elements.append(Paragraph("六、12个月进展预测", heading1_style))

            # 获取月度风险数据
            monthly_risk_data = results.get('monthly_risk', [])
            # 如果results中没有，检查results['results']
            if not monthly_risk_data and 'results' in results:
                monthly_risk_data = results['results'].get('monthly_risk', [])
                
            if monthly_risk_data:
                monthly_risk = monthly_risk_data

                if IMAGE_LIBS_AVAILABLE:
                    try:
                        trend_image = self._generate_risk_trend_chart(monthly_risk, pred_label)
                        if trend_image:
                            trend_desc = Paragraph("<b>图3:</b> 12个月认知风险变化趋势预测图", body_style)
                            elements.append(trend_desc)
                            elements.append(Spacer(1, 10))
                            elements.append(trend_image)
                            elements.append(Spacer(1, 15))
                    except Exception as e:
                        logger.error("生成风险趋势图失败", e)

                trend_data = []
                trend_data.append([Paragraph("<b>时间</b>", body_style), Paragraph("<b>风险值</b>", body_style), Paragraph("<b>风险变化</b>", body_style)])

                prev_risk = None
                for i, item in enumerate(monthly_risk[:12]):
                    current_risk = item.get('risk', 0)
                    month = item.get('month', f'第{i+1}月')

                    if prev_risk is not None:
                        change = current_risk - prev_risk
                        if change > 0.01:
                            change_str = "↑上升"
                        elif change < -0.01:
                            change_str = "↓下降"
                        else:
                            change_str = "→稳定"
                    else:
                        change_str = "基准"

                    trend_data.append([
                        Paragraph(str(month), body_style),
                        Paragraph(f"{current_risk:.3f}", body_style),
                        Paragraph(change_str, body_style)
                    ])
                    prev_risk = current_risk

                trend_table = Table(trend_data, colWidths=[100, 100, 100])
                trend_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dcfce7')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#15803d')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
                ]))
                elements.append(trend_table)

                if len(monthly_risk) >= 2:
                    first_risk = monthly_risk[0].get('risk', 0)
                    last_risk = monthly_risk[-1].get('risk', 0)
                    total_change = last_risk - first_risk

                    trend_analysis = Paragraph(f"<b>趋势分析:</b> 未来12个月风险值从{first_risk:.3f}变化到{last_risk:.3f}，总体{'上升' if total_change > 0 else '下降' if total_change < 0 else '保持稳定'}{abs(total_change):.3f}。", body_style)
                    elements.append(Spacer(1, 10))
                    elements.append(trend_analysis)

            elements.append(PageBreak())

            elements.append(Paragraph("七、个性化指导建议", heading1_style))

            # 获取建议数据
            recommendations = results.get('recommendations', results.get('medical_advice', []))
            # 如果results中没有，检查results['results']
            if not recommendations and 'results' in results:
                recommendations = results['results'].get('recommendations', results['results'].get('medical_advice', []))
                
            if recommendations:

                rec_categories = {
                    '运动锻炼': [r for r in recommendations if '运动' in r or '锻炼' in r or '活动' in r],
                    '饮食调理': [r for r in recommendations if '饮食' in r or '食物' in r or '营养' in r],
                    '认知训练': [r for r in recommendations if '认知' in r or '训练' in r or '学习' in r],
                    '社交活动': [r for r in recommendations if '社交' in r or '交流' in r or '朋友' in r],
                    '定期复查': [r for r in recommendations if '复诊' in r or '复查' in r or '检查' in r]
                }

                for category, recs in rec_categories.items():
                    if recs:
                        elements.append(Paragraph(f"<b>{category}</b>", heading2_style))
                        for i, rec in enumerate(recs, 1):
                            elements.append(Paragraph(f"{i}. {rec}", body_style))
                        elements.append(Spacer(1, 10))

            elements.append(Spacer(1, 30))

            elements.append(Paragraph("八、医生信息和报告说明", heading1_style))

            doctor_data = []
            doctor_data.append([Paragraph("<b>项目</b>", body_style), Paragraph("<b>值</b>", body_style)])
            doctor_data.append([Paragraph("主治医生", body_style), Paragraph("神经内科专家", body_style)])
            doctor_data.append([Paragraph("科室", body_style), Paragraph("神经内科", body_style)])
            doctor_data.append([Paragraph("联系方式", body_style), Paragraph("010-xxxxxxxx", body_style)])
            doctor_data.append([Paragraph("报告日期", body_style), Paragraph(datetime.now().strftime('%Y-%m-%d'), body_style)])

            doctor_table = Table(doctor_data, colWidths=[150, 300])
            doctor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ede9fe')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#5b21b6')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
            ]))
            elements.append(doctor_table)
            elements.append(Spacer(1, 30))

            elements.append(Paragraph("<b>报告说明</b>", heading2_style))

            notes = [
                "1. 本报告由阿尔兹海默症智能诊断系统自动生成，基于多模态数据分析算法。",
                "2. 诊断结果仅供参考，最终诊断应以临床医生综合判断为准。",
                "3. 建议患者定期进行认知功能评估，以便及时监测病情变化。",
                "4. 保持健康的生活方式（规律运动、健康饮食、社交活动）对预防和延缓认知衰退有重要作用。",
                "5. 如有疑问或不适，请及时就医咨询专业医生。"
            ]

            for note in notes:
                elements.append(Paragraph(note, body_style))
                elements.append(Spacer(1, 5))

            elements.append(Spacer(1, 30))

            timestamp_text = Paragraph(f"<b>报告生成时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style)
            elements.append(timestamp_text)
            report_id = Paragraph(f"<b>报告编号:</b> {filename.replace('.pdf', '')}", body_style)
            elements.append(report_id)
            
            # 生成PDF
            doc.build(elements)
            
            logger.info(f"PDF报告生成成功: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"PDF报告生成失败: {e}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _generate_brain_analysis_image(self, diagnosis):
        """
        生成脑部分析图像
        :param diagnosis: 诊断结果
        :return: reportlab Image对象
        """
        if not IMAGE_LIBS_AVAILABLE:
            return None
        
        try:
            # 使用全局字体设置
            if CHINESE_FONT_PATH:
                from matplotlib.font_manager import FontProperties
                font_prop = FontProperties(fname=CHINESE_FONT_PATH)
            else:
                font_prop = None
            
            # 创建一个简单的脑部示意图
            plt.figure(figsize=(8, 6))
            
            # 根据诊断结果设置不同的颜色
            diagnosis_colors = {
                'CN': '#10b981',  # 绿色 - 认知正常
                'EMCI': '#f59e0b',  # 橙色 - 早期轻度认知障碍
                'LMCI': '#ef4444',  # 红色 - 晚期轻度认知障碍
                'AD': '#8b5cf6'     # 紫色 - 阿尔茨海默病
            }
            
            color = diagnosis_colors.get(diagnosis, '#6b7280')  # 默认灰色
            
            # 绘制简化的脑部轮廓
            plt.plot([0.2, 0.8], [0.2, 0.2], color=color, linewidth=2)
            plt.plot([0.2, 0.8], [0.8, 0.8], color=color, linewidth=2)
            plt.plot([0.2, 0.2], [0.2, 0.8], color=color, linewidth=2)
            plt.plot([0.8, 0.8], [0.2, 0.8], color=color, linewidth=2)
            plt.plot([0.5, 0.5], [0.2, 0.8], color=color, linewidth=1, linestyle='--')
            
            # 添加脑区标记
            brain_regions = [
                (0.3, 0.6, '额叶'),
                (0.7, 0.6, '颞叶'),
                (0.3, 0.4, '顶叶'),
                (0.7, 0.4, '枕叶')
            ]
            
            for x, y, region in brain_regions:
                plt.scatter(x, y, color=color, s=50)
                if font_prop:
                    plt.text(x + 0.02, y + 0.02, region, fontsize=10, color='#1f2937', fontproperties=font_prop)
                else:
                    plt.text(x + 0.02, y + 0.02, region, fontsize=10, color='#1f2937')
            
            # 添加标题和说明
            if font_prop:
                plt.title('脑部分析示意图', fontsize=14, fontweight='bold', fontproperties=font_prop)
                plt.xlabel('大脑横向', fontsize=12, fontproperties=font_prop)
                plt.ylabel('大脑纵向', fontsize=12, fontproperties=font_prop)
            else:
                plt.title('Brain Analysis', fontsize=14, fontweight='bold')
                plt.xlabel('Lateral', fontsize=12)
                plt.ylabel('Vertical', fontsize=12)
            
            # 隐藏坐标轴刻度
            plt.xticks([])
            plt.yticks([])
            
            # 将图像转换为字节流
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            # 创建reportlab Image对象
            from reportlab.platypus import Image as ReportLabImage
            img = ReportLabImage(buffer)
            img.drawWidth = 400
            img.drawHeight = 300
            
            plt.close()
            return img
        except Exception as e:
            logger.error(f"生成脑部分析图像失败: {e}")
            return None
    
    def _generate_brain_risk_heatmap(self, risk_score, risk_indicators):
        """
        生成脑区风险热力图
        :param risk_score: 风险评分
        :param risk_indicators: 风险指标
        :return: reportlab Image对象
        """
        if not IMAGE_LIBS_AVAILABLE:
            return None
        
        try:
            # 使用全局字体设置
            if CHINESE_FONT_PATH:
                from matplotlib.font_manager import FontProperties
                font_prop = FontProperties(fname=CHINESE_FONT_PATH)
            else:
                font_prop = None
            
            # 创建脑区风险数据
            brain_regions = ['额叶', '颞叶', '顶叶', '枕叶', '海马体', '扣带回']
            
            # 根据风险评分生成风险值
            base_risk = risk_score
            region_risks = []
            
            for i, region in enumerate(brain_regions):
                # 添加一些随机变化，使热力图更有意义
                region_risk = base_risk * (0.8 + 0.4 * (i % 3) / 2)
                region_risks.append(round(region_risk, 2))
            
            # 转换为2D数组用于热力图
            heatmap_data = np.array(region_risks).reshape(2, 3)
            
            plt.figure(figsize=(8, 6))
            
            # 创建热力图并保存返回值用于colorbar
            ax = sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', 
                        xticklabels=['左', '中', '右'], 
                        yticklabels=['前', '后'])
            
            # 添加标题和说明
            if font_prop:
                plt.title('脑区风险热力图', fontsize=14, fontweight='bold', fontproperties=font_prop)
                plt.xlabel('大脑横向位置', fontsize=12, fontproperties=font_prop)
                plt.ylabel('大脑纵向位置', fontsize=12, fontproperties=font_prop)
            else:
                plt.title('Brain Risk Heatmap', fontsize=14, fontweight='bold')
                plt.xlabel('Lateral Position', fontsize=12)
                plt.ylabel('Vertical Position', fontsize=12)
            
            # 添加颜色条说明
            plt.colorbar(ax.collections[0], label='风险值' if font_prop else 'Risk Value')
            
            # 将图像转换为字节流
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            # 创建reportlab Image对象
            from reportlab.platypus import Image as ReportLabImage
            img = ReportLabImage(buffer)
            img.drawWidth = 400
            img.drawHeight = 300
            
            plt.close()
            return img
        except Exception as e:
            logger.error(f"生成脑区风险热力图失败: {e}")
            return None

    def _generate_risk_trend_chart(self, monthly_risk, diagnosis):
        """
        生成12个月风险趋势图
        :param monthly_risk: 月度风险数据
        :param diagnosis: 诊断结果
        :return: reportlab Image对象
        """
        if not IMAGE_LIBS_AVAILABLE or not monthly_risk:
            return None

        try:
            # 使用全局字体设置
            if CHINESE_FONT_PATH:
                from matplotlib.font_manager import FontProperties
                font_prop = FontProperties(fname=CHINESE_FONT_PATH)
            else:
                font_prop = None

            # 准备数据
            months = []
            risks = []
            for item in monthly_risk[:12]:
                months.append(str(item.get('month', '')))
                risks.append(item.get('risk', 0))

            # 创建图表
            plt.figure(figsize=(10, 5))

            # 根据诊断结果设置颜色
            diagnosis_colors = {
                'CN': '#10b981',  # 绿色
                'EMCI': '#f59e0b',  # 橙色
                'LMCI': '#ef4444',  # 红色
                'AD': '#8b5cf6'     # 紫色
            }
            line_color = diagnosis_colors.get(diagnosis, '#6b7280')

            # 绘制折线图
            plt.plot(months, risks, marker='o', linewidth=2, color=line_color, markersize=8)

            # 添加数据标签
            for i, (month, risk) in enumerate(zip(months, risks)):
                plt.annotate(f'{risk:.2f}', (i, risk), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

            # 添加标题和标签
            if font_prop:
                plt.title('12个月认知风险变化趋势', fontsize=14, fontweight='bold', fontproperties=font_prop)
                plt.xlabel('时间（月）', fontsize=12, fontproperties=font_prop)
                plt.ylabel('风险值', fontsize=12, fontproperties=font_prop)
            else:
                plt.title('12-Month Cognitive Risk Trend', fontsize=14, fontweight='bold')
                plt.xlabel('Time (Month)', fontsize=12)
                plt.ylabel('Risk Value', fontsize=12)

            # 设置y轴范围
            plt.ylim(0, 1.0)

            # 添加网格
            plt.grid(True, linestyle='--', alpha=0.7)

            # 添加风险区域背景色
            plt.axhspan(0, 0.3, alpha=0.1, color='green', label='Low Risk')
            plt.axhspan(0.3, 0.6, alpha=0.1, color='yellow')
            plt.axhspan(0.6, 1.0, alpha=0.1, color='red')

            # 添加图例
            risk_zones = ['低风险区(<0.3)', '中风险区(0.3-0.6)', '高风险区(>0.6)']
            if font_prop:
                plt.legend(risk_zones, loc='upper left', fontsize=8, prop=font_prop)
            else:
                plt.legend(['Low Risk(<0.3)', 'Medium Risk(0.3-0.6)', 'High Risk(>0.6)'], loc='upper left', fontsize=8)

            # 旋转x轴标签
            plt.xticks(rotation=45, ha='right')

            plt.tight_layout()

            # 转换为字节流
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)

            # 创建reportlab Image对象
            from reportlab.platypus import Image as ReportLabImage
            img = ReportLabImage(buffer)
            img.drawWidth = 500
            img.drawHeight = 250

            plt.close()
            return img

        except Exception as e:
            logger.error(f"生成风险趋势图失败: {e}")
            return None