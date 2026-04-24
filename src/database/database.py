"""
数据库连接和会话管理
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
import os

# 数据库连接配置
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./alzheimer.db')

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项，用于获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成")
