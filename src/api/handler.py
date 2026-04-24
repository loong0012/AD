"""
API处理器 - 处理HTTP请求和响应
"""

import json
import traceback
from src.utils.log_manager import log_manager as logger
from src.utils.config_manager import config_manager
from src.diagnosis.engine import DiagnosisEngine
from src.data.processor import DataProcessor
from src.report.generator import ReportGenerator
from src.database.database import SessionLocal
from src.database.models import User, Patient, Doctor, Teleconsultation, LifestyleData, MolecularData, ClinicalRecord, Diagnosis
from src.utils.jwt_utils import verify_password, get_password_hash, create_access_token


class APIHandler:
    """API处理器类 - 处理HTTP请求"""
    
    def __init__(self):
        self.diagnosis_engine = DiagnosisEngine()
        self.data_processor = DataProcessor()
        self.report_generator = ReportGenerator()
        
        # 使用数据库存储用户信息
        self.db = SessionLocal()
        
        logger.info("API处理器初始化完成")
    
    def handle_diagnosis_request(self, request_data):
        """
        处理诊断请求
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info("收到诊断请求")
            
            # 检查是否是测试数据格式
            if 'patient_id' in request_data and 'age' in request_data:
                # 处理测试数据格式
                patient_data = request_data
                
                # 生成随机特征数据
                import numpy as np
                features = np.random.normal(0.5, 0.2, 64).tolist()
                
                # 预处理特征
                processed_features = self.data_processor.preprocess_features([features])[0]
                
                # 执行诊断
                prediction_result = self.diagnosis_engine.predict(processed_features)
                
                # 生成诊断报告
                diagnosis_report = self.diagnosis_engine.generate_diagnosis_report(patient_data, prediction_result)
                
                # 生成脑部图像
                brain_image = self.diagnosis_engine._generate_brain_image(diagnosis_report['diagnosis'], diagnosis_report['risk_indicators'])
                
                # 生成热力图
                heatmap_image = self.diagnosis_engine._generate_heatmap(diagnosis_report['diagnosis'], diagnosis_report['risk_indicators'])
                
                # 保存诊断记录到数据库
                from src.database.models import Diagnosis, Patient
                try:
                    # 尝试查找患者
                    patient = self.db.query(Patient).filter(Patient.id == request_data.get('patient_id')).first()
                    if patient:
                        # 创建诊断记录
                        new_diagnosis = Diagnosis(
                            patient_id=patient.id,
                            pred_label=diagnosis_report['diagnosis'],
                            confidence=diagnosis_report['confidence'],
                            risk_score=diagnosis_report['risk_score'],
                            recommendations=str(diagnosis_report['recommendations'])
                        )
                        self.db.add(new_diagnosis)
                        self.db.commit()
                        logger.info(f"诊断记录保存成功: 患者ID {patient.id}, 诊断结果 {diagnosis_report['diagnosis']}")
                except Exception as db_error:
                    logger.error("保存诊断记录失败", db_error)
                    self.db.rollback()
                
                # 构建响应
                response = {
                    'success': True,
                    'diagnosis': diagnosis_report['diagnosis'],
                    'confidence': diagnosis_report['confidence'],
                    'risk_score': diagnosis_report['risk_score'],
                    'risk_indicators': diagnosis_report['risk_indicators'],
                    'recommendations': diagnosis_report['recommendations'],
                    'brain_image': brain_image,
                    'heatmap_image': heatmap_image,
                    'message': '诊断完成'
                }
            else:
                # 验证请求数据
                validation_result = self._validate_request_data(request_data)
                if not validation_result['is_valid']:
                    return self._create_error_response(400, validation_result['errors'])
                
                # 提取特征数据
                features = request_data.get('features')
                
                # 提取患者信息，确保包含生活方式数据
                patient_data = request_data.get('patient_info', {})
                
                # 如果提供了patient_id，从数据库获取完整的患者信息
                patient_id = patient_data.get('patient_id')
                if patient_id:
                    # 获取患者基本信息
                    patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
                    if patient:
                        # 更新患者基本信息
                        patient_data['name'] = patient.name
                        patient_data['age'] = patient.age
                        patient_data['gender'] = patient.gender
                        patient_data['education_years'] = patient.education_years
                        patient_data['contact_info'] = patient.contact_info
                        patient_data['medical_history'] = patient.medical_history
                        
                        # 获取生活方式数据
                        lifestyle_data = self.db.query(LifestyleData).filter(LifestyleData.patient_id == patient_id).first()
                        if lifestyle_data:
                            patient_data['lifestyle_data'] = {
                                'exercise_frequency': lifestyle_data.exercise_frequency,
                                'sleep_duration': lifestyle_data.sleep_duration,
                                'diet_health': lifestyle_data.diet_health,
                                'social_activities': lifestyle_data.social_activities,
                                'smoking_status': lifestyle_data.smoking_status,
                                'alcohol_consumption': lifestyle_data.alcohol_consumption
                            }
                
                # 预处理特征
                processed_features = self.data_processor.preprocess_features([features])[0]
                
                # 执行诊断
                prediction_result = self.diagnosis_engine.predict(processed_features)
                
                # 生成诊断报告
                diagnosis_report = self.diagnosis_engine.generate_diagnosis_report(patient_data, prediction_result)
                
                # 生成可视化报告
                chart_paths = self.report_generator.generate_visualization(prediction_result)
                
                # 生成综合报告
                summary_report = self.report_generator.generate_summary_report(diagnosis_report, chart_paths)
                
                # 保存JSON报告
                json_report_path = self.report_generator.generate_json_report(diagnosis_report)
                
                # 保存诊断记录到数据库
                from src.database.models import Diagnosis, Patient
                try:
                    # 尝试查找患者（如果提供了patient_id）
                    if patient_id:
                        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
                        if patient:
                            # 创建诊断记录
                            new_diagnosis = Diagnosis(
                                patient_id=patient.id,
                                pred_label=diagnosis_report['diagnosis'],
                                confidence=diagnosis_report['confidence'],
                                risk_score=diagnosis_report['risk_score'],
                                recommendations=str(diagnosis_report['recommendations']),
                                report_path=json_report_path
                            )
                            self.db.add(new_diagnosis)
                            self.db.commit()
                            logger.info(f"诊断记录保存成功: 患者ID {patient.id}, 诊断结果 {diagnosis_report['diagnosis']}")
                except Exception as db_error:
                    logger.error("保存诊断记录失败", db_error)
                    self.db.rollback()
                
                # 构建响应，确保包含完整的患者信息
                response = {
                    'success': True,
                    'data': {
                        'diagnosis': diagnosis_report['diagnosis'],
                        'confidence': diagnosis_report['confidence'],
                        'risk_score': diagnosis_report['risk_score'],
                        'probabilities': diagnosis_report['probabilities'],
                        'recommendations': diagnosis_report['recommendations'],
                        'monthly_risk': diagnosis_report['monthly_risk'],
                        'risk_indicators': diagnosis_report['risk_indicators'],
                        'charts': chart_paths,
                        'report_file': json_report_path
                    },
                    'patient_info': patient_data,
                    'message': '诊断完成'
                }
            
            logger.info("诊断请求处理完成")
            return response
            
        except Exception as e:
            logger.error("诊断请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_demo_request(self, request_data):
        """
        处理演示请求
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info("收到演示请求")
            
            # 获取演示类别
            category = request_data.get('category', 'default')
            
            # 生成演示数据
            demo_features = self._generate_demo_features(category)
            
            # 执行诊断
            prediction_result = self.diagnosis_engine.predict(demo_features)
            
            # 生成演示报告
            patient_data = {
                'name': '演示患者',
                'age': 75,
                'gender': '男',
                'category': category
            }
            
            diagnosis_report = self.diagnosis_engine.generate_diagnosis_report(patient_data, prediction_result)
            
            # 构建响应
            response = {
                'success': True,
                'data': {
                    'diagnosis': diagnosis_report['diagnosis'],
                    'confidence': diagnosis_report['confidence'],
                    'risk_score': diagnosis_report['risk_score'],
                    'probabilities': diagnosis_report['probabilities'],
                    'recommendations': diagnosis_report['recommendations'],
                    'monthly_risk': diagnosis_report['monthly_risk'],
                    'risk_indicators': diagnosis_report['risk_indicators']
                },
                'message': '演示诊断完成'
            }
            
            logger.info("演示请求处理完成")
            return response
            
        except Exception as e:
            logger.error("演示请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_stats_request(self):
        """
        处理统计数据请求
        :return: 响应数据
        """
        try:
            logger.info("收到统计数据请求")
            
            # 从数据库查询实际统计数据
            from src.database.models import Diagnosis
            
            # 查询所有诊断记录
            all_diagnoses = self.db.query(Diagnosis).all()
            total_diagnoses = len(all_diagnoses)
            
            # 计算平均置信度
            if total_diagnoses > 0:
                total_confidence = sum(diagnosis.confidence for diagnosis in all_diagnoses)
                average_confidence = total_confidence / total_diagnoses
            else:
                average_confidence = 0.0
            
            # 统计诊断分布
            distribution = {
                '正常': 0,
                '轻度认知障碍': 0,
                '阿尔茨海默病': 0,
                '其他': 0
            }
            
            # 映射诊断标签到中文
            diagnosis_map = {
                'CN': '正常',
                'EMCI': '轻度认知障碍',
                'LMCI': '轻度认知障碍',
                'AD': '阿尔茨海默病'
            }
            
            for diagnosis in all_diagnoses:
                label = diagnosis.pred_label
                if label in diagnosis_map:
                    distribution[diagnosis_map[label]] += 1
                else:
                    distribution['其他'] += 1
            
            # 生成统计数据
            stats = {
                'total_diagnoses': total_diagnoses,
                'average_confidence': round(average_confidence, 2),
                'distribution': distribution,
                'system_status': '运行正常',
                'model_version': config_manager.get('model.version', '1.0')
            }
            
            response = {
                'success': True,
                'data': stats,
                'message': '统计数据获取成功'
            }
            
            logger.info("统计数据请求处理完成")
            return response
            
        except Exception as e:
            logger.error("统计数据请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def _validate_request_data(self, request_data):
        """验证请求数据"""
        errors = []
        
        if not isinstance(request_data, dict):
            errors.append("请求数据格式不正确")
        
        if 'features' not in request_data:
            errors.append("缺少特征数据")
        elif not isinstance(request_data['features'], list):
            errors.append("特征数据格式不正确")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _generate_demo_features(self, category):
        """生成演示特征数据"""
        import numpy as np
        
        # 根据不同类别生成不同的演示数据
        if category == 'normal':
            # 正常人群特征
            return np.random.normal(0.2, 0.1, 64).tolist()
        elif category == 'mci':
            # 轻度认知障碍特征
            return np.random.normal(0.5, 0.15, 64).tolist()
        elif category == 'ad':
            # 阿尔茨海默病特征
            return np.random.normal(0.8, 0.1, 64).tolist()
        else:
            # 默认特征
            return np.random.normal(0.4, 0.2, 64).tolist()
    
    def _create_error_response(self, status_code, errors):
        """创建错误响应"""
        return {
            'success': False,
            'error': {
                'code': status_code,
                'message': '请求处理失败',
                'details': errors
            },
            'message': errors[0] if errors else '未知错误'
        }
    
    def handle_login_request(self, request_data):
        """
        处理登录请求
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info("收到登录请求")
            
            # 获取登录数据
            username = request_data.get('username')
            password = request_data.get('password')
            role = request_data.get('role')
            
            # 验证请求数据
            if not username or not password or not role:
                return self._create_error_response(400, ['用户名、密码和角色不能为空'])
            
            # 从数据库查询用户
            user = self.db.query(User).filter(User.username == username, User.role == role).first()
            
            if user and verify_password(password, user.password_hash):
                    # 生成JWT token
                    access_token = create_access_token(
                        data={"sub": username, "role": role, "user_id": user.id}
                    )
                    
                    # 构建基本响应数据
                    response_data = {
                        'success': True,
                        'data': {
                            'username': username,
                            'role': role,
                            'display_name': self._get_role_display_name(role),
                            'user_id': user.id
                        },
                        'token': access_token,
                        'message': '登录成功'
                    }
                    
                    # 如果是患者角色，获取患者详细信息和生活方式数据
                    if role == 'patient':
                        patient = self.db.query(Patient).filter(Patient.user_id == user.id).first()
                        if patient:
                            # 添加患者基本信息
                            response_data['data']['patient_info'] = {
                                'id': patient.id,
                                'name': patient.name,
                                'age': patient.age,
                                'gender': patient.gender,
                                'education_years': patient.education_years,
                                'contact_info': patient.contact_info,
                                'medical_history': patient.medical_history
                            }
                            
                            # 获取生活方式数据
                            lifestyle_data = self.db.query(LifestyleData).filter(LifestyleData.patient_id == patient.id).first()
                            if lifestyle_data:
                                response_data['data']['lifestyle_data'] = {
                                    'id': lifestyle_data.id,
                                    'exercise_frequency': lifestyle_data.exercise_frequency,
                                    'sleep_duration': lifestyle_data.sleep_duration,
                                    'diet_health': lifestyle_data.diet_health,
                                    'social_activities': lifestyle_data.social_activities,
                                    'smoking_status': lifestyle_data.smoking_status,
                                    'alcohol_consumption': lifestyle_data.alcohol_consumption
                                }
                    
                    return response_data
            
            return self._create_error_response(401, ['用户名、密码或角色不正确'])
            
        except Exception as e:
            logger.error("登录请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_register_request(self, request_data):
        """
        处理注册请求
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info("收到注册请求")
            
            # 获取注册数据
            username = request_data.get('username')
            email = request_data.get('email')
            password = request_data.get('password')
            role = request_data.get('role')
            
            # 验证请求数据
            if not username or not email or not password or not role:
                return self._create_error_response(400, ['所有字段都不能为空'])
            
            # 验证密码长度
            if len(password)< 6:
                return self._create_error_response(400, ['密码长度至少为6位'])
            
            # 验证角色
            valid_roles = ['patient', 'doctor', 'admin']
            if role not in valid_roles:
                return self._create_error_response(400, ['无效的角色类型'])
            
            # 检查用户名是否已存在
            existing_user = self.db.query(User).filter(User.username == username).first()
            if existing_user:
                return self._create_error_response(400, ['用户名已存在'])
            
            # 检查邮箱是否已存在
            existing_email = self.db.query(User).filter(User.email == email).first()
            if existing_email:
                return self._create_error_response(400, ['邮箱已被注册'])
            
            # 创建新用户
            new_user = User(
                username=username,
                password_hash=get_password_hash(password),
                email=email,
                role=role
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            logger.info(f"新用户注册成功: {username} ({role})")
            
            return {
                'success': True,
                'data': {
                    'username': username,
                    'email': email,
                    'role': role
                },
                'message': '注册成功'
            }
            
        except Exception as e:
            logger.error("注册请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def _get_role_display_name(self, role):
        """获取角色显示名称"""
        role_map = {
            'patient': '患者',
            'doctor': '医生',
            'admin': '管理员'
        }
        return role_map.get(role, role)
    
    def handle_directory_structure_request(self):
        """
        获取项目数据目录结构
        :return: 目录结构数据
        """
        try:
            import os
            
            # 定义数据目录路径 - 与项目实际目录结构完全匹配
            data_directories = {
                'checkpoints': {
                    'path': 'checkpoints',
                    'description': '模型检查点',
                    'type': 'folder'
                },
                'config': {
                    'path': 'config',
                    'description': '配置文件',
                    'type': 'folder'
                },
                'data': {
                    'path': 'data',
                    'description': '数据根目录',
                    'type': 'folder',
                    'subdirectories': {
                        'demo': {
                            'path': 'data/demo',
                            'description': '演示数据',
                            'type': 'folder'
                        },
                        'real': {
                            'path': 'data/real',
                            'description': '真实数据',
                            'type': 'folder',
                            'subdirectories': {
                                'adni': {
                                    'path': 'data/real/adni',
                                    'description': 'ADNI数据集',
                                    'type': 'folder',
                                    'subdirectories': {
                                        'clinical': {
                                            'path': 'data/real/adni/clinical',
                                            'description': '临床数据',
                                            'type': 'folder'
                                        }
                                    }
                                },
                                'adrc': {
                                    'path': 'data/real/adrc',
                                    'description': 'ADRC数据集',
                                    'type': 'folder',
                                    'subdirectories': {
                                        'clinical': {
                                            'path': 'data/real/adrc/clinical',
                                            'description': '临床数据',
                                            'type': 'folder'
                                        }
                                    }
                                },
                                'miriad': {
                                    'path': 'data/real/miriad',
                                    'description': 'MIRIAD数据集',
                                    'type': 'folder',
                                    'subdirectories': {
                                        'mri': {
                                            'path': 'data/real/miriad/mri',
                                            'description': 'MRI数据',
                                            'type': 'folder'
                                        }
                                    }
                                },
                                'nacc': {
                                    'path': 'data/real/nacc',
                                    'description': 'NACC数据集',
                                    'type': 'folder',
                                    'subdirectories': {
                                        'clinical': {
                                            'path': 'data/real/nacc/clinical',
                                            'description': '临床数据',
                                            'type': 'folder'
                                        }
                                    }
                                },
                                'ucsd': {
                                    'path': 'data/real/ucsd',
                                    'description': 'UCSD数据集',
                                    'type': 'folder',
                                    'subdirectories': {
                                        'mri': {
                                            'path': 'data/real/ucsd/mri',
                                            'description': 'MRI数据',
                                            'type': 'folder'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            # 检查目录是否存在并统计文件数量
            def check_directory_recursive(dir_info):
                if os.path.exists(dir_info['path']):
                    dir_info['exists'] = True
                    # 统计文件数量
                    file_count = 0
                    for root, dirs, files in os.walk(dir_info['path']):
                        file_count += len(files)
                    dir_info['file_count'] = file_count
                else:
                    dir_info['exists'] = False
                    dir_info['file_count'] = 0
                
                # 递归检查子目录
                if 'subdirectories' in dir_info:
                    for subdir_name, subdir_info in dir_info['subdirectories'].items():
                        check_directory_recursive(subdir_info)
            
            # 检查所有目录
            for dir_name, dir_info in data_directories.items():
                check_directory_recursive(dir_info)
            
            return {
                'success': True,
                'data': data_directories,
                'message': '目录结构获取成功'
            }
            
        except Exception as e:
            logger.error("获取目录结构失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_directory_files_request(self, directory_path):
        """
        获取目录中的文件列表
        :param directory_path: 目录路径
        :return: 文件列表数据
        """
        try:
            import os
            
            # 验证目录是否存在
            if not os.path.exists(directory_path):
                return self._create_error_response(404, ['目录不存在'])
            
            # 验证是否是目录
            if not os.path.isdir(directory_path):
                return self._create_error_response(400, ['路径不是目录'])
            
            # 获取目录中的文件
            files = []
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    # 获取文件信息
                    file_info = {
                        'name': filename,
                        'path': file_path.replace('\\', '/'),
                        'size': os.path.getsize(file_path),
                        'modified': os.path.getmtime(file_path),
                        'is_image': filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
                    }
                    files.append(file_info)
            
            # 按文件名排序
            files.sort(key=lambda x: x['name'])
            
            return {
                'success': True,
                'data': files,
                'message': '文件列表获取成功'
            }
            
        except Exception as e:
            logger.error("获取目录文件失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_patient_list_request(self):
        """
        获取患者列表
        :return: 响应数据
        """
        try:
            logger.info("收到患者列表请求")
            
            # 从数据库查询所有患者
            patients = self.db.query(Patient).all()
            
            # 构建响应数据
            patient_list = []
            for patient in patients:
                patient_list.append({
                    'id': patient.id,
                    'user_id': patient.user_id,
                    'name': patient.name,
                    'age': patient.age,
                    'gender': patient.gender,
                    'education_years': patient.education_years,
                    'contact_info': patient.contact_info,
                    'created_at': patient.created_at.isoformat()
                })
            
            response = {
                'success': True,
                'data': patient_list,
                'message': '患者列表获取成功'
            }
            
            logger.info("患者列表请求处理完成")
            return response
            
        except Exception as e:
            logger.error("患者列表请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_patient_detail_request(self, patient_id):
        """
        获取患者详情
        :param patient_id: 患者ID
        :return: 响应数据
        """
        try:
            logger.info(f"收到患者详情请求: {patient_id}")
            
            # 从数据库查询患者
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
            
            if not patient:
                return self._create_error_response(404, ['患者不存在'])
            
            # 构建响应数据
            patient_detail = {
                'id': patient.id,
                'user_id': patient.user_id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'education_years': patient.education_years,
                'contact_info': patient.contact_info,
                'medical_history': patient.medical_history,
                'created_at': patient.created_at.isoformat(),
                'updated_at': patient.updated_at.isoformat()
            }
            
            response = {
                'success': True,
                'data': patient_detail,
                'message': '患者详情获取成功'
            }
            
            logger.info("患者详情请求处理完成")
            return response
            
        except Exception as e:
            logger.error("患者详情请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_patient_create_request(self, request_data):
        """
        创建患者
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info("收到创建患者请求")
            
            # 验证请求数据
            required_fields = ['user_id', 'name', 'age', 'gender']
            for field in required_fields:
                if field not in request_data:
                    return self._create_error_response(400, [f'缺少必要字段: {field}'])
            
            # 检查用户是否存在
            user = self.db.query(User).filter(User.id == request_data['user_id']).first()
            if not user:
                return self._create_error_response(404, ['用户不存在'])
            
            # 检查用户角色是否为患者
            if user.role != 'patient':
                return self._create_error_response(400, ['用户角色必须是患者'])
            
            # 检查是否已存在患者记录
            existing_patient = self.db.query(Patient).filter(Patient.user_id == request_data['user_id']).first()
            if existing_patient:
                return self._create_error_response(400, ['该用户已存在患者记录'])
            
            # 创建新患者
            new_patient = Patient(
                user_id=request_data['user_id'],
                name=request_data['name'],
                age=request_data['age'],
                gender=request_data['gender'],
                education_years=request_data.get('education_years'),
                contact_info=request_data.get('contact_info'),
                medical_history=request_data.get('medical_history')
            )
            
            self.db.add(new_patient)
            self.db.commit()
            self.db.refresh(new_patient)
            
            logger.info(f"新患者创建成功: {new_patient.name}")
            
            return {
                'success': True,
                'data': {
                    'id': new_patient.id,
                    'name': new_patient.name,
                    'user_id': new_patient.user_id
                },
                'message': '患者创建成功'
            }
            
        except Exception as e:
            logger.error("创建患者请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_patient_update_request(self, patient_id, request_data):
        """
        更新患者信息
        :param patient_id: 患者ID
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info(f"收到更新患者请求: {patient_id}")
            
            # 从数据库查询患者
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
            
            if not patient:
                return self._create_error_response(404, ['患者不存在'])
            
            # 更新患者信息
            if 'name' in request_data:
                patient.name = request_data['name']
            if 'age' in request_data:
                patient.age = request_data['age']
            if 'gender' in request_data:
                patient.gender = request_data['gender']
            if 'education_years' in request_data:
                patient.education_years = request_data['education_years']
            if 'contact_info' in request_data:
                patient.contact_info = request_data['contact_info']
            if 'medical_history' in request_data:
                patient.medical_history = request_data['medical_history']
            
            self.db.commit()
            
            logger.info(f"患者更新成功: {patient.name}")
            
            return {
                'success': True,
                'data': {
                    'id': patient.id,
                    'name': patient.name
                },
                'message': '患者更新成功'
            }
            
        except Exception as e:
            logger.error("更新患者请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_patient_delete_request(self, patient_id):
        """
        删除患者
        :param patient_id: 患者ID
        :return: 响应数据
        """
        try:
            logger.info(f"收到删除患者请求: {patient_id}")
            
            # 从数据库查询患者
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
            
            if not patient:
                return self._create_error_response(404, ['患者不存在'])
            
            # 删除患者
            self.db.delete(patient)
            self.db.commit()
            
            logger.info(f"患者删除成功: {patient.name}")
            
            return {
                'success': True,
                'message': '患者删除成功'
            }
            
        except Exception as e:
            logger.error("删除患者请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_teleconsultation_list_request(self):
        """
        获取远程会诊列表
        :return: 响应数据
        """
        try:
            logger.info("收到远程会诊列表请求")
            
            # 从数据库查询所有远程会诊
            consultations = self.db.query(Teleconsultation).all()
            
            # 构建响应数据
            consultation_list = []
            for consultation in consultations:
                consultation_list.append({
                    'id': consultation.id,
                    'patient_id': consultation.patient_id,
                    'doctor_id': consultation.doctor_id,
                    'consultation_date': consultation.consultation_date.isoformat(),
                    'status': consultation.status,
                    'meeting_link': consultation.meeting_link,
                    'created_at': consultation.created_at.isoformat()
                })
            
            response = {
                'success': True,
                'data': consultation_list,
                'message': '远程会诊列表获取成功'
            }
            
            logger.info("远程会诊列表请求处理完成")
            return response
            
        except Exception as e:
            logger.error("远程会诊列表请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_teleconsultation_detail_request(self, consultation_id):
        """
        获取远程会诊详情
        :param consultation_id: 会诊ID
        :return: 响应数据
        """
        try:
            logger.info(f"收到远程会诊详情请求: {consultation_id}")
            
            # 从数据库查询远程会诊
            consultation = self.db.query(Teleconsultation).filter(Teleconsultation.id == consultation_id).first()
            
            if not consultation:
                return self._create_error_response(404, ['远程会诊不存在'])
            
            # 构建响应数据
            consultation_detail = {
                'id': consultation.id,
                'patient_id': consultation.patient_id,
                'doctor_id': consultation.doctor_id,
                'consultation_date': consultation.consultation_date.isoformat(),
                'status': consultation.status,
                'meeting_link': consultation.meeting_link,
                'notes': consultation.notes,
                'created_at': consultation.created_at.isoformat(),
                'updated_at': consultation.updated_at.isoformat()
            }
            
            response = {
                'success': True,
                'data': consultation_detail,
                'message': '远程会诊详情获取成功'
            }
            
            logger.info("远程会诊详情请求处理完成")
            return response
            
        except Exception as e:
            logger.error("远程会诊详情请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_teleconsultation_create_request(self, request_data):
        """
        创建远程会诊
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info("收到创建远程会诊请求")
            
            # 验证请求数据
            required_fields = ['patient_id', 'doctor_id', 'consultation_date', 'status']
            for field in required_fields:
                if field not in request_data:
                    return self._create_error_response(400, [f'缺少必要字段: {field}'])
            
            # 检查患者是否存在
            patient = self.db.query(Patient).filter(Patient.id == request_data['patient_id']).first()
            if not patient:
                return self._create_error_response(404, ['患者不存在'])
            
            # 检查医生是否存在
            doctor = self.db.query(Doctor).filter(Doctor.id == request_data['doctor_id']).first()
            if not doctor:
                return self._create_error_response(404, ['医生不存在'])
            
            # 转换日期字符串为datetime对象
            from datetime import datetime
            consultation_date = request_data['consultation_date']
            if isinstance(consultation_date, str):
                try:
                    consultation_date = datetime.fromisoformat(consultation_date)
                except ValueError:
                    return self._create_error_response(400, ['日期格式不正确，请使用ISO格式（如：2026-04-12T10:00:00）'])
            
            # 创建新远程会诊
            new_consultation = Teleconsultation(
                patient_id=request_data['patient_id'],
                doctor_id=request_data['doctor_id'],
                consultation_date=consultation_date,
                status=request_data['status'],
                meeting_link=request_data.get('meeting_link'),
                notes=request_data.get('notes')
            )
            
            self.db.add(new_consultation)
            self.db.commit()
            self.db.refresh(new_consultation)
            
            logger.info(f"新远程会诊创建成功: ID {new_consultation.id}")
            
            return {
                'success': True,
                'data': {
                    'id': new_consultation.id,
                    'patient_id': new_consultation.patient_id,
                    'doctor_id': new_consultation.doctor_id,
                    'status': new_consultation.status
                },
                'message': '远程会诊创建成功'
            }
            
        except Exception as e:
            logger.error("创建远程会诊请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_teleconsultation_update_request(self, consultation_id, request_data):
        """
        更新远程会诊状态
        :param consultation_id: 会诊ID
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info(f"收到更新远程会诊请求: {consultation_id}")
            
            # 从数据库查询远程会诊
            consultation = self.db.query(Teleconsultation).filter(Teleconsultation.id == consultation_id).first()
            
            if not consultation:
                return self._create_error_response(404, ['远程会诊不存在'])
            
            # 更新远程会诊信息
            if 'status' in request_data:
                consultation.status = request_data['status']
            if 'meeting_link' in request_data:
                consultation.meeting_link = request_data['meeting_link']
            if 'notes' in request_data:
                consultation.notes = request_data['notes']
            
            self.db.commit()
            
            logger.info(f"远程会诊更新成功: ID {consultation.id}")
            
            return {
                'success': True,
                'data': {
                    'id': consultation.id,
                    'status': consultation.status
                },
                'message': '远程会诊更新成功'
            }
            
        except Exception as e:
            logger.error("更新远程会诊请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_teleconsultation_delete_request(self, consultation_id):
        """
        删除远程会诊
        :param consultation_id: 会诊ID
        :return: 响应数据
        """
        try:
            logger.info(f"收到删除远程会诊请求: {consultation_id}")
            
            # 从数据库查询远程会诊
            consultation = self.db.query(Teleconsultation).filter(Teleconsultation.id == consultation_id).first()
            
            if not consultation:
                return self._create_error_response(404, ['远程会诊不存在'])
            
            # 删除远程会诊
            self.db.delete(consultation)
            self.db.commit()
            
            logger.info(f"远程会诊删除成功: ID {consultation_id}")
            
            return {
                'success': True,
                'message': '远程会诊删除成功'
            }
            
        except Exception as e:
            logger.error("删除远程会诊请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_lifestyle_data_request(self, patient_id):
        """
        获取患者生活方式数据
        :param patient_id: 患者ID
        :return: 响应数据
        """
        try:
            logger.info(f"收到获取患者生活方式数据请求: {patient_id}")
            
            # 从数据库查询生活方式数据
            lifestyle_data = self.db.query(LifestyleData).filter(LifestyleData.patient_id == patient_id).first()
            
            if not lifestyle_data:
                # 返回空数据结构
                return {
                    'success': True,
                    'data': {
                        'id': None,
                        'patient_id': patient_id,
                        'exercise_frequency': None,
                        'sleep_duration': None,
                        'diet_health': None,
                        'social_activities': None,
                        'smoking_status': None,
                        'alcohol_consumption': None
                    },
                    'message': '生活方式数据不存在，返回空数据'
                }
            
            # 构建响应数据
            data = {
                'id': lifestyle_data.id,
                'patient_id': lifestyle_data.patient_id,
                'exercise_frequency': lifestyle_data.exercise_frequency,
                'sleep_duration': lifestyle_data.sleep_duration,
                'diet_health': lifestyle_data.diet_health,
                'social_activities': lifestyle_data.social_activities,
                'smoking_status': lifestyle_data.smoking_status,
                'alcohol_consumption': lifestyle_data.alcohol_consumption,
                'created_at': lifestyle_data.created_at.isoformat(),
                'updated_at': lifestyle_data.updated_at.isoformat()
            }
            
            response = {
                'success': True,
                'data': data,
                'message': '生活方式数据获取成功'
            }
            
            logger.info("生活方式数据请求处理完成")
            return response
            
        except Exception as e:
            logger.error("获取生活方式数据请求处理失败", e)
            return self._create_error_response(500, [str(e)])
    
    def handle_lifestyle_data_update_request(self, patient_id, request_data):
        """
        更新患者生活方式数据
        :param patient_id: 患者ID
        :param request_data: 请求数据
        :return: 响应数据
        """
        try:
            logger.info(f"收到更新患者生活方式数据请求: {patient_id}")
            
            # 检查患者是否存在
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
            if not patient:
                return self._create_error_response(404, ['患者不存在'])
            
            # 查找或创建生活方式数据
            lifestyle_data = self.db.query(LifestyleData).filter(LifestyleData.patient_id == patient_id).first()
            
            if not lifestyle_data:
                # 创建新的生活方式数据
                lifestyle_data = LifestyleData(patient_id=patient_id)
                self.db.add(lifestyle_data)
                logger.info(f"为患者创建新的生活方式数据: {patient_id}")
            
            # 更新生活方式数据
            if 'exercise_frequency' in request_data:
                lifestyle_data.exercise_frequency = request_data['exercise_frequency']
            if 'sleep_duration' in request_data:
                lifestyle_data.sleep_duration = request_data['sleep_duration']
            if 'diet_health' in request_data:
                lifestyle_data.diet_health = request_data['diet_health']
            if 'social_activities' in request_data:
                lifestyle_data.social_activities = request_data['social_activities']
            if 'smoking_status' in request_data:
                lifestyle_data.smoking_status = request_data['smoking_status']
            if 'alcohol_consumption' in request_data:
                lifestyle_data.alcohol_consumption = request_data['alcohol_consumption']
            
            self.db.commit()
            self.db.refresh(lifestyle_data)
            
            logger.info(f"患者生活方式数据更新成功: {patient_id}")
            
            # 构建响应数据
            data = {
                'id': lifestyle_data.id,
                'patient_id': lifestyle_data.patient_id,
                'exercise_frequency': lifestyle_data.exercise_frequency,
                'sleep_duration': lifestyle_data.sleep_duration,
                'diet_health': lifestyle_data.diet_health,
                'social_activities': lifestyle_data.social_activities,
                'smoking_status': lifestyle_data.smoking_status,
                'alcohol_consumption': lifestyle_data.alcohol_consumption
            }
            
            return {
                'success': True,
                'data': data,
                'message': '生活方式数据更新成功'
            }
            
        except Exception as e:
            logger.error("更新生活方式数据请求处理失败", e)
            self.db.rollback()
            return self._create_error_response(500, [str(e)])
    
    def handle_patient_by_user_id_request(self, user_id):
        """
        根据用户ID获取患者信息
        :param user_id: 用户ID
        :return: 响应数据
        """
        try:
            logger.info(f"收到根据用户ID获取患者信息请求: {user_id}")
            
            # 从数据库查询患者
            patient = self.db.query(Patient).filter(Patient.user_id == user_id).first()
            
            if not patient:
                return self._create_error_response(404, ['患者记录不存在'])
            
            # 构建响应数据
            patient_detail = {
                'id': patient.id,
                'user_id': patient.user_id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'education_years': patient.education_years,
                'contact_info': patient.contact_info,
                'medical_history': patient.medical_history,
                'created_at': patient.created_at.isoformat(),
                'updated_at': patient.updated_at.isoformat()
            }
            
            # 获取生活方式数据
            lifestyle_data = self.db.query(LifestyleData).filter(LifestyleData.patient_id == patient.id).first()
            if lifestyle_data:
                patient_detail['lifestyle_data'] = {
                    'id': lifestyle_data.id,
                    'exercise_frequency': lifestyle_data.exercise_frequency,
                    'sleep_duration': lifestyle_data.sleep_duration,
                    'diet_health': lifestyle_data.diet_health,
                    'social_activities': lifestyle_data.social_activities,
                    'smoking_status': lifestyle_data.smoking_status,
                    'alcohol_consumption': lifestyle_data.alcohol_consumption
                }
            
            response = {
                'success': True,
                'data': patient_detail,
                'message': '患者信息获取成功'
            }
            
            logger.info("根据用户ID获取患者信息请求处理完成")
            return response
            
        except Exception as e:
            logger.error("根据用户ID获取患者信息请求处理失败", e)
            return self._create_error_response(500, [str(e)])
