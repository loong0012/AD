# 基于深度学习的阿尔兹海默分类与进展系统 - 部署文档

## 目录
- [快速开始](#快速开始)
- [部署架构](#部署架构)
- [环境要求](#环境要求)
- [配置说明](#配置说明)
- [部署步骤](#部署步骤)
- [运维管理](#运维管理)
- [故障排除](#故障排除)

## 快速开始

### 使用Docker部署（推荐）

```bash
# 1. 克隆项目
git clone <repository-url>
cd alzheimer-diagnostic-system

# 2. 复制并配置环境变量
cp .deployment.env.example .env
# 编辑 .env 文件，设置必要的配置

# 3. 启动服务
docker-compose up -d

# 4. 检查服务状态
docker-compose ps

# 5. 查看日志
docker-compose logs -f app
```

### 访问系统
- 开发环境: http://localhost:8888
- 生产环境: http://localhost:80

## 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户请求                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Nginx 反向代理                           │
│                   (端口 80/443)                             │
│  - SSL/TLS 终止                                             │
│  - 静态文件服务                                              │
│  - 请求路由                                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI 应用服务                          │
│                   (端口 8888)                              │
│  - 业务逻辑处理                                              │
│  - API响应                                                   │
│  - 图像处理                                                  │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  SQLite  │   │  Redis   │   │   OSS    │
        │ (本地DB) │   │ (缓存)   │   │ (存储)   │
        └──────────┘   └──────────┘   └──────────┘
```

## 环境要求

### 开发环境
- Python 3.11+
- Docker Desktop 4.0+
- 4GB RAM
- 10GB 磁盘空间

### 生产环境
- Linux服务器 (Ubuntu 20.04+)
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB RAM
- 50GB 磁盘空间
- PostgreSQL 15+ (可选)
- Redis 7+ (可选)

## 配置说明

### 环境变量

在 `.env` 文件中配置以下变量：

```bash
# 数据库配置
DATABASE_URL=sqlite:///./alzheimer.db
# 生产环境推荐使用PostgreSQL:
# DATABASE_URL=postgresql://user:password@postgres:5432/alzheimer_diagnostic

# 安全配置
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=false

# 服务器配置
WORKERS=4
TIMEOUT=120

# Redis配置（可选）
REDIS_URL=redis://redis:6379/0

# 备份配置
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
```

### 目录结构

```
项目目录/
├── deployment/              # 部署配置
│   ├── nginx.conf          # Nginx配置
│   ├── gunicorn_config.py  # Gunicorn配置
│   └── supervisord.conf    # Supervisor配置
├── scripts/                 # 运维脚本
│   ├── init_db.sh         # 数据库初始化
│   └── backup.sh          # 数据备份
├── data/                   # 应用数据
│   ├── clinical_data/     # 临床数据
│   └── ...
├── uploaded_img/           # 上传图片
├── results/                # 诊断结果
├── reports/                # 生成报告
├── logs/                   # 日志文件
├── backups/               # 备份文件
└── alzheimer.db          # SQLite数据库
```

## 部署步骤

### 方式一：Docker部署（推荐）

```bash
# 1. 构建镜像
./deploy.sh build

# 2. 启动服务
docker-compose up -d

# 3. 初始化数据库（首次）
./scripts/init_db.sh

# 4. 执行健康检查
curl http://localhost:8888/health
```

### 方式二：docker-compose独立部署

```bash
# 1. 构建镜像
docker build -t alzheimer-diagnostic-system:latest .

# 2. 启动服务
docker-compose -f docker-compose.production.yml up -d

# 3. 查看服务状态
docker-compose ps
```

### 方式三：Kubernetes部署

```bash
# 部署到Kubernetes
kubectl apply -f deployment/k8s/

# 检查部署状态
kubectl get pods -l app=alzheimer
```

## 运维管理

### 启动/停止服务

```bash
# 停止服务
docker-compose down

# 启动服务
docker-compose up -d

# 重启服务
docker-compose restart app
```

### 日志管理

```bash
# 查看应用日志
docker-compose logs -f app

# 查看Nginx日志
docker-compose logs -f nginx

# 查看所有日志
docker-compose logs -f

# 日志轮转（配置在docker-compose.yml中）
```

### 数据备份

```bash
# 执行备份
./scripts/backup.sh

# 查看备份状态
./scripts/backup.sh --status

# 清理过期备份
./scripts/backup.sh --cleanup

# 上传到远程存储
./scripts/backup.sh --upload
```

### 数据库管理

```bash
# 初始化数据库
./scripts/init_db.sh init

# 重置数据库（危险！）
./scripts/init_db.sh reset

# 检查数据库版本
./scripts/init_db.sh upgrade
```

### 服务监控

```bash
# 查看容器资源使用
docker stats

# 查看服务健康状态
curl http://localhost:8888/health

# 查看应用指标（需要启用监控）
curl http://localhost:9090/metrics
```

### 扩展服务

```bash
# 增加Worker数量
# 编辑 .env 文件，设置 WORKERS=8
docker-compose up -d --scale app=3
```

## 故障排除

### 服务无法启动

```bash
# 1. 检查端口占用
netstat -tulpn | grep 8888

# 2. 检查Docker日志
docker-compose logs app

# 3. 检查配置文件
docker-compose config
```

### 数据库连接失败

```bash
# 1. 检查数据库文件权限
ls -la alzheimer.db

# 2. 修复权限
chmod 644 alzheimer.db

# 3. 重新初始化数据库
./scripts/init_db.sh reset
```

### 镜像构建失败

```bash
# 1. 清理Docker缓存
docker builder prune

# 2. 重新构建
docker build --no-cache -t alzheimer-diagnostic-system:latest .

# 3. 检查依赖
pip install -r requirements.txt
```

### 性能问题

```bash
# 1. 检查资源使用
docker stats

# 2. 增加Worker数量
# 编辑 docker-compose.yml
# environment:
#   - WORKERS=8

# 3. 重启服务
docker-compose up -d --scale app=2
```

### 数据恢复

```bash
# 1. 停止服务
docker-compose down

# 2. 恢复数据库
cp backups/alzheimer.db.20240101_120000 alzheimer.db

# 3. 恢复上传文件
tar -xzf backups/uploads.20240101_120000.tar.gz

# 4. 重启服务
docker-compose up -d
```

## 安全建议

1. **修改默认密码**: 首次部署后立即修改管理员密码
2. **启用HTTPS**: 配置SSL证书
3. **限制API访问**: 配置IP白名单
4. **定期备份**: 配置自动备份任务
5. **监控告警**: 配置日志监控和告警机制

## 联系支持

如遇到问题，请查看：
- 日志文件: `logs/` 目录
- Docker日志: `docker-compose logs`
- GitHub Issues: 项目仓库