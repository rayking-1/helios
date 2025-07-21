# PowerShell 脚本: 创建 helios_adaptive_planner 项目目录结构
# 用法: .\create_structure.ps1

# 项目根目录名称
$projectRoot = "helios_adaptive_planner"

# 检查项目根目录是否已存在
if (Test-Path $projectRoot) {
    Write-Host "项目目录 '$projectRoot' 已存在。是否继续（这将保留现有文件）？(Y/N)" -ForegroundColor Yellow
    $continue = Read-Host
    if ($continue -ne "Y" -and $continue -ne "y") {
        Write-Host "操作已取消。" -ForegroundColor Red
        exit
    }
}
else {
    # 创建项目根目录
    New-Item -Path $projectRoot -ItemType Directory | Out-Null
    Write-Host "创建项目根目录: $projectRoot" -ForegroundColor Green
}

# 定义目录结构
$directories = @(
    # 后端结构
    "backend/agents",
    "backend/tools",
    "backend/tests",
    "backend/config",
    
    # 前端结构
    "frontend/src/api",
    "frontend/src/components",
    "frontend/src/hooks",
    "frontend/src/store",
    "frontend/src/pages",
    "frontend/src/types",
    "frontend/public"
)

# 创建目录
foreach ($dir in $directories) {
    $fullPath = Join-Path -Path $projectRoot -ChildPath $dir
    
    if (Test-Path $fullPath) {
        Write-Host "目录已存在: $dir" -ForegroundColor Yellow
    }
    else {
        New-Item -Path $fullPath -ItemType Directory | Out-Null
        Write-Host "创建目录: $dir" -ForegroundColor Green
    }
}

