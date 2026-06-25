# AD-CPredSys - 阿尔兹海默症诊断系统

基于深度学习的阿尔兹海默症分类与进展预测系统，整合多模态医疗数据，提供精准的早期筛查、风险评估和进展预测。

## 功能特性

- **多模态数据融合**：整合MRI影像、临床数据、生活方式、分子标志物
- **AI辅助诊断**：深度学习模型自动分类（CN/EMCI/LMCI/AD）
- **12个月进展预测**：基于当前指标的月度风险变化趋势
- **脑区热力图**：可视化脑区风险分布
- **PDF报告生成**：一键生成专业诊断报告
- **RESTful API**：完整的API接口，支持系统集成

## 快速开始

### 环境要求

- Python 3.11+
- pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/alzheimer-diagnostic-system.git
cd alzheimer-diagnostic-system

# 安装依赖
pip install -r requirements.txt
```

### 启动

```bash
# 方式一：使用启动脚本
python run.py

# 方式二：直接启动
python -m src.app
```

启动后访问：**http://localhost:8888**

### 健康检查

```bash
curl http://localhost:8888/health
```

## Docker 部署

```bash
# 开发环境
docker-compose up -d

# 生产环境（含 Nginx + Redis + PostgreSQL）
docker-compose -f docker-compose.production.yml --profile with-nginx --profile with-redis --profile with-postgres up -d
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 前端页面 |
| GET | `/health` | 健康检查 |
| GET | `/api/demo?category=CN` | 演示分析 |
| POST | `/api/analyze` | 文件分析 |
| POST | `/api/upload` | 文件上传 |
| POST | `/api/diagnose` | 诊断API |
| POST | `/api/generate-pdf` | 生成PDF报告 |
| GET | `/api/reports` | 报告列表 |
| GET | `/api/stats` | 系统统计 |
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/register` | 用户注册 |

## 项目结构

```
├── src/
│   ├── app.py                    # FastAPI 主应用
│   ├── Alzheimer_diagnostic_system.py  # 核心系统类
│   ├── diagnosis/engine.py       # 诊断引擎
│   ├── data/processor.py         # 数据处理器
│   ├── report/generator.py       # 报告生成器
│   ├── api/handler.py            # API处理器
│   ├── database/                 # 数据库模块
│   ├── models/model.py           # 深度学习模型
│   ├── config/config.py          # 配置文件
│   └── utils/                    # 工具模块
├── static/                       # 前端静态文件
├── deployment/                   # 部署配置
├── .github/workflows/ci.yml      # CI/CD 流水线
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 技术栈

- **后端**：FastAPI + Uvicorn + SQLAlchemy
- **深度学习**：PyTorch
- **前端**：HTML5 + CSS3 + JavaScript
- **数据库**：SQLite（开发）/ PostgreSQL（生产）
- **部署**：Docker + Nginx + Gunicorn

## 许可证

本项目仅供学习和研究使用。