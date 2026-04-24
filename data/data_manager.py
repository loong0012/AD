"""
多模态数据管理模块
用于管理和处理患者的多模态医疗数据
"""

import os
import json
import numpy as np
import csv
from datetime import datetime


class MultiModalDataManager:
    """多模态数据管理器"""

    def __init__(self):
        self.data_directories = {
            'images': './uploaded_img',
            'clinical': './clinical_data/clinical_records',
            'molecular': './clinical_data/molecular_data',
            'lifestyle': './clinical_data/lifestyle_data',
            'neuropsych': './clinical_data/neuropsychological'
        }

    def save_patient_data(self, patient_id, data_dict):
        """保存患者的多模态数据"""

        # 1. 影像数据
        if 'mri_image' in data_dict:
            mri_path = f"{self.data_directories['images']}/{patient_id}_mri.npy"
            np.save(mri_path, data_dict['mri_image'])

        if 'pet_image' in data_dict:
            pet_path = f"{self.data_directories['images']}/{patient_id}_pet.npy"
            np.save(pet_path, data_dict['pet_image'])

        # 2. 临床数据
        if 'clinical_info' in data_dict:
            clinical_path = f"{self.data_directories['clinical']}/{patient_id}_clinical.json"
            with open(clinical_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict['clinical_info'], f, ensure_ascii=False, indent=2)

        # 3. 分子数据
        if 'molecular_data' in data_dict:
            molecular_path = f"{self.data_directories['molecular']}/{patient_id}_molecular.csv"
            with open(molecular_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for row in data_dict['molecular_data']:
                    writer.writerow(row)

        # 4. 生活方式数据
        if 'lifestyle_data' in data_dict:
            lifestyle_path = f"{self.data_directories['lifestyle']}/{patient_id}_lifestyle.json"
            with open(lifestyle_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict['lifestyle_data'], f, ensure_ascii=False, indent=2)

        # 5. 神经心理学数据
        if 'neuropsychological_data' in data_dict:
            neuropsych_path = f"{self.data_directories['neuropsych']}/{patient_id}_neuropsych.json"
            with open(neuropsych_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict['neuropsychological_data'], f, ensure_ascii=False, indent=2)

        # 保存元数据
        metadata = {
            'patient_id': patient_id,
            'save_time': datetime.now().isoformat(),
            'modalities': list(data_dict.keys()),
            'data_sizes': {k: len(str(v)) for k, v in data_dict.items()}
        }

        metadata_path = f"./results/individual/{patient_id}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return True

    def load_patient_data(self, patient_id):
        """加载患者的多模态数据"""
        data = {}

        try:
            # 1. 检查影像数据
            mri_path = f"{self.data_directories['images']}/{patient_id}_mri.npy"
            if os.path.exists(mri_path):
                data['mri_image'] = np.load(mri_path)

            pet_path = f"{self.data_directories['images']}/{patient_id}_pet.npy"
            if os.path.exists(pet_path):
                data['pet_image'] = np.load(pet_path)

            # 2. 加载临床数据
            clinical_path = f"{self.data_directories['clinical']}/{patient_id}_clinical.json"
            if os.path.exists(clinical_path):
                with open(clinical_path, 'r', encoding='utf-8') as f:
                    data['clinical_info'] = json.load(f)

            # 3. 加载分子数据
            molecular_path = f"{self.data_directories['molecular']}/{patient_id}_molecular.csv"
            if os.path.exists(molecular_path):
                with open(molecular_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    data['molecular_data'] = list(reader)

            # 4. 加载生活方式数据
            lifestyle_path = f"{self.data_directories['lifestyle']}/{patient_id}_lifestyle.json"
            if os.path.exists(lifestyle_path):
                with open(lifestyle_path, 'r', encoding='utf-8') as f:
                    data['lifestyle_data'] = json.load(f)

            # 5. 加载神经心理学数据
            neuropsych_path = f"{self.data_directories['neuropsych']}/{patient_id}_neuropsych.json"
            if os.path.exists(neuropsych_path):
                with open(neuropsych_path, 'r', encoding='utf-8') as f:
                    data['neuropsychological_data'] = json.load(f)

            return data

        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return None

    def create_demo_multimodal_data(self, category=None):
        """创建完整的多模态演示数据"""
        print(f"Creating multimodal demo data (category: {category})...")

        # 根据类别设置不同的患者ID
        patient_id = f"DEMO_{category or 'CN'}"

        # 1. 创建MRI数据
        self.create_demo_mri_data(category)

        # 2. 创建临床数据
        if category == "CN":
            # 认知正常
            clinical_data = {
                "patient_id": patient_id,
                "demographics": {
                    "age": 68,
                    "gender": "female",
                    "education_years": 16,
                    "apoe_genotype": "ε3/ε3",
                    "race": "Asian",
                    "height_cm": 165,
                    "weight_kg": 62,
                    "bmi": 22.8
                },
                "medical_history": {
                    "family_history_ad": False,
                    "hypertension": False,
                    "diabetes": False,
                    "depression_history": False,
                    "stroke_history": False,
                    "heart_disease": False,
                    "smoking_status": "never",
                    "alcohol_use": "none"
                },
                "vital_signs": {
                    "systolic_bp": 120,
                    "diastolic_bp": 80,
                    "heart_rate": 68,
                    "temperature": 36.3
                }
            }
        elif category == "EMCI":
            # 早期MCI
            clinical_data = {
                "patient_id": patient_id,
                "demographics": {
                    "age": 70,
                    "gender": "male",
                    "education_years": 14,
                    "apoe_genotype": "ε3/ε4",
                    "race": "Asian",
                    "height_cm": 172,
                    "weight_kg": 70,
                    "bmi": 23.8
                },
                "medical_history": {
                    "family_history_ad": True,
                    "hypertension": True,
                    "diabetes": False,
                    "depression_history": True,
                    "stroke_history": False,
                    "heart_disease": False,
                    "smoking_status": "former",
                    "alcohol_use": "moderate"
                },
                "vital_signs": {
                    "systolic_bp": 130,
                    "diastolic_bp": 85,
                    "heart_rate": 75,
                    "temperature": 36.5
                }
            }
        elif category == "MCI":
            # 轻度认知障碍
            clinical_data = {
                "patient_id": patient_id,
                "demographics": {
                    "age": 72,
                    "gender": "male",
                    "education_years": 12,
                    "apoe_genotype": "ε4/ε4",
                    "race": "Asian",
                    "height_cm": 170,
                    "weight_kg": 75,
                    "bmi": 25.9
                },
                "medical_history": {
                    "family_history_ad": True,
                    "hypertension": True,
                    "diabetes": False,
                    "depression_history": False,
                    "stroke_history": False,
                    "heart_disease": False,
                    "smoking_status": "former",
                    "alcohol_use": "moderate"
                },
                "vital_signs": {
                    "systolic_bp": 135,
                    "diastolic_bp": 85,
                    "heart_rate": 72,
                    "temperature": 36.5
                }
            }
        elif category == "AD":
            # 阿尔兹海默症
            clinical_data = {
                "patient_id": patient_id,
                "demographics": {
                    "age": 78,
                    "gender": "female",
                    "education_years": 10,
                    "apoe_genotype": "ε4/ε4",
                    "race": "Asian",
                    "height_cm": 158,
                    "weight_kg": 58,
                    "bmi": 23.1
                },
                "medical_history": {
                    "family_history_ad": True,
                    "hypertension": True,
                    "diabetes": True,
                    "depression_history": True,
                    "stroke_history": True,
                    "heart_disease": True,
                    "smoking_status": "former",
                    "alcohol_use": "none"
                },
                "vital_signs": {
                    "systolic_bp": 145,
                    "diastolic_bp": 90,
                    "heart_rate": 80,
                    "temperature": 36.7
                }
            }
        else:
            # 默认MCI
            clinical_data = {
                "patient_id": patient_id,
                "demographics": {
                    "age": 72,
                    "gender": "male",
                    "education_years": 12,
                    "apoe_genotype": "ε4/ε4",
                    "race": "Asian",
                    "height_cm": 170,
                    "weight_kg": 75,
                    "bmi": 25.9
                },
                "medical_history": {
                    "family_history_ad": True,
                    "hypertension": True,
                    "diabetes": False,
                    "depression_history": False,
                    "stroke_history": False,
                    "heart_disease": False,
                    "smoking_status": "former",
                    "alcohol_use": "moderate"
                },
                "vital_signs": {
                    "systolic_bp": 135,
                    "diastolic_bp": 85,
                    "heart_rate": 72,
                    "temperature": 36.5
                }
            }

        clinical_path = f"{self.data_directories['clinical']}/{patient_id}_clinical.json"
        with open(clinical_path, 'w', encoding='utf-8') as f:
            json.dump(clinical_data, f, ensure_ascii=False, indent=2)

        # 3. 创建分子数据
        if category == "CN":
            molecular_data = [
                ["biomarker", "value", "unit", "reference_range", "status"],
                ["Aβ42", "750", "pg/mL", ">600", "normal"],
                ["p-tau217", "25.5", "pg/mL", "<40", "normal"],
                ["t-tau", "45.2", "pg/mL", "<80", "normal"],
                ["NfL", "12.8", "pg/mL", "<16", "normal"],
                ["GFAP", "65", "pg/mL", "<90", "normal"],
                ["Aβ42/Aβ40", "0.45", "ratio", "0.2-0.4", "normal"],
                ["ApoE4", "0", "copies", "0-2", "negative"]
            ]
        elif category == "EMCI":
            molecular_data = [
                ["biomarker", "value", "unit", "reference_range", "status"],
                ["Aβ42", "620", "pg/mL", ">600", "borderline"],
                ["p-tau217", "38.5", "pg/mL", "<40", "borderline"],
                ["t-tau", "55.3", "pg/mL", "<80", "normal"],
                ["NfL", "18.2", "pg/mL", "<16", "abnormal"],
                ["GFAP", "95", "pg/mL", "<90", "abnormal"],
                ["Aβ42/Aβ40", "0.35", "ratio", "0.2-0.4", "normal"],
                ["ApoE4", "1", "copies", "0-2", "positive"]
            ]
        elif category == "MCI":
            molecular_data = [
                ["biomarker", "value", "unit", "reference_range", "status"],
                ["Aβ42", "550", "pg/mL", ">600", "abnormal"],
                ["p-tau217", "78.2", "pg/mL", "<40", "abnormal"],
                ["t-tau", "65.3", "pg/mL", "<80", "normal"],
                ["NfL", "25.1", "pg/mL", "<16", "abnormal"],
                ["GFAP", "145", "pg/mL", "<90", "abnormal"],
                ["Aβ42/Aβ40", "0.28", "ratio", "0.2-0.4", "borderline"],
                ["ApoE4", "2", "copies", "0-2", "positive"]
            ]
        elif category == "AD":
            molecular_data = [
                ["biomarker", "value", "unit", "reference_range", "status"],
                ["Aβ42", "380", "pg/mL", ">600", "abnormal"],
                ["p-tau217", "125.6", "pg/mL", "<40", "abnormal"],
                ["t-tau", "95.8", "pg/mL", "<80", "abnormal"],
                ["NfL", "42.5", "pg/mL", "<16", "abnormal"],
                ["GFAP", "210", "pg/mL", "<90", "abnormal"],
                ["Aβ42/Aβ40", "0.15", "ratio", "0.2-0.4", "abnormal"],
                ["ApoE4", "2", "copies", "0-2", "positive"]
            ]
        else:
            molecular_data = [
                ["biomarker", "value", "unit", "reference_range", "status"],
                ["Aβ42", "550", "pg/mL", ">600", "abnormal"],
                ["p-tau217", "78.2", "pg/mL", "<40", "abnormal"],
                ["t-tau", "65.3", "pg/mL", "<80", "normal"],
                ["NfL", "25.1", "pg/mL", "<16", "abnormal"],
                ["GFAP", "145", "pg/mL", "<90", "abnormal"],
                ["Aβ42/Aβ40", "0.28", "ratio", "0.2-0.4", "borderline"],
                ["ApoE4", "2", "copies", "0-2", "positive"]
            ]

        molecular_path = f"{self.data_directories['molecular']}/{patient_id}_molecular.csv"
        with open(molecular_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(molecular_data)

        # 4. 创建生活方式数据
        if category == "CN":
            lifestyle_data = {
                "physical_activity": {
                    "minutes_per_week": 300,
                    "type": ["walking", "swimming", "cycling"],
                    "intensity": "moderate-vigorous",
                    "sedentary_hours": 4
                },
                "diet": {
                    "mediterranean_diet_score": 9,
                    "omega3_intake": "high",
                    "antioxidant_rich_foods": True,
                    "processed_foods": "very low",
                    "sugar_intake": "low"
                },
                "cognitive_activities": {
                    "reading_frequency": "daily",
                    "puzzle_solving": "daily",
                    "social_engagement": "very high",
                    "learning_new_skills": "weekly"
                },
                "sleep": {
                    "hours_per_night": 7.5,
                    "quality": "excellent",
                    "sleep_disorders": "none"
                },
                "stress_and_mental_health": {
                    "stress_level": "low",
                    "depression_symptoms": "none",
                    "anxiety_level": "low",
                    "social_support": "excellent"
                }
            }
        elif category == "EMCI":
            lifestyle_data = {
                "physical_activity": {
                    "minutes_per_week": 180,
                    "type": ["walking", "light exercise"],
                    "intensity": "moderate",
                    "sedentary_hours": 6
                },
                "diet": {
                    "mediterranean_diet_score": 6,
                    "omega3_intake": "moderate",
                    "antioxidant_rich_foods": True,
                    "processed_foods": "moderate",
                    "sugar_intake": "moderate"
                },
                "cognitive_activities": {
                    "reading_frequency": "weekly",
                    "puzzle_solving": "weekly",
                    "social_engagement": "moderate",
                    "learning_new_skills": "monthly"
                },
                "sleep": {
                    "hours_per_night": 6.5,
                    "quality": "fair",
                    "sleep_disorders": "mild insomnia"
                },
                "stress_and_mental_health": {
                    "stress_level": "moderate",
                    "depression_symptoms": "mild",
                    "anxiety_level": "moderate",
                    "social_support": "good"
                }
            }
        elif category == "MCI":
            lifestyle_data = {
                "physical_activity": {
                    "minutes_per_week": 120,
                    "type": ["walking"],
                    "intensity": "light",
                    "sedentary_hours": 8
                },
                "diet": {
                    "mediterranean_diet_score": 5,
                    "omega3_intake": "low",
                    "antioxidant_rich_foods": False,
                    "processed_foods": "high",
                    "sugar_intake": "high"
                },
                "cognitive_activities": {
                    "reading_frequency": "monthly",
                    "puzzle_solving": "rarely",
                    "social_engagement": "low",
                    "learning_new_skills": "rarely"
                },
                "sleep": {
                    "hours_per_night": 5.5,
                    "quality": "poor",
                    "sleep_disorders": "moderate insomnia"
                },
                "stress_and_mental_health": {
                    "stress_level": "high",
                    "depression_symptoms": "moderate",
                    "anxiety_level": "high",
                    "social_support": "limited"
                }
            }
        elif category == "AD":
            lifestyle_data = {
                "physical_activity": {
                    "minutes_per_week": 60,
                    "type": ["very light walking"],
                    "intensity": "very light",
                    "sedentary_hours": 10
                },
                "diet": {
                    "mediterranean_diet_score": 3,
                    "omega3_intake": "very low",
                    "antioxidant_rich_foods": False,
                    "processed_foods": "very high",
                    "sugar_intake": "very high"
                },
                "cognitive_activities": {
                    "reading_frequency": "rarely",
                    "puzzle_solving": "never",
                    "social_engagement": "very low",
                    "learning_new_skills": "never"
                },
                "sleep": {
                    "hours_per_night": 4.5,
                    "quality": "very poor",
                    "sleep_disorders": "severe insomnia"
                },
                "stress_and_mental_health": {
                    "stress_level": "very high",
                    "depression_symptoms": "severe",
                    "anxiety_level": "very high",
                    "social_support": "minimal"
                }
            }
        else:
            lifestyle_data = {
                "physical_activity": {
                    "minutes_per_week": 120,
                    "type": ["walking"],
                    "intensity": "light",
                    "sedentary_hours": 8
                },
                "diet": {
                    "mediterranean_diet_score": 5,
                    "omega3_intake": "low",
                    "antioxidant_rich_foods": False,
                    "processed_foods": "high",
                    "sugar_intake": "high"
                },
                "cognitive_activities": {
                    "reading_frequency": "monthly",
                    "puzzle_solving": "rarely",
                    "social_engagement": "low",
                    "learning_new_skills": "rarely"
                },
                "sleep": {
                    "hours_per_night": 5.5,
                    "quality": "poor",
                    "sleep_disorders": "moderate insomnia"
                },
                "stress_and_mental_health": {
                    "stress_level": "high",
                    "depression_symptoms": "moderate",
                    "anxiety_level": "high",
                    "social_support": "limited"
                }
            }

        lifestyle_path = f"{self.data_directories['lifestyle']}/{patient_id}_lifestyle.json"
        with open(lifestyle_path, 'w', encoding='utf-8') as f:
            json.dump(lifestyle_data, f, ensure_ascii=False, indent=2)

        # 5. 创建神经心理学数据
        if category == "CN":
            neuropsych_data = {
                "mmse": {
                    "score": 29,
                    "max_score": 30,
                    "interpretation": "normal"
                },
                "cdr": {
                    "score": 0,
                    "interpretation": "normal"
                },
                "adni_mem": {
                    "score": 0.1,
                    "interpretation": "normal"
                },
                "clock_drawing_test": {
                    "score": 5,
                    "max_score": 5,
                    "interpretation": "normal"
                },
                "trail_making_test": {
                    "part_a_seconds": 30,
                    "part_b_seconds": 60,
                    "interpretation": "normal"
                },
                "verbal_fluency": {
                    "animals_count": 20,
                    "interpretation": "normal"
                }
            }
        elif category == "EMCI":
            neuropsych_data = {
                "mmse": {
                    "score": 27,
                    "max_score": 30,
                    "interpretation": "borderline"
                },
                "cdr": {
                    "score": 0.5,
                    "interpretation": "questionable_dementia"
                },
                "adni_mem": {
                    "score": 0.4,
                    "interpretation": "borderline"
                },
                "clock_drawing_test": {
                    "score": 4,
                    "max_score": 5,
                    "interpretation": "borderline"
                },
                "trail_making_test": {
                    "part_a_seconds": 40,
                    "part_b_seconds": 90,
                    "interpretation": "borderline"
                },
                "verbal_fluency": {
                    "animals_count": 16,
                    "interpretation": "borderline"
                }
            }
        elif category == "MCI":
            neuropsych_data = {
                "mmse": {
                    "score": 24,
                    "max_score": 30,
                    "interpretation": "mild_impairment"
                },
                "cdr": {
                    "score": 0.5,
                    "interpretation": "questionable_dementia"
                },
                "adni_mem": {
                    "score": 0.7,
                    "interpretation": "impaired"
                },
                "clock_drawing_test": {
                    "score": 3,
                    "max_score": 5,
                    "interpretation": "abnormal"
                },
                "trail_making_test": {
                    "part_a_seconds": 50,
                    "part_b_seconds": 120,
                    "interpretation": "impaired"
                },
                "verbal_fluency": {
                    "animals_count": 12,
                    "interpretation": "mild_impairment"
                }
            }
        elif category == "AD":
            neuropsych_data = {
                "mmse": {
                    "score": 18,
                    "max_score": 30,
                    "interpretation": "moderate_impairment"
                },
                "cdr": {
                    "score": 1,
                    "interpretation": "mild_dementia"
                },
                "adni_mem": {
                    "score": 0.9,
                    "interpretation": "severely_impaired"
                },
                "clock_drawing_test": {
                    "score": 1,
                    "max_score": 5,
                    "interpretation": "severely_abnormal"
                },
                "trail_making_test": {
                    "part_a_seconds": 80,
                    "part_b_seconds": 200,
                    "interpretation": "severely_impaired"
                },
                "verbal_fluency": {
                    "animals_count": 5,
                    "interpretation": "severe_impairment"
                }
            }
        else:
            neuropsych_data = {
                "mmse": {
                    "score": 24,
                    "max_score": 30,
                    "interpretation": "mild_impairment"
                },
                "cdr": {
                    "score": 0.5,
                    "interpretation": "questionable_dementia"
                },
                "adni_mem": {
                    "score": 0.7,
                    "interpretation": "impaired"
                },
                "clock_drawing_test": {
                    "score": 3,
                    "max_score": 5,
                    "interpretation": "abnormal"
                },
                "trail_making_test": {
                    "part_a_seconds": 50,
                    "part_b_seconds": 120,
                    "interpretation": "impaired"
                },
                "verbal_fluency": {
                    "animals_count": 12,
                    "interpretation": "mild_impairment"
                }
            }

        neuropsych_path = f"{self.data_directories['neuropsych']}/{patient_id}_neuropsych.json"
        with open(neuropsych_path, 'w', encoding='utf-8') as f:
            json.dump(neuropsych_data, f, ensure_ascii=False, indent=2)

        print("✅ 多模态演示数据已创建")
        return True

    def create_demo_mri_data(self, category=None):
        """创建示例MRI数据"""
        demo_path = "./demodata/demo_mri.npy"

        if not os.path.exists(demo_path):
            print("Creating sample MRI data...")

            # 创建模拟MRI数据
            depth, height, width = 160, 256, 256
            demo_data = np.zeros((depth, height, width), dtype=np.float32)

            # 添加脑部结构
            for d in range(depth):
                for h in range(height):
                    for w in range(width):
                        # 创建椭球体模拟脑部
                        x = (w - width / 2) / (width / 4)
                        y = (h - height / 2) / (height / 4)
                        z = (d - depth / 2) / (depth / 4)

                        value = 1.0 - (x * x + y * y + z * z)

                        if value > 0:
                            demo_data[d, h, w] = value + np.random.normal(0, 0.1)

            # 添加病理特征
            hippocampus_center = (depth // 3, height // 2, width // 3)
            hippocampus_radius = 15

            for d in range(max(0, hippocampus_center[0] - hippocampus_radius),
                           min(depth, hippocampus_center[0] + hippocampus_radius)):
                for h in range(max(0, hippocampus_center[1] - hippocampus_radius),
                               min(height, hippocampus_center[1] + hippocampus_radius)):
                    for w in range(max(0, hippocampus_center[2] - hippocampus_radius),
                                   min(width, hippocampus_center[2] + hippocampus_radius)):
                        dist = np.sqrt((d - hippocampus_center[0]) ** 2 +
                                       (h - hippocampus_center[1]) ** 2 +
                                       (w - hippocampus_center[2]) ** 2)

                        if dist < hippocampus_radius:
                            # 模拟萎缩
                            demo_data[d, h, w] *= 0.7

            # 保存数据
            np.save(demo_path, demo_data)
            print(f"✅ 示例MRI数据已保存: {demo_path}")

        return demo_path
