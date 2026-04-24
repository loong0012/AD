#!/usr/bin/env python3
"""
完善PDF报告内容，确保包含所有诊断模块
"""

import os

# 读取原文件
file_path = 'd:\\Desktop\\Alzheimer-diagnostic system\\src\\Alzheimer_diagnostic_system.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换完整的generate_report方法
old_generate_report = '''    def generate_report(self, results_data, patient_info):
        """
        生成PDF报告
        :param results_data: 诊断结果数据
        :param patient_info: 患者信息
        :return: PDF文件路径
        """
        try:
            # 这里是一个示例实现，实际应该使用reportlab或其他库生成PDF
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
                # 尝试注册Windows字体
                pdfmetrics.registerFont(TTFont('SimHei', 'C:\\\\Windows\\\\Fonts\\\\simhei.ttf'))
                pdfmetrics.registerFont(TTFont('SimSun', 'C:\\\\Windows\\\\Fonts\\\\simsun.ttc'))
                chinese_font_name = 'SimHei'
                chinese_font_name_serif = 'SimSun'
            except Exception as e:
                logger.warning(f"注册中文字体失败: {e}")
                chinese_font_name = 'Helvetica'
                chinese_font_name_serif = 'Helvetica'
            
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
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontName=chinese_font_name,
                fontSize=24,
                textColor=colors.HexColor('#1a56db'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading1_style = ParagraphStyle(
                'CustomHeading1',
                parent=styles['Heading1'],
                fontName=chinese_font_name,
                fontSize=18,
                textColor=colors.HexColor('#1e429f'),
                spaceBefore=20,
                spaceAfter=15
            )
            
            heading2_style = ParagraphStyle(
                'CustomHeading2',
                parent=styles['Heading2'],
                fontName=chinese_font_name,
                fontSize=14,
                textColor=colors.HexColor('#3b82f6'),
                spaceBefore=15,
                spaceAfter=10
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontName=chinese_font_name,
                fontSize=12,
                leading=18
            )
            
            # 添加标题
            title = Paragraph("阿尔兹海默症诊断报告", title_style)
            elements.append(title)
            
            # 添加医院和系统信息
            hospital_info = Paragraph("<b>医院名称:</b> 示例医院神经内科", body_style)
            elements.append(hospital_info)
            system_info = Paragraph("<b>系统版本:</b> 阿尔兹海默症诊断系统 v3.0.0", body_style)
            elements.append(system_info)
            elements.append(Spacer(1, 30))
            
            # 添加患者信息
            patient_info_title = Paragraph("患者信息", heading1_style)
            elements.append(patient_info_title)
            
            # 整理患者信息数据
            patient_data = []
            patient_data.append([Paragraph("<b>项目</b>", body_style), Paragraph("<b>值</b>", body_style)])
            
            # 基本信息
            basic_info = {
                '姓名': patient_info.get('name', '未知'),
                '年龄': patient_info.get('age', '未知'),
                '性别': patient_info.get('gender', '未知'),
                '教育年限': patient_info.get('education_years', '未知'),
                '联系方式': patient_info.get('contact_info', '未知'),
                '病史': patient_info.get('medical_history', '无')
            }
            
            for key, value in basic_info.items():
                patient_data.append([Paragraph(key, body_style), Paragraph(str(value), body_style)])
            
            # 检查是否有生活方式数据
            if 'lifestyle_data' in patient_info:
                elements.append(Spacer(1, 15))
                lifestyle_title = Paragraph("生活方式信息", heading2_style)
                elements.append(lifestyle_title)
                
                lifestyle_info = patient_info['lifestyle_data']
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
                
                for key, label in lifestyle_map.items():
                    value = lifestyle_info.get(key, '未知')
                    # 转换值为更友好的显示
                    if key == 'diet_health':
                        value_map = {'low': '差', 'medium': '中等', 'high': '良好'}
                        value = value_map.get(value, value)
                    elif key == 'smoking_status':
                        value_map = {'never': '从不吸烟', 'past': '曾经吸烟', 'current': '正在吸烟'}
                        value = value_map.get(value, value)
                    elif key == 'alcohol_consumption':
                        value_map = {'none': '不饮酒', 'occasional': '偶尔饮酒', 'regular': '经常饮酒'}
                        value = value_map.get(value, value)
                    
                    lifestyle_data.append([Paragraph(label, body_style), Paragraph(str(value), body_style)])
                
                # 创建生活方式表格
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
            
            # 创建患者基本信息表格
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
            
            # 添加诊断结果
            diagnosis_title = Paragraph("诊断结果", heading1_style)
            elements.append(diagnosis_title)
            
            if 'results' in results_data:
                results = results_data['results']
                
                # 诊断结果
                pred_label = results.get('pred_label', '未知')
                confidence = results.get('confidence', 0.0)
                risk_score = results.get('risk_score', 0.0)
                
                # 转换诊断结果为中文
                label_map = {
                    'CN': '认知正常',
                    'EMCI': '早期轻度认知障碍',
                    'LMCI': '晚期轻度认知障碍',
                    'AD': '阿尔茨海默病'
                }
                pred_label_cn = label_map.get(pred_label, pred_label)
                
                diagnosis_data = []
                diagnosis_data.append([Paragraph("<b>项目</b>", body_style), Paragraph("<b>结果</b>", body_style)])
                diagnosis_data.append([Paragraph("诊断结果", body_style), Paragraph(pred_label_cn, body_style)])
                diagnosis_data.append([Paragraph("置信度", body_style), Paragraph(f"{confidence:.2f}", body_style)])
                diagnosis_data.append([Paragraph("风险评分", body_style), Paragraph(f"{risk_score:.2f}", body_style)])
                
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
                
                # 添加脑部图像分析
                if IMAGE_LIBS_AVAILABLE:
                    try:
                        # 生成脑部头像分析图像
                        brain_image = self._generate_brain_analysis_image(pred_label)
                        if brain_image:
                            brain_image_title = Paragraph("脑部分析图像", heading2_style)
                            elements.append(brain_image_title)
                            elements.append(brain_image)
                            elements.append(Spacer(1, 20))
                        
                        # 生成脑区风险热力图像
                        heatmap_image = self._generate_brain_risk_heatmap(risk_score, results.get('risk_indicators', {}))
                        if heatmap_image:
                            heatmap_title = Paragraph("脑区风险热力图", heading2_style)
                            elements.append(heatmap_title)
                            elements.append(heatmap_image)
                            elements.append(Spacer(1, 20))
                    except Exception as e:
                        logger.error("生成脑部图像失败", e)
                
                # 风险指标
                if 'risk_indicators' in results:
                    risk_indicators = results['risk_indicators']
                    risk_title = Paragraph("风险指标", heading2_style)
                    elements.append(risk_title)
                    
                    risk_data = []
                    risk_data.append([Paragraph("<b>指标</b>", body_style), Paragraph("<b>值</b>", body_style), Paragraph("<b>风险等级</b>", body_style)])
                    
                    for indicator_name, indicator in risk_indicators.items():
                        risk_data.append([
                            Paragraph(indicator_name, body_style),
                            Paragraph(str(indicator['value']), body_style),
                            Paragraph(indicator['risk_level'], body_style)
                        ])
                    
                    risk_table = Table(risk_data, colWidths=[150, 100, 100])
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
                
                # 建议
                if 'recommendations' in results:
                    recommendations = results['recommendations']
                    rec_title = Paragraph("建议", heading2_style)
                    elements.append(rec_title)
                    
                    for i, recommendation in enumerate(recommendations, 1):
                        rec_text = Paragraph(f"{i}. {recommendation}", body_style)
                        elements.append(rec_text)
                    elements.append(Spacer(1, 20))
                
                # 月度风险预测
                if 'monthly_risk' in results:
                    monthly_risk = results['monthly_risk']
                    if monthly_risk:
                        risk_trend_title = Paragraph("风险趋势预测", heading2_style)
                        elements.append(risk_trend_title)
                        
                        # 简单的风险趋势表格
                        trend_data = []
                        trend_data.append([Paragraph("<b>月份</b>", body_style), Paragraph("<b>风险值</b>", body_style)])
                        
                        for item in monthly_risk[:6]:  # 只显示前6个月
                            trend_data.append([
                                Paragraph(str(item['month']), body_style),
                                Paragraph(f"{item['risk']:.3f}", body_style)
                            ])
                        
                        trend_table = Table(trend_data, colWidths=[100, 100])
                        trend_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dcfce7')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#15803d')),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                            ('TOPPADDING', (0, 0), (-1, 0), 10),
                            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
                        ]))
                        elements.append(trend_table)
                        elements.append(Spacer(1, 20))
            
            # 添加医生信息
            doctor_info_title = Paragraph("医生信息", heading1_style)
            elements.append(doctor_info_title)
            
            doctor_data = []
            doctor_data.append([Paragraph("<b>项目</b>", body_style), Paragraph("<b>值</b>", body_style)])
            doctor_data.append([Paragraph("主治医生", body_style), Paragraph("示例医生", body_style)])
            doctor_data.append([Paragraph("科室", body_style), Paragraph("神经内科", body_style)])
            doctor_data.append([Paragraph("联系方式", body_style), Paragraph("138****8888", body_style)])
            
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
            
            # 添加报告说明
            note_title = Paragraph("报告说明", heading1_style)
            elements.append(note_title)
            
            notes = [
                "1. 本报告由阿尔兹海默症诊断系统自动生成，仅供参考。",
                "2. 诊断结果基于患者提供的信息和系统分析，最终诊断以医生临床判断为准。",
                "3. 建议患者定期复诊，以便及时调整治疗方案。",
                "4. 保持健康的生活方式对预防和延缓阿尔兹海默症的进展有重要作用。"
            ]
            
            for note in notes:
                note_text = Paragraph(note, body_style)
                elements.append(note_text)
            elements.append(Spacer(1, 30))
            
            # 添加生成时间和页码
            timestamp_text = Paragraph(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style)
            elements.append(timestamp_text)
            
            # 生成PDF
            doc.build(elements)
            
            logger.info(f"PDF报告生成成功: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error("PDF报告生成失败", e)
            # 生成一个简单的JSON文件作为替代
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            patient_id = patient_info.get('patient_id', 'unknown')
            filename = f"diagnosis_report_{patient_id}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            report_data = {
                'patient_info': patient_info,
                'results_data': results_data,
                'generated_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            logger.warning(f"生成JSON报告作为替代: {filepath}")
            return filepath'''

