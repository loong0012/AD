"""
数据库模型
定义系统所需的数据表结构
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """用户表"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)  # patient, doctor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    patient = relationship('Patient', back_populates='user', uselist=False)
    doctor = relationship('Doctor', back_populates='user', uselist=False)

class Patient(Base):
    """患者表"""
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    education_years = Column(Integer)
    contact_info = Column(String(255))
    medical_history = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship('User', back_populates='patient')
    diagnoses = relationship('Diagnosis', back_populates='patient')

class Doctor(Base):
    """医生表"""
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100))
    hospital = Column(String(255))
    license_number = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship('User', back_populates='doctor')

class Diagnosis(Base):
    """诊断结果表"""
    __tablename__ = 'diagnoses'
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    diagnosis_date = Column(DateTime, default=datetime.utcnow)
    pred_label = Column(String(50), nullable=False)  # CN, EMCI, LMCI, AD
    confidence = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    recommendations = Column(Text)
    report_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    patient = relationship('Patient', back_populates='diagnoses')

class LifestyleData(Base):
    """生活方式数据表"""
    __tablename__ = 'lifestyle_data'
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    exercise_frequency = Column(Integer)  # 每周运动次数
    sleep_duration = Column(Float)  # 每天睡眠时间
    diet_health = Column(String(20))  # low, medium, high
    social_activities = Column(Integer)  # 每周社交活动次数
    smoking_status = Column(String(20))  # never, past, current
    alcohol_consumption = Column(String(20))  # none, occasional, regular
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MolecularData(Base):
    """分子数据表"""
    __tablename__ = 'molecular_data'
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    biomarker_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    test_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class ClinicalRecord(Base):
    """临床记录表"""
    __tablename__ = 'clinical_records'
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    record_date = Column(DateTime, default=datetime.utcnow)
    symptoms = Column(Text)
    physical_exam = Column(Text)
    cognitive_test = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Teleconsultation(Base):
    """远程会诊表"""
    __tablename__ = 'teleconsultations'
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    consultation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)  # scheduled, completed, cancelled
    meeting_link = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
