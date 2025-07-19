# Helios 容器化与部署指南

本文档提供了 Helios 应用的容器化与云部署完整指南，包括本地开发环境设置、Docker 镜像构建以及部署到 AWS 云平台的详细步骤。

## 目录

1. [项目结构](#项目结构)
2. [本地开发环境](#本地开发环境)
3. [Docker 镜像构建](#docker-镜像构建)
4. [数据库迁移](#数据库迁移)
5. [部署到 AWS](#部署到-aws)
6. [CI/CD 流程](#cicd-流程)
7. [安全最佳实践](#安全最佳实践)
8. [监控与日志](#监控与日志)
9. [故障排除](#故障排除)

## 项目结构

Helios 应用采用了清晰的分层架构，主要包括以下组件：

- **配置层**：负责加载和提供配置值，不依赖项目的其他部分
- **服务层**：负责创建和提供服务实例，如 logger 和 model_client
- **数据库层**：使用 SQLAlchemy ORM 实现数据模型和数据库操作
- **仓储层**：实现仓储模式，提供数据访问抽象
- **API 层**：使用 FastAPI 实现 RESTful API
- **前端**：简单的静态 HTML/CSS/JS 页面

## 本地开发环境

### 前提条件

- Python 3.11 或更高版本
- Docker 和 Docker Compose
- PostgreSQL（可选，如果不使用 Docker）

### 设置步骤

1. **克隆代码仓库**：

```bash
git clone https://github.com/yourusername/helios-adaptive-planner.git
cd helios-adaptive-planner
```

2. **创建并激活虚拟环境**：

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. **安装依赖**：

```bash
pip install -r requirements-prod.txt
```

4. **创建 .env 文件**：

```bash
# 开发环境配置
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/helios
SECRET_KEY=your_development_secret_key
ENVIRONMENT=development
```

5. **使用 Docker Compose 启动开发环境**：

```bash
docker-compose up -d
```

这将启动 PostgreSQL 数据库和 Adminer 数据库管理工具。

6. **运行数据库迁移**：

```bash
# 初始化迁移
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

7. **启动应用**：

```bash
uvicorn helios.main_api:app --reload
```

应用将在 http://localhost:8000 上运行，API 文档可在 http://localhost:8000/docs 访问。

## Docker 镜像构建

Helios 应用使用多阶段构建的 Dockerfile，以减小镜像体积并提高安全性。

### 手动构建镜像

```bash
# 构建镜像
docker build -t helios-app:latest .

# 运行容器
docker run -p 8000:8000 --env-file .env helios-app:latest
```

### 使用 Docker Compose 构建和运行

```bash
# 构建并启动所有服务
docker-compose up --build

# 仅重建应用服务
docker-compose up --build app
```

## 数据库迁移

Helios 应用使用 Alembic 进行数据库迁移管理。

### 创建新迁移

```bash
# 自动生成迁移脚本
alembic revision --autogenerate -m "描述变更内容"

# 手动创建迁移脚本
alembic revision -m "描述变更内容"
```

### 应用迁移

```bash
# 应用所有未应用的迁移
alembic upgrade head

# 应用到特定版本
alembic upgrade <revision_id>

# 回滚到特定版本
alembic downgrade <revision_id>
```

### 在容器中运行迁移

```bash
# 在应用容器中运行迁移
docker-compose exec app alembic upgrade head
```

## 部署到 AWS

Helios 应用可以部署到 AWS App Runner，这是一个全托管的容器化应用服务。

### 手动部署步骤

1. **创建 ECR 仓库**：

```bash
aws ecr create-repository --repository-name helios-app --region <your-region>
```

2. **登录 ECR**：

```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

3. **构建并推送镜像**：

```bash
docker build -t helios-app:latest .
docker tag helios-app:latest <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/helios-app:latest
docker push <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/helios-app:latest
```

4. **创建 RDS 数据库**：

通过 AWS 控制台或 AWS CLI 创建 PostgreSQL RDS 实例。

5. **在 Secrets Manager 中存储凭证**：

通过 AWS 控制台或 AWS CLI 创建密钥，存储数据库连接字符串和应用密钥。

6. **创建 App Runner 服务**：

通过 AWS 控制台或 AWS CLI 创建 App Runner 服务，使用上传的镜像和配置环境变量。

### 使用 GitHub Actions 自动部署

项目已配置 GitHub Actions 工作流，可以在代码推送到主分支时自动部署到 AWS App Runner。

1. **配置 GitHub 仓库密钥**：

在 GitHub 仓库的 Settings > Secrets 中添加以下密钥：

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

2. **推送代码触发部署**：

```bash
git add .
git commit -m "Update application"
git push origin main
```

## CI/CD 流程

Helios 应用使用 GitHub Actions 实现 CI/CD 流程，包括以下步骤：

1. **测试**：运行单元测试和集成测试
2. **构建**：构建 Docker 镜像
3. **推送**：将镜像推送到 GitHub Container Registry
4. **部署**：部署到 AWS App Runner

工作流配置文件位于 `.github/workflows/deploy.yml`。

## 安全最佳实践

Helios 应用实施了以下安全最佳实践：

1. **多阶段构建**：减小镜像体积，降低攻击面
2. **非 root 用户**：容器内使用非特权用户运行应用
3. **环境变量注入**：敏感信息通过环境变量注入，而不是硬编码
4. **密钥管理**：使用 AWS Secrets Manager 管理敏感信息
5. **HTTPS**：所有通信都通过 HTTPS 加密
6. **JWT 认证**：使用 JWT 进行用户认证和授权
7. **密码哈希**：使用 bcrypt 算法对密码进行哈希处理

## 监控与日志

### 应用日志

应用日志通过 stdout/stderr 输出，可以通过以下方式查看：

```bash
# 本地开发环境
docker-compose logs -f app

# AWS App Runner
aws apprunner describe-service --service-name helios-app
# 然后通过 AWS CloudWatch 查看日志
```

### 健康检查

应用提供了健康检查端点 `/health`，可用于监控应用状态。

### 性能监控

可以使用 AWS CloudWatch 监控 App Runner 服务的性能指标。

## 故障排除

### 常见问题

1. **数据库连接失败**：

   - 检查数据库连接字符串是否正确
   - 确认数据库服务是否运行
   - 验证网络连接和安全组设置

2. **容器启动失败**：

   - 检查 Docker 日志 `docker logs <container_id>`
   - 验证环境变量是否正确设置
   - 确认容器内的权限设置

3. **API 请求失败**：

   - 检查应用日志
   - 验证 API 路由和请求格式
   - 确认认证信息是否正确

### 获取支持

如果遇到无法解决的问题，请通过以下渠道获取支持：

- 提交 GitHub Issue
- 联系项目维护者 