# 新的完整generate_report方法
new_generate_report = '''    def generate_report(self, results_data, patient_info):
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
                pdfmetrics.registerFont(TTFont('SimHei', 'C:\\\\Windows\\\\Fonts\\\\simhei.ttf'))
                pdfmetrics.registerFont(TTFont('SimSun', 'C:\\\\Windows\\\\Fonts\\\\simsun.ttc'))
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
            title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontName=chinese_font_name, fontSize=24, textColor=colors.HexColor('#1a56db'), spaceAfter=30, alignment=TA_CENTER)
            heading1_style = ParagraphStyle('CustomHeading1', parent=styles['Heading1'], fontName=chinese_font_name, fontSize=18, textColor=colors.HexColor('#1e429f'), spaceBefore=20, spaceAfter=15)
            heading2_style = ParagraphStyle('CustomHeading2', parent=styles['Heading2'], fontName=chinese_font_name, fontSize=14, textColor=colors.HexColor('#3b82f6'), spaceBefore=15, spaceAfter=10)
            body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'], fontName=chinese_font_name, fontSize=12, leading=18)
            toc_style = ParagraphStyle('TocEntry', parent=styles['Normal'], fontName=chinese_font_name, fontSize=11, leading=16)
            
            # ========== 添加报告目录 ==========
            elements.append(Paragraph("目 录", title_style))
            elements.append(Spacer(1, 20))
            
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
                toc_text = Paragraph(f"{toc_item} ............................. {page}", toc_style)
                elements.append(toc_text)
            
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
            
            # 生活方式数据
            if 'lifestyle_data' in patient_info:
                elements.append(Spacer(1, 15))
                elements.append(Paragraph("生活方式信息", heading2_style))
                
                lifestyle_info = patient_info['lifestyle_data']
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
            
            if 'results' in results_data:
                results = results_data['results']
                
                pred_label = results.get('pred_label', '未知')
                confidence = results.get('confidence', 0.0)
                risk_score = results.get('risk_score', 0.0)
                
                label_map = {'CN': '认知正常', 'EMCI': '早期轻度认知障碍', 'LMCI': '晚期轻度认知障碍', 'AD': '阿尔茨海默病'}
                pred_label_cn = label_map.get(pred_label, pred_label)
                
                # 风险等级判定
                if risk_score < 0.3:
                    risk_level = "低风险"
                    risk_color = colors.HexColor('#10b981')
                elif risk_score < 0.6:
                    risk_level = "中风险"
                    risk_color = colors.HexColor('#f59e0b')
                else:
                    risk_level = "高风险"
                    risk_color = colors.HexColor('#ef4444')
                
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
                
                # ========== 三、脑部图像分析 ==========
                elements.append(Paragraph("三、脑部图像分析", heading1_style))
                
                if IMAGE_LIBS_AVAILABLE:
                    try:
                        brain_image = self._generate_brain_analysis_image(pred_label)
                        if brain_image:
                            brain_desc = Paragraph(f"<b>图1:</b> 脑部结构分析图 - 显示{pred_label_cn}状态下的脑区分布情况", body_style)
                            elements.append(brain_desc)
                            elements.append(Spacer(1, 10))
                            elements.append(brain_image)
                            elements.append(Spacer(1, 15))
                            
                            # 添加脑区说明
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
                
                # ========== 四、脑区风险热力图 ==========
                elements.append(Paragraph("四、脑区风险热力图", heading1_style))
                
                if IMAGE_LIBS_AVAILABLE:
                    try:
                        heatmap_image = self._generate_brain_risk_heatmap(risk_score, results.get('risk_indicators', {}))
                        if heatmap_image:
                            heatmap_desc = Paragraph(f"<b>图2:</b> 脑区风险热力图 - 展示不同脑区的风险程度(风险值越高颜色越深)", body_style)
                            elements.append(heatmap_desc)
                            elements.append(Spacer(1, 10))
                            elements.append(heatmap_image)
                            elements.append(Spacer(1, 15))
                            
                            # 添加热力图说明
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
                
                # ========== 五、关键风险指标 ==========
                elements.append(Paragraph("五、关键风险指标", heading1_style))
                
                if 'risk_indicators' in results:
                    risk_indicators = results['risk_indicators']
                    
                    risk_data = []
                    risk_data.append([Paragraph("<b>指标名称</b>", body_style), Paragraph("<b>检测值</b>", body_style), Paragraph("<b>风险等级</b>", body_style), Paragraph("<b>参考说明</b>", body_style)])
                    
                    indicator_refs = {
                        '年龄风险': '年龄越大风险越高',
                        '教育程度': '教育年限越少风险越高',
                        '家族史': '有家族史风险增加',
                        '生活方式': '不良生活方式增加风险',
                        '认知功能': '认知功能下降是重要指标'
                    }
                    
                    for indicator_name, indicator in risk_indicators.items():
                        ref = indicator_refs.get(indicator_name, '')
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
                
                # ========== 六、12个月进展预测 ==========
                elements.append(Paragraph("六、12个月进展预测", heading1_style))
                
                if 'monthly_risk' in results and results['monthly_risk']:
                    monthly_risk = results['monthly_risk']
                    
                    # 生成趋势图
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
                    
                    # 风险趋势表格
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
                    
                    # 添加趋势分析
                    if len(monthly_risk) >= 2:
                        first_risk = monthly_risk[0].get('risk', 0)
                        last_risk = monthly_risk[-1].get('risk', 0)
                        total_change = last_risk - first_risk
                        
                        trend_analysis = Paragraph(f"<b>趋势分析:</b> 未来12个月风险值从{first_risk:.3f}变化到{last_risk:.3f}，总体{'上升' if total_change > 0 else '下降' if total_change < 0 else '保持稳定'}{abs(total_change):.3f}。", body_style)
                        elements.append(Spacer(1, 10))
                        elements.append(trend_analysis)
                
                elements.append(PageBreak())
                
                # ========== 七、个性化指导建议 ==========
                elements.append(Paragraph("七、个性化指导建议", heading1_style))
                
                if 'recommendations' in results:
                    recommendations = results['recommendations']
                    
                    # 添加建议分类
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
                
                # ========== 八、医生信息和报告说明 ==========
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
                
                # 报告说明
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
                
                # 报告元数据
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
            raise e'''

content = content.replace(old_generate_report, new_generate_report)

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("PDF报告内容完善完成！")
print("\n新增内容：")
print("1. 报告目录（包含8个主要部分）")
print("2. 诊断结果概要（包含风险等级判定）")
print("3. 脑部图像分析（带详细图例说明）")
print("4. 脑区风险热力图（带颜色说明）")
print("5. 关键风险指标（增加参考说明列）")
print("6. 12个月进展预测（添加趋势图和变化分析）")
print("7. 个性化指导建议（分类展示）")
print("8. 医生信息和报告说明（包含报告编号）")
