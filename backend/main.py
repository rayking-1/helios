from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os
from typing import Optional
import uvicorn
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入路由和WebSocket
from routes import plan_routes, graphql_routes
from websockets import websocket_endpoint, manager, create_status_message

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建FastAPI应用实例
app = FastAPI(
    title="Helios Adaptive Planner API",
    description="智能自适应计划系统API",
    version="1.0.0",
)

# 配置CORS（跨源资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中，应该设置为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误，请联系管理员"}
    )

# 包含路由
app.include_router(plan_routes.router)
app.include_router(graphql_routes.router)  # 添加GraphQL路由

# 添加WebSocket端点
@app.websocket("/ws/{user_id}")
async def ws_endpoint(websocket: WebSocket, user_id: str):
    await websocket_endpoint(websocket, user_id)

# 添加简单的健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# 连接智能体团队
# 在实际实现中，这里会初始化AdaptivePlanTeam并设置事件处理程序
@app.on_event("startup")
async def startup_event():
    logger.info("应用启动，初始化智能体团队...")
    try:
        # 在这里初始化agent_team并连接WebSocket通知
        # 示例: connect_agent_team_events(on_plan_update, on_agent_message)
        pass
    except Exception as e:
        logger.error(f"初始化智能体团队时出错: {str(e)}")

# 在应用关闭时清理资源
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用关闭，清理资源...")
    # 在这里关闭数据库连接等资源

# 定义事件处理函数（在实际应用中将由AdaptivePlanTeam触发）
async def on_plan_update(user_id: str, plan_data: dict):
    """当计划更新时调用"""
    from websockets import create_plan_updated_message
    message = create_plan_updated_message(plan_data)
    await manager.broadcast_to_user(user_id, message)

async def on_agent_message(user_id: str, agent_name: str, content: str):
    """当智能体发送消息时调用"""
    from websockets import create_agent_message
    message = create_agent_message(agent_name, content)
    await manager.broadcast_to_user(user_id, message)

# 主入口
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
 