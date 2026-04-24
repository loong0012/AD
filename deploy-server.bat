@echo off
chcp 65001 > nul
color 0B

echo ========================================
echo 阿尔兹海默症诊断系统 - 部署脚本
echo ========================================
echo.

echo [1/6] 检查Docker环境...
docker --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker未安装，正在安装Docker Desktop...
    powershell -Command "Start-Process -FilePath 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -Verb RunAs -Wait"
) else (
    echo Docker已安装
)

echo.
echo [2/6] 启动Docker服务...
net start com.docker.service > nul 2>&1
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo 正在启动Docker Desktop，请等待...
    powershell -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"
    echo 等待Docker启动...
    timeout /t 30 /nobreak
)

echo.
echo [3/6] 创建项目目录...
if exist "C:\AlzheimerDiagnosticSystem" (
    rmdir /s /q "C:\AlzheimerDiagnosticSystem"
)
mkdir "C:\AlzheimerDiagnosticSystem"
echo 项目目录已创建: C:\AlzheimerDiagnosticSystem

echo.
echo [4/6] 复制项目文件...
echo 请将项目文件复制到: C:\AlzheimerDiagnosticSystem
echo 或者使用git克隆仓库到该目录
echo.
echo 如果已经复制了项目文件，按任意键继续...
pause > nul

echo.
echo [5/6] 配置环境变量...
if not exist "C:\AlzheimerDiagnosticSystem\.env" (
    if exist "C:\AlzheimerDiagnosticSystem\.deployment.env.example" (
        copy "C:\AlzheimerDiagnosticSystem\.deployment.env.example" "C:\AlzheimerDiagnosticSystem\.env"
        powershell -Command "(Get-Content 'C:\AlzheimerDiagnosticSystem\.env') -replace 'your-super-secret-key-change-this-in-production', 'alzheimer-secret-key-2024' | Set-Content 'C:\AlzheimerDiagnosticSystem\.env'"
    )
)
echo 环境变量已配置

echo.
echo [6/6] 构建并启动容器...
cd /d "C:\AlzheimerDiagnosticSystem"

echo 正在构建Docker镜像（这可能需要几分钟）...
docker build -t alzheimer-diagnostic-system:latest .

echo.
echo 正在启动容器...
docker run -d -p 8888:8888 -p 80:80 --name alzheimer-app alzheimer-diagnostic-system:latest

echo.
echo ========================================
echo 部署完成！
echo ========================================
echo.
echo 系统访问地址: http://localhost:8888
echo API文档地址: http://localhost:8888/docs
echo 健康检查地址: http://localhost:8888/health
echo.
echo 外部访问地址: http://115.29.202.86
echo.
echo 重要提醒：
echo 1. 请在阿里云安全组中开放80和8888端口
echo 2. 检查容器运行状态: docker ps
echo 3. 查看容器日志: docker logs alzheimer-app
echo.
pause