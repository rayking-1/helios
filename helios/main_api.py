# helios/main_api.py

import uvicorn
import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from helios.services import logger
from helios.routers import tasks, websocket
from helios.database.migrations import create_tables
from helios.repositories.user_repository import UserRepository
from helios.database.session import SessionLocal
from helios.security import get_password_hash

# ----------------- 部署优化部分 -----------------
# 检查是否在容器或生产环境中，如果是，则跳过创建默认用户
# 生产环境的用户应通过安全途径创建
IS_IN_PRODUCTION = os.getenv("ENVIRONMENT") == "production"

def create_default_user():
    if IS_IN_PRODUCTION:
        return # 不在生产环境中创建默认用户
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        default_user = user_repo.find_by_username("default_user")
        if not default_user:
            hashed_password = get_password_hash("insecure_password")
            user_repo.create(
                username="default_user", 
                email="default@helios.dev", 
                hashed_password=hashed_password
            )
            logger.info("默认用户已创建")
        else:
            logger.info("默认用户已存在")
    finally:
        db.close()
# ----------------------------------------------------

app = FastAPI(
    title="Helios 智能规划系统 API",
    description="Helios 自适应规划项目的RESTful API服务",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    # 仅在需要时创建表。生产环境中可能使用 Alembic 等迁移工具管理
    logger.info("初始化数据库...")
    create_tables() 
    logger.info("创建默认用户...")
    create_default_user()
    logger.info("Helios API服务启动完成")

# 获取允许的CORS来源
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
logger.info(f"配置CORS允许的来源: {cors_origins}")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # 使用环境变量中定义的特定来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 static 目录，用于提供 CSS, JS 等文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含 API 路由
app.include_router(tasks.router, prefix="/api")
app.include_router(websocket.router)

# 将根路径指向 index.html
@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('static/index.html')

# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查端点，用于监控系统是否正常运行"""
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "development")}

# 直接运行此文件时启动服务器
if __name__ == "__main__":
    uvicorn.run("helios.main_api:app", host="0.0.0.0", port=8000, reload=True)
