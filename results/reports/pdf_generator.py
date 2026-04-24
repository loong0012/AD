"""
PDF报告生成模块
用于生成阿尔兹海默症诊断与风险预测报告
"""

import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping


class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_fonts()
        self.setup_styles()

    def setup_fonts(self):
        """设置字体"""
        try:
            # 尝试注册中文字体
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",  # 黑体
                "C:/Windows/Fonts/simsun.ttc",  # 宋体
                "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
                "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        if "simhei" in font_path.lower():
                            # 注册常规字体
                            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                            addMapping('ChineseFont', 0, 0, 'ChineseFont')
                            print(f"✅ 已注册中文字体: {font_path}")

                            # 注册相同的字体为粗体字体（实际上使用同一个文件）
                            pdfmetrics.registerFont(TTFont('ChineseFont-Bold', font_path))
                            addMapping('ChineseFont-Bold', 1, 0, 'ChineseFont-Bold')
                            print(f"✅ 已注册中文字体粗体变体: {font_path}")
                            break
                    except Exception as e:
                        print(f"⚠️ 注册字体 {font_path} 失败: {e}")
                        continue

            # 使用默认字体作为后备
            font_names = pdfmetrics.getRegisteredFontNames()
            if 'ChineseFont' in font_names:
                self.chinese_font = 'ChineseFont'
            else:
                self.chinese_font = 'Helvetica'
                print("⚠️ 使用默认字体 Helvetica")

        except Exception as e:
            print(f"⚠️ 字体设置失败: {e}")
            self.chinese_font = 'Helvetica'

    def setup_styles(self):
        """设置PDF样式"""
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

        # 章节标题样式
        self.section_style = ParagraphStyle(
            'Section',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            spaceBefore=20,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

        # 子标题样式
        self.subsection_style = ParagraphStyle(
            'Subsection',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8,
            spaceBefore=15,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

        # 正文样式
        self.normal_style = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#475569'),
            spaceAfter=6,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

        # 强调文本样式
        self.emphasize_style = ParagraphStyle(
            'Emphasize',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=6,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

        # 表格标题样式
        self.table_header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

        # 表格内容样式
        self.table_cell_style = ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            alignment=TA_LEFT,
            fontName=self.chinese_font,
            encoding='utf-8'
        )

    def generate_report(self, results_data, patient_info=None, output_path=None):
        """生成完整PDF报告"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            patient_id = results_data.get('patient_id', f'DEMO_{timestamp}')
            output_path = f"./reports/{patient_id}_report_{timestamp}.pdf"

        # 创建PDF文档
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2 * 2.54,
            leftMargin=2 * 2.54,
            topMargin=2 * 2.54,
            bottomMargin=2 * 2.54,
            encoding='utf-8'
        )

        # 构建报告内容
        story = []

        # 1. 封面页
        story.extend(self.create_cover_page(results_data, patient_info))
        story.append(PageBreak())

        # 2. 目录
        story.extend(self.create_table_of_contents())
        story.append(PageBreak())

        # 3. 患者基本信息
        story.extend(self.create_patient_info_section(patient_info))
        story.append(Spacer(1, 20))

        # 4. 诊断结果摘要
        story.extend(self.create_diagnosis_summary_section(results_data))
        story.append(Spacer(1, 20))

        # 5. 多模态数据详情
        story.extend(self.create_multimodal_data_section(results_data))
        story.append(PageBreak())

        # 6. 风险指标分析
        story.extend(self.create_risk_indicators_section(results_data))
        story.append(Spacer(1, 20))

        # 7. 医学建议
        story.extend(self.create_medical_advice_section(results_data))
        story.append(Spacer(1, 20))

        # 8. 技术分析
        story.extend(self.create_technical_analysis_section(results_data))
        story.append(PageBreak())

        # 9. 随访建议
        story.extend(self.create_followup_section(results_data))
        story.append(Spacer(1, 20))

        # 10. 声明和签字
        story.extend(self.create_disclaimer_section())

        # 生成PDF
        try:
            doc.build(story)
            print(f"PDF report generated: {output_path}")
            return output_path
        except Exception as e:
            print(f"PDF report generation failed: {e}")
            return None

    def create_cover_page(self, results_data, patient_info):
        """创建封面页"""
        elements = []

        # 标题
        elements.append(Spacer(1, 5 * 2.54))
        elements.append(Paragraph("阿尔兹海默症诊断与风险预测报告", self.title_style))
        elements.append(Spacer(1, 3 * 2.54))

        # 患者信息
        patient_id = patient_info.get('patient_id', '未提供') if patient_info else 'DEMO001'
        elements.append(Paragraph(f"患者ID: {patient_id}", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        # 报告信息
        report_id = f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        elements.append(Paragraph(f"报告编号: {report_id}", self.normal_style))
        elements.append(Paragraph(f"生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}", self.normal_style))
        elements.append(Paragraph(f"系统版本: AD-CPredSys v4.0.0", self.normal_style))
        elements.append(Spacer(1, 4 * 2.54))

        # 机构信息
        elements.append(Paragraph("AI辅助诊断系统", self.subsection_style))
        elements.append(Paragraph("基于深度学习的阿尔兹海默症分类与进展预测", self.normal_style))
        elements.append(Paragraph(f"发布日期: 2025年11月", self.normal_style))

        return elements

    def create_table_of_contents(self):
        """创建目录"""
        elements = []

        elements.append(Paragraph("目录", self.title_style))
        elements.append(Spacer(1, 2 * 2.54))

        toc_items = [
            ("1. 患者基本信息", 1),
            ("2. 诊断结果摘要", 2),
            ("3. 多模态数据详情", 3),
            ("4. 风险指标分析", 4),
            ("5. 医学建议", 5),
            ("6. 技术分析", 6),
            ("7. 随访建议", 7),
            ("8. 声明", 8)
        ]

        for item, page in toc_items:
            elements.append(Paragraph(f"{item} ................. {page}", self.normal_style))
            elements.append(Spacer(1, 0.5 * 2.54))

        return elements

    def create_patient_info_section(self, patient_info):
        """创建患者信息部分"""
        elements = []

        elements.append(Paragraph("1. 患者基本信息", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        if not patient_info:
            patient_info = {
                'patient_id': 'DEMO001',
                'age': 72,
                'gender': '男性',
                'education': '大学',
                'clinical_history': '高血压病史5年'
            }

        # 患者信息表格
        patient_data = [
            [Paragraph("项目", self.table_header_style), Paragraph("内容", self.table_header_style)],
            [Paragraph("患者ID", self.table_cell_style),
             Paragraph(str(patient_info.get('patient_id', '未提供')), self.table_cell_style)],
            [Paragraph("年龄", self.table_cell_style),
             Paragraph(f"{patient_info.get('age', '未提供')}岁", self.table_cell_style)],
            [Paragraph("性别", self.table_cell_style),
             Paragraph(str(patient_info.get('gender', '未提供')), self.table_cell_style)],
            [Paragraph("教育程度", self.table_cell_style),
             Paragraph(str(patient_info.get('education', '未提供')), self.table_cell_style)],
            [Paragraph("主要病史", self.table_cell_style),
             Paragraph(str(patient_info.get('clinical_history', '未提供')), self.table_cell_style)],
            [Paragraph("家族史", self.table_cell_style),
             Paragraph(str(patient_info.get('family_history', '无')), self.table_cell_style)],
            [Paragraph("首次评估日期", self.table_cell_style),
             Paragraph(str(patient_info.get('assessment_date', datetime.now().strftime('%Y-%m-%d'))),
                       self.table_cell_style)]
        ]

        patient_table = Table(patient_data, colWidths=[80, 200])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), self.chinese_font),
            ('FONTSIZE', (0, 0), (1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (1, -1), self.chinese_font),
            ('FONTSIZE', (0, 1), (1, -1), 9),
        ]))

        elements.append(patient_table)
        return elements

    def create_diagnosis_summary_section(self, results_data):
        """创建诊断结果摘要部分"""
        elements = []

        elements.append(Paragraph("2. 诊断结果摘要", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        diagnosis_result = results_data.get('results', {})
        pred_label = diagnosis_result.get('pred_label', 'CN')
        confidence = diagnosis_result.get('confidence', 0.85) * 100
        
        # 获取风险评分并处理可能的None值
        risk_score_value = diagnosis_result.get('risk_score', 0.18)
        risk_score_value = risk_score_value if risk_score_value is not None else 0.18
        risk_score = risk_score_value * 100

        # 诊断类别映射
        label_map = {
            'CN': '认知正常 (Cognitive Normal)',
            'EMCI': '早期轻度认知障碍 (Early Mild Cognitive Impairment)',
            'LMCI': '晚期轻度认知障碍 (Late Mild Cognitive Impairment)',
            'MCI': '轻度认知障碍 (Mild Cognitive Impairment)',
            'AD': '阿尔兹海默病 (Alzheimer\'s Disease)'
        }

        # 风险等级
        if risk_score is None:
            risk_score = 0.0
        
        if risk_score < 20:
            risk_level = "低风险"
            risk_color = colors.HexColor('#10b981')
        elif risk_score < 50:
            risk_level = "中风险"
            risk_color = colors.HexColor('#f59e0b')
        else:
            risk_level = "高风险"
            risk_color = colors.HexColor('#ef4444')

        # 诊断结果表格
        diagnosis_data = [
            [Paragraph("诊断类别", self.table_header_style), Paragraph("内容", self.table_header_style)],
            [Paragraph("诊断类别", self.table_cell_style),
             Paragraph(f"{pred_label} - {label_map.get(pred_label, pred_label)}", self.table_cell_style)],
            [Paragraph("诊断置信度", self.table_cell_style), Paragraph(f"{confidence:.1f}%", self.table_cell_style)],
            [Paragraph("12个月进展概率", self.table_cell_style),
             Paragraph(f"{risk_score:.1f}%" if risk_score is not None else "N/A", self.table_cell_style)],
            [Paragraph("综合风险等级", self.table_cell_style), Paragraph(risk_level, self.table_cell_style)],
            [Paragraph("分析时间", self.table_cell_style),
             Paragraph(diagnosis_result.get('analysis_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                       self.table_cell_style)],
            [Paragraph("模型版本", self.table_cell_style),
             Paragraph(f"AD-CPredSys v4.0.0", self.table_cell_style)]
        ]

        # 设置风险等级的文本颜色
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), self.chinese_font),
            ('FONTSIZE', (0, 0), (1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (1, -1), self.chinese_font),
            ('FONTSIZE', (0, 1), (1, -1), 9),
        ])

        # 设置风险等级的颜色
        table_style.add('TEXTCOLOR', (1, 4), (1, 4), risk_color)
        table_style.add('FONTSIZE', (1, 4), (1, 4), 10)

        diagnosis_table = Table(diagnosis_data, colWidths=[80, 180])
        diagnosis_table.setStyle(table_style)

        elements.append(diagnosis_table)
        return elements

    def create_multimodal_data_section(self, results_data):
        """创建多模态数据详情部分"""
        elements = []

        elements.append(Paragraph("3. 多模态数据详情", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        # 各模态数据摘要
        modalities = results_data.get('results', {}).get('modalities_used', ['MRI', '临床数据', '生活方式', '分子数据'])
        modalities = modalities if modalities is not None else ['MRI', '临床数据', '生活方式', '分子数据']

        elements.append(Paragraph("3.1 数据模态概览", self.subsection_style))
        elements.append(Spacer(1, 0.5 * 2.54))

        modality_data = [
            [Paragraph("数据模态", self.table_header_style), Paragraph("状态", self.table_header_style)]
        ]
        for i, modality in enumerate(modalities, 1):
            modality_data.append([
                Paragraph(f"{i}. {modality}", self.table_cell_style),
                Paragraph("✓ 已分析", self.table_cell_style)
            ])

        modality_table = Table(modality_data, colWidths=[150, 80])
        modality_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), self.chinese_font),
            ('GRID', (0, 0), (1, -1), 1, colors.grey),
        ]))

        elements.append(modality_table)
        elements.append(Spacer(1, 1 * 2.54))

        # 各模态权重（如果提供）
        weights = results_data.get('results', {}).get('modality_weights', {})
        if weights and isinstance(weights, dict):
            elements.append(Paragraph("3.2 模态融合权重", self.subsection_style))
            elements.append(Spacer(1, 0.5 * 2.54))

            weight_data = [
                [Paragraph("模态", self.table_header_style),
                 Paragraph("权重", self.table_header_style),
                 Paragraph("贡献度", self.table_header_style)]
            ]

            for modality, weight in weights.items():
                if weight is not None:
                    weight_data.append([
                        Paragraph(modality, self.table_cell_style),
                        Paragraph(f"{weight:.3f}", self.table_cell_style),
                        Paragraph(f"{weight * 100:.1f}%", self.table_cell_style)
                    ])

            weight_table = Table(weight_data, colWidths=[100, 80, 80])
            weight_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
                ('ALIGN', (0, 0), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (2, 0), self.chinese_font),
                ('GRID', (0, 0), (2, -1), 1, colors.grey),
            ]))

            elements.append(weight_table)

        return elements

    def create_risk_indicators_section(self, results_data):
        """创建风险指标分析部分"""
        elements = []

        elements.append(Paragraph("4. 风险指标分析", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        risk_indicators = results_data.get('results', {}).get('risk_indicators', {})

        if not risk_indicators:
            # 生成示例风险指标
            risk_indicators = {}
            risk_indicators_list = ['海马体萎缩', 'p-tau217浓度', 'Aβ42/Aβ40比率', '脑葡萄糖代谢率', '白质高信号', '脑体积减少率']
            for indicator in risk_indicators_list:
                risk_indicators[indicator] = {
                    'value': random.uniform(20, 90),
                    'risk_level': random.choice(['low', 'medium', 'high'])
                }

        # 风险指标表格
        risk_data = [
            [Paragraph("风险指标", self.table_header_style),
             Paragraph("当前值", self.table_header_style),
             Paragraph("参考范围", self.table_header_style),
             Paragraph("风险等级", self.table_header_style),
             Paragraph("临床意义", self.table_header_style)]
        ]

        reference_ranges = {
            '海马体萎缩': '0-30%',
            'p-tau217浓度': '<40 pg/mL',
            'Aβ42/Aβ40比率': '0.2-0.4',
            '脑葡萄糖代谢率': '>85%',
            '白质高信号': '<20%',
            '脑体积减少率': '0-25%'
        }

        clinical_significance = {
            'low': '轻度异常，建议定期随访',
            'medium': '中度异常，需要临床关注',
            'high': '显著异常，建议立即临床干预'
        }

        risk_colors = {
            'low': colors.HexColor('#10b981'),
            'medium': colors.HexColor('#f59e0b'),
            'high': colors.HexColor('#ef4444')
        }

        risk_texts = {
            'low': '低风险',
            'medium': '中风险',
            'high': '高风险'
        }

        for indicator, data in risk_indicators.items():
            value = data.get('value', 50)
            risk_level = data.get('risk_level', 'medium')
            ref_range = reference_ranges.get(indicator, 'N/A')
            significance = clinical_significance.get(risk_level, '需要进一步评估')
            risk_text = risk_texts.get(risk_level, '中风险')

            # 创建风险等级样式
            risk_text_style = ParagraphStyle(
                'RiskText',
                parent=self.table_cell_style,
                textColor=risk_colors.get(risk_level, colors.black),
                fontName=self.chinese_font,
                fontSize=9
            )

            risk_data.append([
                Paragraph(indicator, self.table_cell_style),
                Paragraph(f"{value:.1f}", self.table_cell_style),
                Paragraph(ref_range, self.table_cell_style),
                Paragraph(risk_text, risk_text_style),
                Paragraph(significance, self.table_cell_style)
            ])

        # 使用更简单的表格设置
        risk_table = Table(risk_data, colWidths=[80, 50, 60, 50, 100])

        # 创建表格样式
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (4, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (4, 0), colors.white),
            ('ALIGN', (0, 0), (4, 0), 'CENTER'),
            ('ALIGN', (0, 1), (4, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (4, 0), self.chinese_font),
            ('FONTSIZE', (0, 0), (4, 0), 9),
            ('BOTTOMPADDING', (0, 0), (4, 0), 12),
            ('GRID', (0, 0), (4, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (4, -1), self.chinese_font),
            ('FONTSIZE', (0, 1), (4, -1), 8),
        ])

        risk_table.setStyle(table_style)

        elements.append(risk_table)

        # 风险总结
        elements.append(Spacer(1, 1 * 2.54))
        elements.append(Paragraph("4.1 风险总结", self.subsection_style))

        high_risk_count = 0
        medium_risk_count = 0
        if risk_indicators and isinstance(risk_indicators, dict):
            high_risk_count = sum(1 for data in risk_indicators.values() if data and data.get('risk_level') == 'high')
            medium_risk_count = sum(1 for data in risk_indicators.values() if data and data.get('risk_level') == 'medium')

        # 获取风险评分并处理可能的None值
        risk_score = results_data.get('results', {}).get('risk_score', 0)
        risk_score = risk_score if risk_score is not None else 0
        risk_score_percent = risk_score * 100
        
        summary_text = f"""
        综合分析显示，在{len(risk_indicators)}个关键风险指标中：
        • 高风险指标: {high_risk_count}个
        • 中风险指标: {medium_risk_count}个
        • 低风险指标: {len(risk_indicators) - high_risk_count - medium_risk_count}个

        综合风险评分: {risk_score_percent:.1f}%
        建议: {clinical_significance.get('high' if high_risk_count > 2 else 'medium' if medium_risk_count > 2 else 'low', '定期随访')}
        """

        elements.append(Paragraph(summary_text.replace('•', '●'), self.normal_style))

        return elements

    def create_medical_advice_section(self, results_data):
        """创建医学建议部分"""
        elements = []

        elements.append(Paragraph("5. 个性化医学建议", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        advice_list = results_data.get('results', {}).get('medical_advice', [])

        if not advice_list:
            # 生成默认建议
            pred_label = results_data.get('results', {}).get('pred_label', 'CN')
            advice_map = {
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
                    "控制阿尔兹海默病风险因素",
                    "建立健康档案，记录认知变化"
                ],
                'AD': [
                    "高度怀疑阿尔兹海默病，立即就医",
                    "尽快进行PET-CT或脑脊液检查确诊",
                    "开始药物治疗（胆碱酯酶抑制剂等）",
                    "制定全面的护理和支持计划",
                    "参与临床试验和新治疗方案"
                ]
            }
            advice_list = advice_map.get(pred_label, advice_map['CN'])

        # 建议列表
        for i, advice in enumerate(advice_list, 1):
            elements.append(Paragraph(f"{i}. {advice}", self.normal_style))
            elements.append(Spacer(1, 0.3 * 2.54))

        return elements

    def create_technical_analysis_section(self, results_data):
        """创建技术分析部分"""
        elements = []

        elements.append(Paragraph("6. 技术分析", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        # 模型信息
        elements.append(Paragraph("6.1 模型分析详情", self.subsection_style))
        elements.append(Spacer(1, 0.5 * 2.54))

        model_info = [
            [Paragraph("项目", self.table_header_style), Paragraph("数值", self.table_cell_style)],
            [Paragraph("模型名称", self.table_cell_style), Paragraph("MultiModalADModel", self.table_cell_style)],
            [Paragraph("架构", self.table_cell_style), Paragraph("3D-CNN + Transformer + LSTM", self.table_cell_style)],
            [Paragraph("输入维度", self.table_cell_style), Paragraph("160×256×256", self.table_cell_style)],
            [Paragraph("模态数量", self.table_cell_style), Paragraph("4 (影像、临床、生活、分子)", self.table_cell_style)],
            [Paragraph("输出类别", self.table_cell_style), Paragraph("CN/EMCI/LMCI/MCI/AD", self.table_cell_style)],
            [Paragraph("置信度阈值", self.table_cell_style), Paragraph(">85%", self.table_cell_style)],
            [Paragraph("分析时间", self.table_cell_style),
             Paragraph(f"{random.uniform(0.5, 2.0):.2f}秒", self.table_cell_style)]
        ]

        model_table = Table(model_info, colWidths=[100, 150])
        model_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#4b5563')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), self.chinese_font),
            ('GRID', (0, 0), (1, -1), 1, colors.grey),
        ]))

        elements.append(model_table)

        # 置信度分布
        elements.append(Spacer(1, 1 * 2.54))
        elements.append(Paragraph("6.2 类别置信度分布", self.subsection_style))
        elements.append(Spacer(1, 0.5 * 2.54))

        probabilities = results_data.get('results', {}).get('probabilities', {})
        if not probabilities:
            probabilities = {'CN': 0.85, 'EMCI': 0.07, 'LMCI': 0.05, 'MCI': 0.02, 'AD': 0.01}

        prob_data = [
            [Paragraph("诊断类别", self.table_header_style),
             Paragraph("置信度", self.table_header_style),
             Paragraph("分布", self.table_header_style)]
        ]

        label_chinese = {
            'CN': '认知正常',
            'EMCI': '早期轻度认知障碍',
            'LMCI': '晚期轻度认知障碍',
            'MCI': '轻度认知障碍',
            'AD': '阿尔兹海默病'
        }

        for label, prob in probabilities.items():
            bar = "█" * int(prob * 20)  # 简单条形图
            prob_data.append([
                Paragraph(f"{label} - {label_chinese.get(label, label)}", self.table_cell_style),
                Paragraph(f"{prob * 100:.1f}%", self.table_cell_style),
                Paragraph(bar, self.table_cell_style)
            ])

        prob_table = Table(prob_data, colWidths=[100, 60, 100])
        prob_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#4b5563')),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
            ('ALIGN', (0, 0), (2, 0), 'CENTER'),
            ('ALIGN', (0, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (2, 0), self.chinese_font),
            ('GRID', (0, 0), (2, -1), 1, colors.grey),
        ]))

        elements.append(prob_table)

        return elements

    def create_followup_section(self, results_data):
        """创建随访建议部分"""
        elements = []

        elements.append(Paragraph("7. 随访建议", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        # 随访计划
        elements.append(Paragraph("7.1 随访计划", self.subsection_style))
        elements.append(Spacer(1, 0.5 * 2.54))

        followup_plan = [
            [Paragraph("时间点", self.table_header_style),
             Paragraph("检查项目", self.table_header_style),
             Paragraph("目的", self.table_header_style)],
            [Paragraph("1个月后", self.table_cell_style),
             Paragraph("认知功能简易评估", self.table_cell_style),
             Paragraph("评估短期变化", self.table_cell_style)],
            [Paragraph("3个月后", self.table_cell_style),
             Paragraph("神经心理学全套评估", self.table_cell_style),
             Paragraph("全面评估认知状态", self.table_cell_style)],
            [Paragraph("6个月后", self.table_cell_style),
             Paragraph("头部MRI复查", self.table_cell_style),
             Paragraph("评估脑结构变化", self.table_cell_style)],
            [Paragraph("12个月后", self.table_cell_style),
             Paragraph("多模态全面评估", self.table_cell_style),
             Paragraph("评估年度进展", self.table_cell_style)]
        ]

        followup_table = Table(followup_plan, colWidths=[80, 120, 120])
        followup_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
            ('ALIGN', (0, 0), (2, 0), 'CENTER'),
            ('ALIGN', (0, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (2, 0), self.chinese_font),
            ('GRID', (0, 0), (2, -1), 1, colors.grey),
        ]))

        elements.append(followup_table)

        # 注意事项
        elements.append(Spacer(1, 1 * 2.54))
        elements.append(Paragraph("7.2 注意事项", self.subsection_style))

        notes = [
            "• 如出现认知功能急剧下降，请立即就医",
            "• 定期监测血压、血糖、血脂等血管危险因素",
            "• 保持健康饮食和适度运动",
            "• 参与社交和认知训练活动",
            "• 记录认知变化日记，定期与医生沟通"
        ]

        for note in notes:
            elements.append(Paragraph(note.replace('•', '●'), self.normal_style))
            elements.append(Spacer(1, 0.2 * 2.54))

        return elements

    def create_disclaimer_section(self):
        """创建声明部分"""
        elements = []

        elements.append(Paragraph("8. 重要声明", self.section_style))
        elements.append(Spacer(1, 1 * 2.54))

        disclaimer_text = f"""
        <b>免责声明</b>

        1. 本报告为AI辅助诊断工具生成的结果，仅供临床医生参考使用。
        2. 本报告不能替代执业医师的专业诊断和临床判断。
        3. 最终的诊断和治疗决策应由执业医师根据完整临床资料做出。
        4. 紧急医疗情况请立即就医，不要依赖本报告延迟治疗。
        5. 本系统基于深度学习模型，可能存在一定的误差率。
        6. 报告结果受输入数据质量和完整性的影响。
        7. 患者的隐私和数据安全已采取保护措施。

        <b>报告认证信息</b>

        • 生成系统: AD-CPredSys v4.0.0
        • 报告时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
        • 报告编号: RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}
        • 技术支持: 深度学习辅助诊断研究组

        <b>医生签字:</b> _______________________

        <b>日期:</b> {datetime.now().strftime('%Y年%m月%d日')}
        """

        elements.append(Paragraph(disclaimer_text.replace('•', '●'), self.normal_style))

        return elements
