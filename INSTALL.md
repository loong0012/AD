# 阿尔兹海默症诊断系统 - 安装说明

## 1. 系统概述

**基于深度学习的多模态阿尔兹海默症分类与进展预测系统**

这是一个现代化的Web界面系统，采用FastAPI框架构建，提供阿尔兹海默症的早期诊断和进展预测功能。系统支持多模态数据融合分析，包括影像数据、临床数据、分子数据和生活方式数据。

## 2. 系统要求

### 2.1 硬件要求
- **CPU**：至少4核处理器
- **内存**：8GB+ RAM（推荐16GB+）
- **存储**：50GB+ 可用磁盘空间
- **GPU**：可选，用于加速模型推理（推荐NVIDIA GPU）

### 2.2 软件要求
- **操作系统**：
  - Windows 10/11
  - Ubuntu 20.04+ / Debian 10+
  - macOS 12+
- **Python**：3.9+（推荐3.11）
- **Docker**：20.10+（用于容器化部署）
- **CUDA**：11.8+（如果使用GPU加速）

## 3. 安装方法

### 3.1 方法一：直接安装（开发环境）

#### 步骤1：克隆项目
```bash
# 克隆项目仓库
git clone <repository-url>
cd alzheimer-diagnostic-system
```

#### 步骤2：创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 步骤3：安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤4：配置环境变量（可选）
```bash
# 复制环境变量示例文件
cp .deployment.env.example .env

# 编辑.env文件设置必要的配置
# 例如数据库连接、密钥等
```

#### 步骤5：启动系统
```bash
# 方法1：使用启动脚本
python run.py

# 方法2：直接使用uvicorn
uvicorn src.app:app --host 0.0.0.0 --port 8889 --reload
```

### 3.2 方法二：Docker容器化部署（推荐生产环境）

#### 步骤1：安装Docker
- **Windows**：下载并安装Docker Desktop
- **Linux**：按照官方文档安装Docker
- **macOS**：下载并安装Docker Desktop

#### 步骤2：构建Docker镜像
```bash
# 构建镜像
docker build -t alzheimer-diagnostic-system:latest .

# 或使用部署脚本
./deploy.sh build
```

#### 步骤3：配置环境变量
```bash
# 复制环境变量示例文件
cp .deployment.env.example .env

# 编辑.env文件设置必要的配置
```

#### 步骤4：启动容器
```bash
# 开发环境
docker-compose up -d app

# 生产环境（包含Nginx反向代理）
docker-compose -f docker-compose.production.yml up -d
```

### 3.3 方法三：Kubernetes部署（大规模生产环境）

#### 步骤1：准备Kubernetes集群
- 可以使用Minikube（本地测试）
- 或使用云服务商提供的Kubernetes服务

#### 步骤2：部署应用
```bash
# 部署到Kubernetes
kubectl apply -f deployment/k8s/deployment.yaml

# 检查部署状态
kubectl get pods -l app=alzheimer
```

## 4. 配置说明

### 4.1 环境变量配置

在`.env`文件中配置以下变量：

| 变量名 | 默认值 | 说明 |
|-------|-------|------|
| DATABASE_URL | sqlite:///./alzheimer.db | 数据库连接URL |
| SECRET_KEY | your-super-secret-key-change-this-in-production | JWT密钥 |
| DEBUG | false | 调试模式 |
| LOG_LEVEL | INFO | 日志级别 |
| WORKERS | 4 | 工作进程数 |
| TIMEOUT | 120 | 请求超时时间（秒） |

### 4.2 目录结构配置

确保以下目录存在且具有正确的权限：

- `uploaded_img/`：上传的图像文件
- `reports/`：生成的PDF报告
- `results/`：诊断结果
- `logs/`：日志文件
- `temp/`：临时文件

## 5. 启动和访问

### 5.1 访问地址

- **开发环境**：http://localhost:8889
- **生产环境（Docker）**：http://localhost
- **Kubernetes环境**：根据集群配置的Ingress地址

### 5.2 初始登录

- **用户名**：admin
- **密码**：admin

首次登录后建议修改默认密码。

### 5.3 系统功能访问

- **Web界面**：http://localhost:8889
- **API文档**：http://localhost:8889/docs
- **健康检查**：http://localhost:8889/health

## 6. 数据初始化

### 6.1 初始化数据库

```bash
# 使用脚本初始化数据库
bash scripts/init_db.sh

# 或手动初始化
python -m src.database.init_db
```

### 6.2 导入示例数据

系统默认包含演示数据，位于`demodata/`目录。

## 7. 故障排除

### 7.1 常见问题

| 问题 | 解决方案 |
|------|---------|
| 端口8889被占用 | 修改启动脚本中的端口号，或停止占用该端口的进程 |
| 依赖安装失败 | 确保Python版本正确，尝试使用`--no-cache-dir`选项 |
| Docker构建失败 | 清理Docker缓存：`docker builder prune`，然后重新构建 |
| 数据库连接失败 | 检查数据库文件权限，确保目录可写 |
| 上传文件失败 | 检查`uploaded_img`目录权限，确保可写 |

### 7.2 日志查看

系统日志存储在`logs/`目录中：

```bash
# 查看最新日志
tail -f logs/alzheimer-diagnostic_*.log

# 查看Docker容器日志
docker-compose logs -f app
```

## 8. 系统更新

### 8.1 代码更新

```bash
# 拉取最新代码
git pull

# 重新安装依赖
pip install -r requirements.txt

# 重启服务
python run.py
```

### 8.2 Docker镜像更新

```bash
# 停止并移除旧容器
docker-compose down

# 重新构建镜像
docker build -t alzheimer-diagnostic-system:latest .

# 启动新容器
docker-compose up -d
```

## 9. 系统维护

### 9.1 数据备份

```bash
# 执行备份
./scripts/backup.sh

# 查看备份状态
./scripts/backup.sh --status
```

### 9.2 系统监控

- **资源使用**：`docker stats`（Docker部署）
- **服务状态**：`curl http://localhost:8889/health`
- **日志监控**：配置日志管理工具（如ELK Stack）

## 10. 技术支持

- 📧 邮箱：1478211871@qq.com
- 📞 电话：17864454060

## 11. 许可证

本项目采用开源许可证。

---

**注意**：本系统仅供研究和辅助诊断使用，不能替代专业医生的诊断和治疗建议。在使用系统结果时，请结合临床实际情况进行综合判断。