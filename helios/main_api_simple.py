# helios/main_api_simple.py

import uvicorn
import os
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Helios 智能规划系统 API",
    description="Helios 自适应规划项目的RESTful API服务",
    version="1.0.0",
)

# 获取允许的CORS来源
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 static 目录，用于提供 CSS, JS 等文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 将根路径指向 index.html
@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('static/index.html')

# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查端点，用于监控系统是否正常运行"""
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "development")}

# 简单的任务API
@app.get("/api/tasks")
async def get_tasks():
    """获取任务列表"""
    return [
        {
            "id": "1",
            "description": "测试任务1",
            "status": "pending",
            "priority": 1,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "2", 
            "description": "测试任务2",
            "status": "completed",
            "priority": 2,
            "created_at": "2024-01-02T00:00:00Z"
        }
    ]

@app.post("/api/tasks")
async def create_task(task: dict):
    """创建新任务"""
    return {
        "id": "3",
        "description": task.get("description", "新任务"),
        "status": "pending",
        "priority": task.get("priority", 1),
        "created_at": "2024-01-03T00:00:00Z"
    }

# AI模型调用API
class ModelRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"  # 默认模型

@app.post("/api/model/generate", tags=["AI"])
async def generate_text(request: ModelRequest):
    """使用AI模型生成文本"""
    try:
        # 模拟AI模型调用
        response = f"这是来自{request.model}的回复: {request.prompt}"
        
        # 返回结果
        return {
            "success": True,
            "model": request.model,
            "response": response,
            "tokens": len(request.prompt.split()) * 2  # 简单估算token数
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# AG2智能体调用API
@app.post("/api/agents/run", tags=["智能体"])
async def run_agent(
    task: str = Body(..., description="要执行的任务描述"),
    agent_type: str = Body("planner", description="智能体类型")
):
    """调用AG2智能体执行任务"""
    try:
        # 模拟智能体执行过程
        return {
            "success": True,
            "agent_type": agent_type,
            "task": task,
            "result": f"{agent_type}智能体已处理任务: {task}",
            "steps": [
                {"step": 1, "action": "分析任务", "output": "理解任务需求"},
                {"step": 2, "action": "执行计划", "output": "生成执行方案"},
                {"step": 3, "action": "总结结果", "output": "任务完成"}
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 直接运行此文件时启动服务器
if __name__ == "__main__":
    uvicorn.run("helios.main_api_simple:app", host="0.0.0.0", port=8000, reload=True) 

import uvicorn
import os
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Helios 智能规划系统 API",
    description="Helios 自适应规划项目的RESTful API服务",
    version="1.0.0",
)

# 获取允许的CORS来源
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 static 目录，用于提供 CSS, JS 等文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 将根路径指向 index.html
@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('static/index.html')

# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查端点，用于监控系统是否正常运行"""
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "development")}

# 简单的任务API
@app.get("/api/tasks")
async def get_tasks():
    """获取任务列表"""
    return [
        {
            "id": "1",
            "description": "测试任务1",
            "status": "pending",
            "priority": 1,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "2", 
            "description": "测试任务2",
            "status": "completed",
            "priority": 2,
            "created_at": "2024-01-02T00:00:00Z"
        }
    ]

@app.post("/api/tasks")
async def create_task(task: dict):
    """创建新任务"""
    return {
        "id": "3",
        "description": task.get("description", "新任务"),
        "status": "pending",
        "priority": task.get("priority", 1),
        "created_at": "2024-01-03T00:00:00Z"
    }

# AI模型调用API
class ModelRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"  # 默认模型

@app.post("/api/model/generate", tags=["AI"])
async def generate_text(request: ModelRequest):
    """使用AI模型生成文本"""
    try:
        # 模拟AI模型调用
        response = f"这是来自{request.model}的回复: {request.prompt}"
        
        # 返回结果
        return {
            "success": True,
            "model": request.model,
            "response": response,
            "tokens": len(request.prompt.split()) * 2  # 简单估算token数
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# AG2智能体调用API
@app.post("/api/agents/run", tags=["智能体"])
async def run_agent(
    task: str = Body(..., description="要执行的任务描述"),
    agent_type: str = Body("planner", description="智能体类型")
):
    """调用AG2智能体执行任务"""
    try:
        # 模拟智能体执行过程
        return {
            "success": True,
            "agent_type": agent_type,
            "task": task,
            "result": f"{agent_type}智能体已处理任务: {task}",
            "steps": [
                {"step": 1, "action": "分析任务", "output": "理解任务需求"},
                {"step": 2, "action": "执行计划", "output": "生成执行方案"},
                {"step": 3, "action": "总结结果", "output": "任务完成"}
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 直接运行此文件时启动服务器
if __name__ == "__main__":
    uvicorn.run("helios.main_api_simple:app", host="0.0.0.0", port=8000, reload=True) 