"""
数据库初始化脚本
创建所有表并添加默认用户
"""

from src.database.database import init_db, SessionLocal
from src.database.models import User, Patient, Doctor
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_default_users():
    """创建默认用户"""
    db = SessionLocal()
    try:
        # 检查是否已存在用户
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("数据库中已存在用户，跳过默认用户创建")
            return
        
        # 创建默认管理员用户
        admin_user = User(
            username="admin",
            password_hash=pwd_context.hash("admin123"),
            email="admin@example.com",
            role="admin"
        )
        db.add(admin_user)
        
        # 创建默认医生用户
        doctor_user = User(
            username="doctor",
            password_hash=pwd_context.hash("doctor123"),
            email="doctor@example.com",
            role="doctor"
        )
        db.add(doctor_user)
        
        # 创建默认患者用户
        patient_user = User(
            username="patient",
            password_hash=pwd_context.hash("patient123"),
            email="patient@example.com",
            role="patient"
        )
        db.add(patient_user)
        
        # 提交事务
        db.commit()
        
        # 创建医生信息
        doctor = Doctor(
            user_id=doctor_user.id,
            name="张医生",
            specialty="神经内科",
            hospital="北京协和医院",
            license_number="123456789"
        )
        db.add(doctor)
        
        # 创建患者信息
        patient = Patient(
            user_id=patient_user.id,
            name="李患者",
            age=75,
            gender="男",
            education_years=12,
            contact_info="13800138000"
        )
        db.add(patient)
        
        # 再次提交事务
        db.commit()
        
        print("默认用户创建成功")
        print("管理员账号: admin / admin123")
        print("医生账号: doctor / doctor123")
        print("患者账号: patient / patient123")
        
    except Exception as e:
        print(f"创建默认用户失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始初始化数据库...")
    init_db()
    print("创建默认用户...")
    create_default_users()
    print("数据库初始化完成")
