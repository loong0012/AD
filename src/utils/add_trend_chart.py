#!/usr/bin/env python3
"""
添加风险趋势图生成方法
"""

import os

file_path = 'd:\\Desktop\\Alzheimer-diagnostic system\\src\\Alzheimer_diagnostic_system.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到_generate_brain_risk_heatmap方法的结尾，在其后添加新方法
old_heatmap_end = '''            plt.close()
            return img
        except Exception as e:
            logger.error(f"生成脑区风险热力图失败: {e}")
            return None'''

new_heatmap_end = '''            plt.close()
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
            return None'''

content = content.replace(old_heatmap_end, new_heatmap_end)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("风险趋势图生成方法添加完成！")
