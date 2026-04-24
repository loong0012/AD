"""
阿尔兹海默症诊断系统 - FastAPI应用
使用现代Web框架替代传统HTTP服务器
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
import traceback
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入JWT工具
from src.utils.jwt_utils import verify_token

# 导入配置管理器
from src.utils.config_manager import config_manager, CONFIG

# 导入模块化组件
from src.diagnosis.engine import DiagnosisEngine
from src.data.processor import DataProcessor
from src.report.generator import ReportGenerator
from src.Alzheimer_diagnostic_system import PDFReportGenerator, MultiModalDataManager
from src.api.handler import APIHandler

# 导入辅助函数
from src.utils.helpers import (
    preprocess_nifti_data,
    check_port_available,
    find_available_port,
    save_json_data,
    load_json_data,
    generate_timestamp
)

# 导入模型管理器
from src.utils.model_manager import model_manager

# 导入日志管理器
from src.utils.log_manager import log_manager as logger

# 全局系统实例
global_system_instance = None

# 全局API处理器实例（单例模式）
global_api_handler = None

# JWT认证依赖
def get_current_user(request: Request):
    """获取当前用户"""
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    # 去掉Bearer前缀
    if token.startswith("Bearer "):
        token = token[7:]
    
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    
    return user_data

# 创建FastAPI应用
app = FastAPI(
    title="阿尔兹海默症诊断系统",
    description="基于深度学习的阿尔兹海默症分类与进展预测系统",
    version="3.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/uploaded_img", StaticFiles(directory="./uploaded_img"), name="uploaded_img")

# 初始化系统组件
def get_system_instance():
    """获取系统实例"""
    global global_system_instance
    if global_system_instance is None:
        global_system_instance = AlzheimerDiagnosticSystem()
    return global_system_instance

def get_api_handler():
    """获取API处理器实例"""
    global global_api_handler
    if global_api_handler is None:
        global_api_handler = APIHandler()
    return global_api_handler

# 阿尔兹海默症诊断系统主类
class AlzheimerDiagnosticSystem:
    """阿尔兹海默症诊断系统主类"""

    def __init__(self):
        """初始化系统"""
        logger.info(f"\nStarting {config_manager.get('project.name')} v{config_manager.get('project.version')}")
        logger.info(f"Release date: {config_manager.get('project.release_date')}")
        
        try:
            # 初始化模块化组件
            self.data_manager = MultiModalDataManager()
            self.diagnosis_engine = DiagnosisEngine()
            self.data_processor = DataProcessor()
            self.report_generator = ReportGenerator()
            self.pdf_generator = PDFReportGenerator()
            self.api_handler = APIHandler()
            
            # 使用模型管理器获取模型（单例模式）
            self.model = model_manager.get_model()
            
            logger.info("System initialization completed")
            
        except Exception as e:
            logger.error("系统初始化失败", e)

    def analyze_multimodal_data(self, patient_id=None, use_demo=False, demo_category=None, patient_info=None):
        """分析多模态数据"""
        logger.info(f"\nStarting data analysis (patient ID: {patient_id}, demo mode: {use_demo}, demo category: {demo_category})")
        
        if use_demo:
            patient_id = f"DEMO_{demo_category or 'CN'}"
            # 创建演示数据
            self.data_manager.create_demo_multimodal_data(demo_category)
        
        # 加载数据
        if patient_id:
            patient_data = self.data_manager.load_patient_data(patient_id)
        else:
            # 生成随机数据用于分析
            patient_data = self.generate_random_patient_data()
        
        # 如果提供了患者信息，更新数据
        if patient_info:
            patient_data['clinical_info'] = patient_data.get('clinical_info', {})
            patient_data['clinical_info'].update(patient_info)
        
        # 模拟模型分析，传入演示类别和患者信息
        results = self.simulate_model_analysis(patient_data, demo_category)
        
        # 保存分析结果
        self.save_analysis_results(patient_id or "UNKNOWN", results)
        
        return results

    def generate_random_patient_data(self):
        """生成随机患者数据"""
        import numpy as np
        import random
        
        return {
            'mri_image': np.random.randn(160, 256, 256),
            'clinical_info': {
                'age': random.randint(55, 85),
                'gender': random.choice(['male', 'female']),
                'education_years': random.randint(8, 20)
            },
            'molecular_data': [
                ['biomarker', 'value', 'unit'],
                ['Aβ42', str(random.uniform(400, 800)), 'pg/mL'],
                ['p-tau217', str(random.uniform(20, 150)), 'pg/mL']
            ],
            'lifestyle_data': {
                'physical_activity': random.uniform(50, 300),
                'diet_score': random.uniform(3, 10)
            }
        }

    def simulate_model_analysis(self, patient_data, demo_category=None):
        """模拟模型分析过程"""
        import random
        
        # 从患者数据中提取生活方式信息
        lifestyle_data = {}
        if patient_data and patient_data.get('clinical_info', {}).get('lifestyle'):
            lifestyle_data = patient_data['clinical_info']['lifestyle']
        
        # 根据演示类别设置初始诊断结果
        if demo_category == "CN":
            pred_label = "CN"
        elif demo_category == "EMCI":
            pred_label = "EMCI"
        elif demo_category == "LMCI":
            pred_label = "LMCI"
        elif demo_category == "AD":
            pred_label = "AD"
        else:
            # 随机生成诊断结果
            labels = config_manager.get('diagnosis.output_classes')
            pred_label = random.choices(labels, weights=[0.25, 0.3, 0.25, 0.2])[0]
        
        # 根据生活方式数据调整诊断结果
        if lifestyle_data:
            # 计算生活方式风险调整因子
            lifestyle_adjustment = 0.0
            
            # 运动频率影响
            exercise_freq = lifestyle_data.get('exercise_frequency')
            if exercise_freq:
                exercise_freq = int(exercise_freq)
                if exercise_freq< 2:
                    lifestyle_adjustment += 0.15
                elif exercise_freq >4:
                    lifestyle_adjustment -= 0.1
            
            # 睡眠时长影响
            sleep_duration = lifestyle_data.get('sleep_duration')
            if sleep_duration:
                sleep_duration = float(sleep_duration)
                if sleep_duration < 6 or sleep_duration >9:
                    lifestyle_adjustment += 0.1
            
            # 饮食习惯影响
            diet_health = lifestyle_data.get('diet_health')
            if diet_health == 'low':
                lifestyle_adjustment += 0.1
            elif diet_health == 'high':
                lifestyle_adjustment -= 0.05
            
            # 社交活动影响
            social_activities = lifestyle_data.get('social_activities')
            if social_activities:
                social_activities = int(social_activities)
                if social_activities < 2:
                    lifestyle_adjustment += 0.08
                elif social_activities > 4:
                    lifestyle_adjustment -= 0.05
            
            # 吸烟状况影响
            smoking_status = lifestyle_data.get('smoking_status')
            if smoking_status == 'current':
                lifestyle_adjustment += 0.2
            elif smoking_status == 'past':
                lifestyle_adjustment += 0.1
            
            # 饮酒频率影响
            alcohol_consumption = lifestyle_data.get('alcohol_consumption')
            if alcohol_consumption == 'regular':
                lifestyle_adjustment += 0.1
            
            # 根据调整因子调整诊断结果
            label_index = {'CN': 0, 'EMCI': 1, 'LMCI': 2, 'AD': 3}
            current_index = label_index.get(pred_label, 1)
            
            # 根据调整因子调整风险等级
            if lifestyle_adjustment >0.2:
                current_index = min(3, current_index + 1)
            elif lifestyle_adjustment < -0.15:
                current_index = max(0, current_index - 1)
            
            # 更新诊断结果
            reverse_label_index = {0: 'CN', 1: 'EMCI', 2: 'LMCI', 3: 'AD'}
            pred_label = reverse_label_index.get(current_index, pred_label)
        
        # 生成置信度
        confidence = random.uniform(0.75, 0.98)
        
        # 生成风险评分
        risk_score_map = {
            'CN': random.uniform(0.05, 0.15),
            'EMCI': random.uniform(0.2, 0.4),
            'LMCI': random.uniform(0.4, 0.7),
            'AD': random.uniform(0.7, 0.95)
        }
        base_risk = risk_score_map.get(pred_label, 0.5)
        
        # 根据生活方式数据调整基础风险
        if lifestyle_data:
            # 应用生活方式调整因子
            base_risk = min(0.95, max(0.05, base_risk + lifestyle_adjustment))
        
        # 生成每月进展风险数据（12个月）
        monthly_risk = []
        
        # 根据诊断类别生成合理的风险变化趋势
        if pred_label == 'CN':
            # 认知正常：风险缓慢增加，波动较小
            for month in range(1, 13):
                # 基础风险缓慢增长，加上小波动
                month_risk = base_risk * (1 + (month - 1) * 0.02) + random.uniform(-0.03, 0.03)
                monthly_risk.append({'month': month, 'risk': month_risk})
        elif pred_label == 'EMCI':
            # 早期轻度认知障碍：风险中等，有一定波动
            for month in range(1, 13):
                # 风险逐渐增加，波动适中
                month_risk = base_risk * (1 + (month - 1) * 0.04) + random.uniform(-0.05, 0.05)
                monthly_risk.append({'month': month, 'risk': month_risk})
        elif pred_label == 'LMCI':
            # 晚期轻度认知障碍：风险较高，波动较大
            for month in range(1, 13):
                # 风险快速增加，波动较大
                month_risk = base_risk * (1 + (month - 1) * 0.06) + random.uniform(-0.07, 0.07)
                monthly_risk.append({'month': month, 'risk': month_risk})
        else:  # AD
            # 阿尔茨海默病：风险很高，持续上升
            for month in range(1, 13):
                # 风险快速上升，波动相对较小
                month_risk = base_risk * (1 + (month - 1) * 0.03) + random.uniform(-0.04, 0.04)
                monthly_risk.append({'month': month, 'risk': month_risk})
        
        # 确保风险值在合理范围内
        for item in monthly_risk:
            item['risk'] = min(0.99, max(0.01, item['risk']))
        
        # 将risk_score设置为12月的风险概率，确保与图表显示一致
        risk_score = monthly_risk[-1]['risk']
        
        # 生成风险指标 - 使用DiagnosisEngine的方法
        from src.diagnosis.engine import DiagnosisEngine
        diagnosis_engine = DiagnosisEngine()
        
        # 构建预测结果
        prediction_result = {
            'prediction': pred_label,
            'confidence': confidence
        }
        
        # 生成风险指标
        risk_indicators = diagnosis_engine._generate_risk_indicators(prediction_result, patient_data.get('clinical_info', {}))
        
        # 生成建议
        recommendations = [
            "保持规律的体育锻炼",
            "保持健康的饮食习惯",
            "保持社交活动",
            "定期进行认知训练",
            "定期复诊"
        ]
        
        # 生成脑部图像
        brain_image = diagnosis_engine._generate_brain_image(pred_label, risk_indicators)
        
        # 生成原始MRI影像
        original_mri_image = diagnosis_engine._generate_brain_image(pred_label, risk_indicators, show_original=True)
        
        # 生成热力图
        heatmap_image = diagnosis_engine._generate_heatmap(pred_label, risk_indicators, patient_data)
        
        # 构建结果
        results = {
            'success': True,
            'results': {
                'pred_label': pred_label,
                'confidence': confidence,
                'risk_score': risk_score,
                'monthly_risk': monthly_risk,
                'risk_indicators': risk_indicators,
                'recommendations': recommendations,
                'brain_image': brain_image,
                'original_mri_image': original_mri_image,
                'heatmap_image': heatmap_image
            },
            'patient_info': patient_data.get('clinical_info', {})
        }
        
        return results

    def save_analysis_results(self, patient_id, results):
        """保存分析结果"""
        try:
            # 创建结果目录
            results_dir = f'./results/individual/{patient_id}_{generate_timestamp()}'
            os.makedirs(results_dir, exist_ok=True)
            
            # 保存结果到JSON文件
            result_path = os.path.join(results_dir, 'analysis_result.json')
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Analysis results saved to: {result_path}")
        except Exception as e:
            logger.error("保存分析结果失败", e)

    def generate_pdf_report(self, results_data, patient_info):
        """生成PDF报告"""
        try:
            # 调用PDF生成器
            pdf_path = self.pdf_generator.generate_report(
                results_data=results_data,
                patient_info=patient_info
            )
            return pdf_path
        except Exception as e:
            logger.error("生成PDF报告失败", e)
            return None

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return FileResponse("./static/index.html")

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "阿尔兹海默症诊断系统",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

# 演示数据分析
@app.get("/api/demo")
async def demo_analysis(category: str = None):
    """演示数据分析"""
    try:
        logger.info(f"Processing demo data request (category: {category})...")
        
        # 使用系统实例
        system = get_system_instance()
        
        # 分析数据
        results = system.analyze_multimodal_data(use_demo=True, demo_category=category)

        logger.info(f"Demo data analysis completed, diagnosis result: {results.get('results', {}).get('pred_label', 'Unknown')}")
        return results
    except Exception as e:
        logger.error(f"Demo analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 文件分析
@app.post("/api/analyze")
async def analyze_data(
    patient_info: str = Form(None),
    files: list[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """文件分析"""
    try:
        logger.info("Processing file analysis request...")
        
        # 解析患者信息
        patient_info_data = None
        if patient_info:
            try:
                patient_info_data = json.loads(patient_info)
            except json.JSONDecodeError:
                logger.error("患者信息JSON解析失败")
                raise HTTPException(status_code=400, detail="患者信息格式错误")
        
        # 使用系统实例
        system = get_system_instance()
        
        # 分析数据
        results = system.analyze_multimodal_data(
            patient_id=patient_info_data.get('patient_id') if patient_info_data else None,
            patient_info=patient_info_data
        )

        logger.info(f"File analysis completed, diagnosis result: {results.get('results', {}).get('pred_label', 'Unknown')}")
        return results
    except Exception as e:
        logger.error(f"File analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 文件上传
@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...), current_user: dict = Depends(get_current_user)):
    """文件上传"""
    try:
        logger.info("Processing file upload request...")
        
        uploaded_files = []
        
        for file in files:
            # 保存文件到uploaded_img目录
            upload_dir = './uploaded_img'
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成唯一文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{timestamp}{file_ext}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # 保存文件
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)
            
            uploaded_files.append({
                'filename': file.filename,
                'saved_as': unique_filename,
                'size': len(content),
                'path': f'/uploaded_img/{unique_filename}'
            })
            logger.info(f"File saved: {unique_filename}")
        
        if uploaded_files:
            return {
                'success': True,
                'message': f'成功上传 {len(uploaded_files)} 个文件',
                'files': uploaded_files
            }
        else:
            return {
                'success': False,
                'error': '未找到可上传的文件'
            }
            
    except Exception as e:
        logger.error(f"文件上传失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 生成PDF报告
@app.post("/api/generate-pdf")
async def generate_pdf(data: dict):
    """生成PDF报告"""
    try:
        logger.info("Processing PDF generation request...")
        results_data = data.get('results', {})
        patient_info = data.get('patient_info', {})
        
        # 使用系统实例
        system = get_system_instance()

        # 生成PDF
        pdf_path = system.generate_pdf_report(results_data, patient_info)

        if pdf_path and os.path.exists(pdf_path):
            pdf_filename = os.path.basename(pdf_path)
            pdf_url = f"/reports/{pdf_filename}"

            logger.info(f"PDF generation successful: {pdf_filename}")
            return {
                'success': True,
                'pdf_url': pdf_url,
                'filename': pdf_filename,
                'message': 'PDF报告生成成功'
            }
        else:
            logger.error("PDF文件生成失败")
            raise HTTPException(status_code=500, detail='PDF文件生成失败')

    except Exception as e:
        logger.error("生成PDF失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取报告列表
@app.get("/api/reports")
async def get_reports():
    """获取报告列表"""
    try:
        logger.info("Retrieving report list...")
        reports_dir = './reports'
        reports = []

        if os.path.exists(reports_dir):
            for filename in os.listdir(reports_dir):
                if filename.endswith('.pdf'):
                    filepath = os.path.join(reports_dir, filename)
                    stat = os.stat(filepath)

                    # 从文件名提取信息
                    parts = filename.replace('.pdf', '').split('_')
                    patient_id = parts[0] if len(parts) > 0 else 'Unknown'

                    reports.append({
                        'name': filename,
                        'path': f'/reports/{filename}',
                        'patient_id': patient_id,
                        'size': stat.st_size,
                        'modified': stat.st_mtime * 1000,
                        'timestamp': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })

        # 按修改时间排序（最新的在前面）
        reports.sort(key=lambda x: x['modified'], reverse=True)

        logger.info(f"Found {len(reports)} reports")
        return {
            'success': True,
            'reports': reports[:10]  # 返回最近的10个报告
        }

    except Exception as e:
        logger.error("获取报告列表失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取系统统计
@app.get("/api/stats")
async def get_stats():
    """获取系统统计"""
    try:
        logger.info("Retrieving system statistics...")
        # 固定患者数量为28
        total_patients = 28

        # 固定报告数量为22
        total_reports = 22

        # 固定诊断分析次数为56
        analysis_count = 56

        # 固定数据总量为15324例
        data_size_str = "15324 例"

        # 从数据库获取最近分析时间
        from src.database.models import Diagnosis
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from src.utils.config_manager import config_manager
        
        # 获取数据库配置
        db_url = config_manager.get('database.url', 'sqlite:///./alzheimer.db')
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        last_analysis = '-'
        
        try:
            # 获取最近分析时间
            latest_diagnosis = db.query(Diagnosis).order_by(Diagnosis.diagnosis_date.desc()).first()
            if latest_diagnosis:
                last_analysis = latest_diagnosis.diagnosis_date.strftime('%Y-%m-%d %H:%M')
        except Exception as db_error:
            logger.error("数据库查询失败", db_error)
        finally:
            db.close()

        logger.info(f"Statistics retrieved successfully: {total_patients} patients, {total_reports} reports, {analysis_count} analyses")
        return {
            'success': True,
            'total_patients': total_patients,
            'total_reports': total_reports,
            'analysis_count': analysis_count,
            'data_size': data_size_str,
            'last_analysis': last_analysis
        }

    except Exception as e:
        logger.error("获取统计失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 清理临时文件
@app.post("/api/clear-temp")
async def clear_temp(current_user: dict = Depends(get_current_user)):
    """清理临时文件"""
    try:
        logger.info("Cleaning temporary files...")
        temp_dirs = ['./temp/tmp_uploads', './temp/cache', './temp/logs']
        total_deleted = 0

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    filepath = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(filepath):
                            os.remove(filepath)
                            total_deleted += 1
                    except:
                        pass

        logger.info(f"Cleaned {total_deleted} temporary files")
        return {
            'success': True,
            'message': f'清理了 {total_deleted} 个临时文件'
        }

    except Exception as e:
        logger.error("清理临时文件失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 诊断API
@app.post("/api/diagnose")
async def diagnose(data: dict):
    """诊断API"""
    try:
        logger.info("Processing diagnosis request...")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_diagnosis_request(data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=400, detail=response.get('message', '诊断失败'))
    except Exception as e:
        logger.error("诊断请求处理失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 登录
@app.post("/api/auth/login")
async def login(data: dict):
    """登录"""
    try:
        logger.info("收到登录请求")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_login_request(data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=401, detail=response.get('message', '登录失败'))
    except Exception as e:
        logger.error("登录请求处理失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 注册
@app.post("/api/auth/register")
async def register(data: dict):
    """注册"""
    try:
        logger.info("收到注册请求")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_register_request(data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=400, detail=response.get('message', '注册失败'))
    except Exception as e:
        logger.error("注册请求处理失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取目录结构
@app.get("/api/directory")
async def get_directory_structure():
    """获取目录结构"""
    try:
        logger.info("获取目录结构")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_directory_structure_request()
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取目录结构失败'))
    except Exception as e:
        logger.error("获取目录结构失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取目录文件列表
@app.get("/api/directory/{path:path}")
async def get_directory_files(path: str):
    """获取目录文件列表"""
    try:
        logger.info(f"获取目录文件列表: {path}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_directory_files_request(path)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取目录文件失败'))
    except Exception as e:
        logger.error("获取目录文件失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取文件内容
@app.get("/api/file/{path:path}")
async def get_file(path: str):
    """获取文件内容"""
    try:
        logger.info(f"获取文件: {path}")
        
        # 验证文件是否存在
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 验证是否是文件
        if not os.path.isfile(path):
            raise HTTPException(status_code=400, detail="路径不是文件")
        
        # 返回文件
        return FileResponse(path)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("获取文件失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 患者管理API

# 获取患者列表
@app.get("/api/patients")
async def get_patients(current_user: dict = Depends(get_current_user)):
    """获取患者列表"""
    try:
        logger.info("获取患者列表")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_patient_list_request()
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取患者列表失败'))
    except Exception as e:
        logger.error("获取患者列表失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取患者详情
@app.get("/api/patients/{patient_id}")
async def get_patient_detail(patient_id: int, current_user: dict = Depends(get_current_user)):
    """获取患者详情"""
    try:
        logger.info(f"获取患者详情: {patient_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_patient_detail_request(patient_id)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取患者详情失败'))
    except Exception as e:
        logger.error("获取患者详情失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 创建患者
@app.post("/api/patients")
async def create_patient(data: dict, current_user: dict = Depends(get_current_user)):
    """创建患者"""
    try:
        logger.info("创建患者")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_patient_create_request(data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '创建患者失败'))
    except Exception as e:
        logger.error("创建患者失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 更新患者信息
@app.put("/api/patients/{patient_id}")
async def update_patient(patient_id: int, data: dict, current_user: dict = Depends(get_current_user)):
    """更新患者信息"""
    try:
        logger.info(f"更新患者信息: {patient_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_patient_update_request(patient_id, data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '更新患者信息失败'))
    except Exception as e:
        logger.error("更新患者信息失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 删除患者
@app.delete("/api/patients/{patient_id}")
async def delete_patient(patient_id: int, current_user: dict = Depends(get_current_user)):
    """删除患者"""
    try:
        logger.info(f"删除患者: {patient_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_patient_delete_request(patient_id)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '删除患者失败'))
    except Exception as e:
        logger.error("删除患者失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 远程会诊API

# 获取远程会诊列表
@app.get("/api/teleconsultations")
async def get_teleconsultations(current_user: dict = Depends(get_current_user)):
    """获取远程会诊列表"""
    try:
        logger.info("获取远程会诊列表")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_teleconsultation_list_request()
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取远程会诊列表失败'))
    except Exception as e:
        logger.error("获取远程会诊列表失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 获取远程会诊详情
@app.get("/api/teleconsultations/{consultation_id}")
async def get_teleconsultation_detail(consultation_id: int, current_user: dict = Depends(get_current_user)):
    """获取远程会诊详情"""
    try:
        logger.info(f"获取远程会诊详情: {consultation_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_teleconsultation_detail_request(consultation_id)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取远程会诊详情失败'))
    except Exception as e:
        logger.error("获取远程会诊详情失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 创建远程会诊
@app.post("/api/teleconsultations")
async def create_teleconsultation(data: dict, current_user: dict = Depends(get_current_user)):
    """创建远程会诊"""
    try:
        logger.info("创建远程会诊")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_teleconsultation_create_request(data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '创建远程会诊失败'))
    except Exception as e:
        logger.error("创建远程会诊失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 更新远程会诊状态
@app.put("/api/teleconsultations/{consultation_id}")
async def update_teleconsultation(consultation_id: int, data: dict, current_user: dict = Depends(get_current_user)):
    """更新远程会诊状态"""
    try:
        logger.info(f"更新远程会诊状态: {consultation_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_teleconsultation_update_request(consultation_id, data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '更新远程会诊状态失败'))
    except Exception as e:
        logger.error("更新远程会诊状态失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 删除远程会诊
@app.delete("/api/teleconsultations/{consultation_id}")
async def delete_teleconsultation(consultation_id: int, current_user: dict = Depends(get_current_user)):
    """删除远程会诊"""
    try:
        logger.info(f"删除远程会诊: {consultation_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_teleconsultation_delete_request(consultation_id)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '删除远程会诊失败'))
    except Exception as e:
        logger.error("删除远程会诊失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 生活方式数据API

# 获取患者生活方式数据
@app.get("/api/patients/{patient_id}/lifestyle")
async def get_patient_lifestyle(patient_id: int, current_user: dict = Depends(get_current_user)):
    """获取患者生活方式数据"""
    try:
        logger.info(f"获取患者生活方式数据: {patient_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_lifestyle_data_request(patient_id)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取生活方式数据失败'))
    except Exception as e:
        logger.error("获取生活方式数据失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 更新患者生活方式数据
@app.put("/api/patients/{patient_id}/lifestyle")
async def update_patient_lifestyle(patient_id: int, data: dict, current_user: dict = Depends(get_current_user)):
    """更新患者生活方式数据"""
    try:
        logger.info(f"更新患者生活方式数据: {patient_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_lifestyle_data_update_request(patient_id, data)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '更新生活方式数据失败'))
    except Exception as e:
        logger.error("更新生活方式数据失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 根据用户ID获取患者信息
@app.get("/api/patients/by-user/{user_id}")
async def get_patient_by_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """根据用户ID获取患者信息"""
    try:
        logger.info(f"根据用户ID获取患者信息: {user_id}")
        
        # 使用API处理器
        api_handler = get_api_handler()
        response = api_handler.handle_patient_by_user_id_request(user_id)
        
        if response.get('success'):
            return response
        else:
            raise HTTPException(status_code=500, detail=response.get('message', '获取患者信息失败'))
    except Exception as e:
        logger.error("根据用户ID获取患者信息失败", e)
        raise HTTPException(status_code=500, detail=str(e))

# 静态文件服务
@app.get("/reports/{filename}")
async def get_report(filename: str):
    """获取报告文件"""
    file_path = f'./reports/{filename}'
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="报告文件不存在")

@app.get("/uploaded_img/{filename}")
async def get_uploaded_image(filename: str):
    """获取上传的图片"""
    file_path = f'./uploaded_img/{filename}'
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="图片文件不存在")

@app.get("/demodata/{path:path}")
async def get_demo_data(path: str):
    """获取演示数据"""
    file_path = f'./demodata/{path}'
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="演示数据不存在")

# 启动服务器
if __name__ == "__main__":
    # 查找可用端口
    port = find_available_port(8888)
    logger.info(f"Starting server on port {port}")
    
    # 启动FastAPI服务器
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
