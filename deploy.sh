#!/bin/bash

# 阿尔兹海默症诊断系统 - 部署脚本 (Shell)
# 适用于Linux服务器（Ubuntu/CentOS）

# 配置参数
SERVER_IP="115.29.202.86"
PROJECT_DIR="/opt/alzheimer-diagnostic-system"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印标题
echo "========================================"
echo "阿尔兹海默症诊断系统 - 部署脚本"
echo "========================================"
echo ""

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   print_error "此脚本需要以root用户运行"
   print_info "请使用: sudo bash deploy.sh"
   exit 1
fi

print_info "开始部署阿尔兹海默症诊断系统..."
echo ""

# 检测操作系统
print_info "[1/7] 检测操作系统..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
    print_success "检测到操作系统: $NAME $VERSION"
else
    print_error "无法检测操作系统"
    exit 1
fi

echo ""

# 更新系统
print_info "[2/7] 更新系统软件包..."
if [ "$OS" == "ubuntu" ] || [ "$OS" == "debian" ]; then
    apt update && apt upgrade -y
elif [ "$OS" == "centos" ] || [ "$OS" == "rhel" ]; then
    yum update -y
fi
print_success "系统更新完成"

echo ""

# 安装必要软件
print_info "[3/7] 安装必要软件..."
if [ "$OS" == "ubuntu" ] || [ "$OS" == "debian" ]; then
    apt install -y curl wget git unzip apt-transport-https ca-certificates gnupg lsb-release
elif [ "$OS" == "centos" ] || [ "$OS" == "rhel" ]; then
    yum install -y curl wget git unzip
fi
print_success "必要软件安装完成"

echo ""

# 安装Docker
print_info "[4/7] 安装Docker..."
if ! command -v docker &> /dev/null; then
    if [ "$OS" == "ubuntu" ] || [ "$OS" == "debian" ]; then
        # 添加Docker GPG key
        mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

        # 添加Docker仓库
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

        # 安装Docker
        apt update
        apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    elif [ "$OS" == "centos" ] || [ "$OS" == "rhel" ]; then
        yum install -y yum-utils
        yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    fi

    # 启动Docker
    systemctl start docker
    systemctl enable docker
    print_success "Docker安装完成"
else
    print_success "Docker已安装"
fi

echo ""

# 安装Docker Compose（独立版本）
print_info "[5/7] 安装Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose安装完成"
else
    print_success "Docker Compose已安装"
fi

echo ""

# 创建项目目录
print_info "[6/7] 创建项目目录..."
if [ -d "$PROJECT_DIR" ]; then
    print_warning "项目目录已存在，备份并重新创建..."
    mv "$PROJECT_DIR" "${PROJECT_DIR}_backup_$(date +%Y%m%d%H%M%S)"
fi

mkdir -p "$PROJECT_DIR"
print_success "项目目录已创建: $PROJECT_DIR"

echo ""

# 复制项目文件
print_info "[7/7] 复制项目文件..."
print_warning "请将项目文件复制到: $PROJECT_DIR"
print_info "或者使用以下命令克隆仓库:"
echo "  git clone <your-repo-url> $PROJECT_DIR"
echo ""

# 配置环境变量
print_info "配置环境变量..."
if [ -f "$PROJECT_DIR/.deployment.env.example" ]; then
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        cp "$PROJECT_DIR/.deployment.env.example" "$PROJECT_DIR/.env"
        sed -i 's/your-super-secret-key-change-this-in-production/alzheimer-secret-key-2024/g' "$PROJECT_DIR/.env"
        print_success "环境变量已配置"
    else
        print_success "环境变量已存在"
    fi
fi

echo ""

# 构建Docker镜像
print_info "构建Docker镜像（这可能需要几分钟）..."
cd "$PROJECT_DIR"
docker build -t alzheimer-diagnostic-system:latest .

if [ $? -eq 0 ]; then
    print_success "Docker镜像构建完成"
else
    print_error "Docker镜像构建失败"
    exit 1
fi

echo ""

# 启动容器
print_info "启动容器..."
docker run -d \
    --name alzheimer-app \
    -p 8888:8888 \
    -p 80:80 \
    -v "$PROJECT_DIR/data:/app/data" \
    -v "$PROJECT_DIR/logs:/app/logs" \
    -v "$PROJECT_DIR/reports:/app/reports" \
    -v "$PROJECT_DIR/uploaded_img:/app/uploaded_img" \
    --restart unless-stopped \
    alzheimer-diagnostic-system:latest

if [ $? -eq 0 ]; then
    print_success "容器启动成功"
else
    print_error "容器启动失败"
    exit 1
fi

echo ""

# 检查容器状态
print_info "检查容器状态..."
sleep 2
docker ps | grep alzheimer-app

echo ""
echo "========================================"
echo "部署完成！"
echo "========================================"
echo ""
echo -e "${GREEN}系统访问地址:${NC}"
echo "  本地访问: http://localhost:8888"
echo "  外部访问: http://$SERVER_IP"
echo ""
echo -e "${GREEN}API文档地址:${NC}"
echo "  http://$SERVER_IP/docs"
echo ""
echo -e "${GREEN}健康检查地址:${NC}"
echo "  http://$SERVER_IP/health"
echo ""
echo -e "${YELLOW}重要提醒:${NC}"
echo "  1. 请在阿里云安全组中开放80和8888端口"
echo "  2. 检查容器运行状态: docker ps"
echo "  3. 查看容器日志: docker logs alzheimer-app"
echo "  4. 停止容器: docker stop alzheimer-app"
echo "  5. 启动容器: docker start alzheimer-app"
echo ""
echo -e "${BLUE}后续步骤:${NC}"
echo "  1. 访问 http://$SERVER_IP 验证系统"
echo "  2. 使用示例数据进行测试"
echo "  3. 配置域名（可选）"
echo "  4. 配置SSL证书启用HTTPS（可选）"
echo ""