# 创建基础文件
$files = @{
    # 配置文件
    "$projectRoot/.env.example" = "# 环境变量示例文件
# 复制此文件为 .env 并填入你的实际值

# LLM API密钥
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
ZHIPUAI_API_KEY=your_zhipuai_api_key_here

# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# 应用配置
LOG_LEVEL=INFO
"
    
    # 后端主要文件
    "$projectRoot/backend/requirements.txt" = "pyautogen
fastapi
uvicorn
python-dotenv
pytest
httpx
aiohttp
"
    
    "$projectRoot/backend/main.py" = "# backend/main.py
import os
from fastapi import FastAPI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(
    title=\"Helios Adaptive Planning API\",
    description=\"AI-powered adaptive planning system API\",
    version=\"1.0.0\",
)

@app.get(\"/\")
async def root():
    \"\"\"健康检查端点\"\"\"
    return {\"status\": \"ok\", \"message\": \"Helios Adaptive Planning API is running\"}

if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(\"main:app\", host=\"0.0.0.0\", port=8000, reload=True)
"
    
    # Git 忽略文件
    "$projectRoot/.gitignore" = "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log
yarn-error.log
yarn-debug.log
.pnpm-debug.log

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build
/build
/dist

# Testing
/coverage
.pytest_cache/
htmlcov/
.coverage
.coverage.*
"
    
    # README
    "$projectRoot/README.md" = "# Helios Adaptive Planner

基于AutoGen (ag2) 框架的自适应规划系统，使用多智能体协作构建高质量、可调整的计划。

## 项目概览

Helios Adaptive Planner 是一个智能计划生成系统，通过多个专业智能体的协作，将用户的模糊目标转化为结构化、可执行的计划，并根据反馈实时调整。

## 快速开始

### 环境准备

1. 创建并激活虚拟环境:
```bash
python -m venv venv
.\\venv\\Scripts\\activate  # Windows
source venv/bin/activate    # Linux/macOS
```

2. 安装依赖:
```bash
cd backend
pip install -r requirements.txt
```

3. 配置环境变量:
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的API密钥
```

4. 启动服务:
```bash
python main.py
```

## 开发指南

详细的开发指南请参考 [DEVELOPMENT.md](DEVELOPMENT.md)
"
    
    # 前端主要文件
    "$projectRoot/frontend/package.json" = "{
  \"name\": \"helios-frontend\",
  \"private\": true,
  \"version\": \"1.0.0\",
  \"type\": \"module\",
  \"scripts\": {
    \"dev\": \"vite\",
    \"build\": \"tsc && vite build\",
    \"lint\": \"eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0\",
    \"preview\": \"vite preview\"
  },
  \"dependencies\": {
    \"axios\": \"^1.6.0\",
    \"react\": \"^18.2.0\",
    \"react-dom\": \"^18.2.0\",
    \"react-router-dom\": \"^6.18.0\",
    \"zustand\": \"^4.4.6\"
  },
  \"devDependencies\": {
    \"@types/react\": \"^18.2.15\",
    \"@types/react-dom\": \"^18.2.7\",
    \"@typescript-eslint/eslint-plugin\": \"^6.0.0\",
    \"@typescript-eslint/parser\": \"^6.0.0\",
    \"@vitejs/plugin-react\": \"^4.0.3\",
    \"eslint\": \"^8.45.0\",
    \"eslint-plugin-react-hooks\": \"^4.6.0\",
    \"eslint-plugin-react-refresh\": \"^0.4.3\",
    \"typescript\": \"^5.0.2\",
    \"vite\": \"^4.4.5\"
  }
}
"
    "$projectRoot/frontend/index.html" = "<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <link rel=\"icon\" type=\"image/svg+xml\" href=\"/vite.svg\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Helios Adaptive Planner</title>
  </head>
  <body>
    <div id=\"root\"></div>
    <script type=\"module\" src=\"/src/main.tsx\"></script>
  </body>
</html>
"
    
    # 开发环境配置
    "$projectRoot/.vscode/settings.json" = "{
  \"editor.formatOnSave\": true,
  \"editor.codeActionsOnSave\": {
    \"source.fixAll.eslint\": true
  },
  \"python.linting.enabled\": true,
  \"python.linting.pylintEnabled\": true,
  \"python.formatting.provider\": \"autopep8\",
  \"[python]\": {
    \"editor.formatOnSave\": true
  },
  \"[typescript]\": {
    \"editor.defaultFormatter\": \"esbenp.prettier-vscode\"
  },
  \"[typescriptreact]\": {
    \"editor.defaultFormatter\": \"esbenp.prettier-vscode\"
  }
}
"
}

# 创建文件
foreach ($file in $files.Keys) {
    if (Test-Path $file) {
        Write-Host "文件已存在: $file" -ForegroundColor Yellow
    }
    else {
        $content = $files[$file]
        Set-Content -Path $file -Value $content
        Write-Host "创建文件: $file" -ForegroundColor Green
    }
}

# 创建Docker文件
$dockerfilePath = "$projectRoot/backend/Dockerfile"
if (Test-Path $dockerfilePath) {
    Write-Host "Dockerfile 已存在: $dockerfilePath" -ForegroundColor Yellow
}
else {
    $dockerfileContent = @"
# 多阶段构建: 构建阶段
FROM python:3.10-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# 安装Python依赖
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# 多阶段构建: 最终镜像
FROM python:3.10-slim

# 创建非特权用户
RUN addgroup --system app && \
    adduser --system --group app

WORKDIR /app

# 从构建阶段复制预构建的wheels
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# 复制应用代码
COPY . .

# 设置适当的权限
RUN chown -R app:app /app

# 切换到非特权用户
USER app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"@

    Set-Content -Path $dockerfilePath -Value $dockerfileContent
    Write-Host "创建Dockerfile: $dockerfilePath" -ForegroundColor Green
}

# 创建 Docker Compose 文件
$dockerComposePath = "$projectRoot/docker-compose.yml"
if (Test-Path $dockerComposePath) {
    Write-Host "docker-compose.yml 已存在: $dockerComposePath" -ForegroundColor Yellow
}
else {
    $dockerComposeContent = @"
version: '3.8'

services:
  # 后端API服务
  backend:
    build: ./backend
    container_name: helios_backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: helios_frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:8000

  # 数据库服务
  db:
    image: postgres:14
    container_name: helios_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=helios
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"@

    Set-Content -Path $dockerComposePath -Value $dockerComposeContent
    Write-Host "创建 docker-compose.yml: $dockerComposePath" -ForegroundColor Green
}

# 创建前端Dockerfile
$frontendDockerfilePath = "$projectRoot/frontend/Dockerfile"
if (Test-Path $frontendDockerfilePath) {
    Write-Host "Frontend Dockerfile 已存在: $frontendDockerfilePath" -ForegroundColor Yellow
}
else {
    $frontendDockerfileContent = @"
# 构建阶段
FROM node:18-alpine as build

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm install

# 复制源代码并构建
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 从构建阶段复制构建输出到Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
"@

    Set-Content -Path $frontendDockerfilePath -Value $frontendDockerfileContent
    Write-Host "创建前端Dockerfile: $frontendDockerfilePath" -ForegroundColor Green
}

# 总结
Write-Host "`n项目结构创建完成!" -ForegroundColor Green
Write-Host "`n下一步建议:" -ForegroundColor Cyan
Write-Host "1. 进入项目目录: cd $projectRoot" -ForegroundColor Cyan
Write-Host "2. 初始化Git仓库: git init" -ForegroundColor Cyan
Write-Host "3. 创建Python虚拟环境: python -m venv venv" -ForegroundColor Cyan
Write-Host "4. 激活虚拟环境: .\\venv\\Scripts\\activate" -ForegroundColor Cyan
Write-Host "5. 安装后端依赖: cd backend && pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "6. 安装前端依赖: cd ../frontend && npm install" -ForegroundColor Cyan
Write-Host "7. 复制环境变量模板: cp .env.example .env，然后填入API密钥" -ForegroundColor Cyan 