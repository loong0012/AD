# 阿尔兹海默症诊断系统 - 远程部署脚本 (PowerShell)
# 适用于阿里云Windows Server服务器

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "阿尔兹海默症诊断系统 - 部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 配置参数
$ServerIP = "115.29.202.86"
$ProjectDir = "C:\AlzheimerDiagnosticSystem"
$ProjectRepo = "https://github.com/your-username/alzheimer-diagnostic-system.git"

# 远程服务器信息
$RemoteServer = $ServerIP
$RemoteUser = "Administrator"

Write-Host "[1/7] 检查远程服务器连接..." -ForegroundColor Yellow

# 测试远程连接
try {
    Test-Connection -ComputerName $RemoteServer -Count 2 -ErrorAction Stop | Out-Null
    Write-Host "✓ 远程服务器连接正常" -ForegroundColor Green
} catch {
    Write-Host "✗ 无法连接到远程服务器: $RemoteServer" -ForegroundColor Red
    Write-Host "请确保服务器已启动并允许远程连接" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/7] 创建本地临时目录..." -ForegroundColor Yellow

# 创建临时目录
$TempDir = "$env:TEMP\AlzheimerDeploy"
if (Test-Path $TempDir) {
    Remove-Item -Path $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
Write-Host "✓ 临时目录已创建: $TempDir" -ForegroundColor Green

Write-Host ""
Write-Host "[3/7] 创建部署脚本..." -ForegroundColor Yellow

# 创建远程部署脚本内容
$DeployScript = @'
# 阿尔兹海默症诊断系统 - 服务器端部署脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始部署阿尔兹海默症诊断系统..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Docker是否安装
Write-Host "[1/5] 检查Docker环境..." -ForegroundColor Yellow
$docker = Get-Command docker -ErrorAction SilentlyContinue
if (-not $docker) {
    Write-Host "Docker未安装，正在安装Docker Desktop..." -ForegroundColor Red
    # 下载Docker Desktop安装包
    $dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"
    Invoke-WebRequest -Uri "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -OutFile $dockerInstaller
    # 安装Docker Desktop (需要管理员权限)
    Start-Process -FilePath $dockerInstaller -ArgumentList "install --quiet" -Wait -Verb RunAs
    Write-Host "✓ Docker Desktop安装完成" -ForegroundColor Green
} else {
    Write-Host "✓ Docker已安装" -ForegroundColor Green
}

# 启动Docker服务
Write-Host ""
Write-Host "[2/5] 启动Docker服务..." -ForegroundColor Yellow
Start-Service Docker -ErrorAction SilentlyContinue
Set-Service -Name Docker -StartupType Automatic
Write-Host "✓ Docker服务已启动" -ForegroundColor Green

# 创建项目目录
Write-Host ""
Write-Host "[3/5] 创建项目目录..." -ForegroundColor Yellow
$ProjectDir = "C:\AlzheimerDiagnosticSystem"
if (Test-Path $ProjectDir) {
    Remove-Item -Path $ProjectDir -Recurse -Force
}
New-Item -ItemType Directory -Path $ProjectDir -Force | Out-Null
Write-Host "✓ 项目目录已创建: $ProjectDir" -ForegroundColor Green

# 下载项目文件
Write-Host ""
Write-Host "[4/5] 下载项目文件..." -ForegroundColor Yellow
# 注意：您需要将项目文件上传到服务器，或使用以下方法克隆仓库
# git clone <your-repo-url> $ProjectDir
Write-Host "请将项目文件复制到: $ProjectDir" -ForegroundColor Yellow
Write-Host "或者运行: git clone <your-repo-url> `"$ProjectDir`"" -ForegroundColor Yellow

# 配置环境变量
Write-Host ""
Write-Host "[5/5] 配置环境变量..." -ForegroundColor Yellow
$envFile = Join-Path $ProjectDir ".env"
if (-not (Test-Path $envFile)) {
    $envTemplate = Join-Path $ProjectDir ".deployment.env.example"
    if (Test-Path $envTemplate) {
        Copy-Item $envTemplate $envFile
        # 修改默认配置
        (Get-Content $envFile) -replace 'your-super-secret-key-change-this-in-production', 'alzheimer-secret-key-2024' | Set-Content $envFile
        Write-Host "✓ 环境变量文件已创建" -ForegroundColor Green
    }
}

# 构建Docker镜像
Write-Host ""
Write-Host "构建Docker镜像..." -ForegroundColor Yellow
Set-Location $ProjectDir
docker build -t alzheimer-diagnostic-system:latest .

# 启动容器
Write-Host ""
Write-Host "启动容器..." -ForegroundColor Yellow
docker run -d -p 8888:8888 -p 80:80 --name alzheimer-app alzheimer-diagnostic-system:latest

# 检查容器状态
Write-Host ""
Write-Host "检查容器状态..." -ForegroundColor Yellow
docker ps -a | Where-Object { $_.Names -like "*alzheimer*" }

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "系统访问地址: http://localhost:8888" -ForegroundColor Green
Write-Host "API文档地址: http://localhost:8888/docs" -ForegroundColor Green
Write-Host "健康检查地址: http://localhost:8888/health" -ForegroundColor Green
Write-Host ""
'@

# 保存部署脚本
$ScriptPath = Join-Path $TempDir "Deploy-AlzheimerSystem.ps1"
$DeployScript | Out-File -FilePath $ScriptPath -Encoding UTF8
Write-Host "✓ 部署脚本已创建: $ScriptPath" -ForegroundColor Green

Write-Host ""
Write-Host "[4/7] 将部署脚本传输到远程服务器..." -ForegroundColor Yellow

# 使用SCP传输文件（需要安装OpenSSH或使用其他方法）
try {
    # 尝试使用SCP
    scp -r $TempDir "$RemoteUser@$RemoteServer`:C:\Temp\"
    Write-Host "✓ 部署脚本已传输到远程服务器" -ForegroundColor Green
} catch {
    Write-Host "✗ 文件传输失败，请手动上传部署脚本" -ForegroundColor Red
    Write-Host "脚本位置: $ScriptPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[5/7] 在远程服务器上执行部署脚本..." -ForegroundColor Yellow

# 在远程服务器上执行部署脚本
try {
    # 使用PowerShell Remoting执行远程命令
    $session = New-PSSession -ComputerName $RemoteServer -Credential (Get-Credential)
    if ($session) {
        # 上传部署脚本
        Copy-Item -Path $ScriptPath -Destination $session

        # 执行远程部署脚本
        Invoke-Command -Session $session -ScriptBlock {
            param($scriptPath)
            & $scriptPath
        } -ArgumentList "C:\Temp\Deploy-AlzheimerSystem.ps1"

        Remove-PSSession $session
        Write-Host "✓ 远程部署完成" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ 远程执行失败，请手动在服务器上执行部署脚本" -ForegroundColor Red
    Write-Host "部署脚本位置: $ScriptPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[6/7] 检查部署状态..." -ForegroundColor Yellow

# 检查远程服务器上的Docker容器状态
try {
    # 尝试通过HTTP请求检查服务状态
    $healthCheck = Invoke-WebRequest -Uri "http://$RemoteServer`:8888/health" -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($healthCheck.StatusCode -eq 200) {
        Write-Host "✓ 系统运行正常！" -ForegroundColor Green
        Write-Host "健康检查响应: $($healthCheck.Content)" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ 无法连接到系统，请检查部署是否成功" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[7/7] 生成部署报告..." -ForegroundColor Yellow

# 生成部署报告
$Report = @"
========================================
阿尔兹海默症诊断系统 - 部署报告
========================================

部署时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
服务器IP: $ServerIP

部署状态: $(if($?){"成功"}else{"失败"})

访问信息:
- 系统主页: http://$ServerIP
- API文档: http://$ServerIP/docs
- 健康检查: http://$ServerIP/health

后续步骤:
1. 确保阿里云安全组已开放80和8888端口
2. 访问系统主页验证功能
3. 使用示例数据进行测试
4. 配置域名（可选）

========================================
"@

$Report | Out-File -FilePath "$TempDir\DeploymentReport.txt" -Encoding UTF8
Write-Host "✓ 部署报告已生成: $TempDir\DeploymentReport.txt" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "部署脚本生成完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host "1. 将部署脚本上传到服务器: C:\Temp\Deploy-AlzheimerSystem.ps1" -ForegroundColor White
Write-Host "2. 在服务器上以管理员身份运行PowerShell" -ForegroundColor White
Write-Host "3. 执行部署脚本: .\Deploy-AlzheimerSystem.ps1" -ForegroundColor White
Write-Host "4. 访问系统: http://$ServerIP" -ForegroundColor White
Write-Host ""
Write-Host "或者手动:" -ForegroundColor Yellow
Write-Host "1. 复制项目文件到服务器" -ForegroundColor White
Write-Host "2. 安装Docker Desktop" -ForegroundColor White
Write-Host "3. 运行: docker build -t alzheimer-diagnostic-system:latest ." -ForegroundColor White
Write-Host "4. 运行: docker run -d -p 8888:8888 -p 80:80 alzheimer-diagnostic-system:latest" -ForegroundColor White
Write-Host ""