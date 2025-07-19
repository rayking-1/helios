# Dockerfile

# ---- Builder Stage ----
# 使用官方 Python 镜像作为构建环境
FROM python:3.11-slim-bullseye as builder

# 设置工作目录
WORKDIR /usr/src/app

# 设置环境变量，防止 Python 写入 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
# 确保 Python 输出是无缓冲的
ENV PYTHONUNBUFFERED 1

# 安装构建依赖（如果需要编译某些包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements-prod.txt .

# 创建并激活虚拟环境，并将依赖安装其中
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements-prod.txt


# ---- Final Stage ----
# 使用一个更小、更安全的基础镜像
FROM python:3.11-slim-bullseye

# 设置工作目录
WORKDIR /app

# 从 builder 阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 创建一个非 root 用户，并切换到该用户，增强安全性
RUN useradd --create-home appuser
RUN mkdir -p /app/static && chown -R appuser:appuser /app

# 复制应用代码和静态文件
COPY --chown=appuser:appuser helios /app/helios
COPY --chown=appuser:appuser static /app/static
COPY --chown=appuser:appuser alembic.ini /app/
COPY --chown=appuser:appuser migrations /app/migrations

# 切换到非root用户
USER appuser

# 设置环境变量，让应用使用虚拟环境中的 Python 和库
ENV PATH="/opt/venv/bin:$PATH"
ENV ENVIRONMENT="production" # 标识为生产环境
# 将 SECRET_KEY 暴露为环境变量，以便在运行时注入
ENV SECRET_KEY="change_this_in_production"
# 数据库连接字符串也应在运行时注入
ENV DATABASE_URL="postgresql://postgres:postgres@db:5432/helios"

# 暴露应用监听的端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 容器启动时运行的命令
# 使用 Gunicorn 启动 4 个 Uvicorn worker 进程
# 监听所有网络接口的 8000 端口
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "helios.main_api:app", "-b", "0.0.0.0:8000"] 