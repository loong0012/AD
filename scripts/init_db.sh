#!/bin/bash
# 阿尔兹海默症诊断系统 - 数据库初始化脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 数据库初始化
init_database() {
    log_info "开始初始化数据库..."

    # 创建数据库目录
    mkdir -p ./data

    # 检查Python环境
    if ! command -v python &> /dev/null; then
        log_error "Python未安装，请先安装Python 3.11+"
        exit 1
    fi

    # 安装依赖
    if [ -f requirements.txt ]; then
        log_info "安装Python依赖..."
        pip install -q -r requirements.txt
    fi

    # 初始化数据库
    log_info "创建数据库表结构..."
    python -c "
import sys
sys.path.append('.')
from src.database.database import init_db, engine
from src.database.models import Base

try:
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print('数据库表创建成功')

    # 创建默认管理员账户（如果不存在）
    from src.database.models import User
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    session = Session()

    # 检查是否已存在管理员账户
    admin = session.query(User).filter(User.username == 'admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash='pbkdf2:sha256:260000\$randomsalt\$hashedpassword',
            email='admin@alzheimer-system.local',
            role='admin'
        )
        session.add(admin)
        session.commit()
        print('默认管理员账户已创建')
        print('用户名: admin')
        print('密码: admin123 (请立即修改)')
    else:
        print('管理员账户已存在')

    session.close()
    print('数据库初始化完成')

except Exception as e:
    print(f'数据库初始化失败: {e}')
    sys.exit(1)
"

    log_info "数据库初始化完成"
}

# 重置数据库（危险操作）
reset_database() {
    log_warn "即将重置数据库，所有数据将被删除！"
    read -p "确认重置? (yes/no): " confirm

    if [ "$confirm" != "yes" ]; then
        log_info "取消重置操作"
        exit 0
    fi

    log_info "开始重置数据库..."

    python -c "
import sys
sys.path.append('.')
from src.database.database import engine
from src.database.models import Base
from sqlalchemy import inspect

try:
    # 删除所有表
    Base.metadata.drop_all(bind=engine)
    print('所有表已删除')

    # 重新创建表
    Base.metadata.create_all(bind=engine)
    print('数据库表已重新创建')

    print('数据库重置完成')

except Exception as e:
    print(f'数据库重置失败: {e}')
    sys.exit(1)
"

    log_info "数据库重置完成，请运行初始化脚本创建默认账户"
}

# 升级数据库
upgrade_database() {
    log_info "检查数据库版本..."

    python -c "
import sys
sys.path.append('.')
from src.database.database import engine
from src.database.models import Base
from sqlalchemy import inspect

try:
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print('当前数据库表:')
    for table in tables:
        print(f'  - {table}')

    print('数据库版本检查完成')

except Exception as e:
    print(f'数据库版本检查失败: {e}')
    sys.exit(1)
"

    log_info "数据库版本检查完成"
}

# 显示帮助
show_help() {
    echo "阿尔兹海默症诊断系统 - 数据库管理脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  init     初始化数据库"
    echo "  reset    重置数据库（危险，会删除所有数据）"
    echo "  upgrade  检查数据库版本"
    echo "  help     显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 init"
    echo "  $0 upgrade"
}

# 主函数
case "${1:-init}" in
    init)
        init_database
        ;;
    reset)
        reset_database
        ;;
    upgrade)
        upgrade_database
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "未知命令: $1"
        show_help
        exit 1
        ;;
esac