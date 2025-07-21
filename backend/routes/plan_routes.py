from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1", tags=["plans"])

# 数据模型
class TaskModel(BaseModel):
    taskId: str
    description: str
    dueDate: str
    status: str = "PENDING"
    dependsOn: List[str] = []

class PlanModel(BaseModel):
    planId: str
    version: str
    goal: str
    tasks: List[TaskModel]
    changelog: Optional[str] = None

class GoalPayload(BaseModel):
    goal: str
    timeframe: Optional[str] = None
    constraints: Optional[List[str]] = None

# 模拟数据存储
current_plan = None

@router.post("/plans", status_code=status.HTTP_202_ACCEPTED)
async def create_plan(payload: GoalPayload, background_tasks: BackgroundTasks):
    """
    启动新规划，接收用户初始目标，启动多智能体协作流程
    """
    print(f"收到用户目标: {payload.goal}")
    
    # 在实际实现中，这里会调用agent_team.py中的AdaptivePlanTeam
    # 在背景任务中处理，避免阻塞API响应
    background_tasks.add_task(process_plan_creation, payload)
    
    return {"status": "planning started", "message": "Your plan is being generated"}

@router.get("/plans/current", response_model=PlanModel)
async def get_current_plan():
    """
    获取用户当前激活的最新版本计划
    """
    if current_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active plan found. Please create a plan first."
        )
    
    return current_plan

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """
    获取特定任务的详细信息和状态
    """
    if current_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active plan found"
        )
    
    for task in current_plan["tasks"]:
        if task["taskId"] == task_id:
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found"
    )

class FeedbackPayload(BaseModel):
    feedbackType: str
    comment: Optional[str] = None
    timestamp: datetime

@router.post("/tasks/{task_id}/feedback", status_code=status.HTTP_202_ACCEPTED)
async def submit_task_feedback(task_id: str, payload: FeedbackPayload, background_tasks: BackgroundTasks):
    """
    用户提交对任务的反馈，触发反馈循环智能体
    """
    print(f"收到任务 {task_id} 的反馈: {payload.dict()}")
    
    # 在实际实现中，这里会调用agent_team.py中的AdaptorAgent
    background_tasks.add_task(process_feedback, task_id, payload)
    
    return {"status": "feedback received"}

@router.get("/system/status")
async def get_system_status():
    """
    查询后端智能体团队的当前工作状态
    """
    # 在实际实现中，这将从某种状态管理器获取
    return {
        "status": "IDLE" if current_plan else "PLANNING",
        "lastUpdated": datetime.now().isoformat()
    }

# 后台处理函数
async def process_plan_creation(payload: GoalPayload):
    """模拟智能体团队处理计划创建的后台任务"""
    global current_plan
    
    # 在实际实现中，这里会调用AdaptivePlanTeam的run方法
    # 现在使用模拟数据
    current_plan = {
        "planId": f"plan-{uuid.uuid4().hex[:8]}",
        "version": "1.0",
        "goal": payload.goal,
        "tasks": [
            {
                "taskId": f"task-{uuid.uuid4().hex[:6]}",
                "description": "进行20分钟的慢跑训练",
                "dueDate": "2025-07-21",
                "status": "PENDING",
                "dependsOn": []
            },
            {
                "taskId": f"task-{uuid.uuid4().hex[:6]}",
                "description": "进行核心力量训练",
                "dueDate": "2025-07-22",
                "status": "PENDING",
                "dependsOn": []
            }
        ],
        "changelog": "初始计划已创建"
    }
    
    print(f"已生成计划: {current_plan['planId']}")
    # 这里可以添加WebSocket通知

async def process_feedback(task_id: str, payload: FeedbackPayload):
    """模拟智能体处理反馈的后台任务"""
    global current_plan
    
    if current_plan is None:
        print("没有活跃计划，无法处理反馈")
        return
    
    # 模拟计划更新
    if payload.feedbackType == "TOO_HARD":
        current_plan["version"] = "1.1"
        current_plan["changelog"] = f"根据您的反馈'{payload.comment}'，已调整任务难度。"
        
        # 更新任务描述
        for task in current_plan["tasks"]:
            if task["taskId"] == task_id:
                task["description"] = "修改后的" + task["description"]
                break
    
    print(f"已处理反馈并更新计划版本: {current_plan['version']}")
    # 这里可以添加WebSocket通知 
 
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1", tags=["plans"])

# 数据模型
class TaskModel(BaseModel):
    taskId: str
    description: str
    dueDate: str
    status: str = "PENDING"
    dependsOn: List[str] = []

class PlanModel(BaseModel):
    planId: str
    version: str
    goal: str
    tasks: List[TaskModel]
    changelog: Optional[str] = None

class GoalPayload(BaseModel):
    goal: str
    timeframe: Optional[str] = None
    constraints: Optional[List[str]] = None

# 模拟数据存储
current_plan = None

@router.post("/plans", status_code=status.HTTP_202_ACCEPTED)
async def create_plan(payload: GoalPayload, background_tasks: BackgroundTasks):
    """
    启动新规划，接收用户初始目标，启动多智能体协作流程
    """
    print(f"收到用户目标: {payload.goal}")
    
    # 在实际实现中，这里会调用agent_team.py中的AdaptivePlanTeam
    # 在背景任务中处理，避免阻塞API响应
    background_tasks.add_task(process_plan_creation, payload)
    
    return {"status": "planning started", "message": "Your plan is being generated"}

@router.get("/plans/current", response_model=PlanModel)
async def get_current_plan():
    """
    获取用户当前激活的最新版本计划
    """
    if current_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active plan found. Please create a plan first."
        )
    
    return current_plan

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """
    获取特定任务的详细信息和状态
    """
    if current_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active plan found"
        )
    
    for task in current_plan["tasks"]:
        if task["taskId"] == task_id:
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found"
    )

class FeedbackPayload(BaseModel):
    feedbackType: str
    comment: Optional[str] = None
    timestamp: datetime

@router.post("/tasks/{task_id}/feedback", status_code=status.HTTP_202_ACCEPTED)
async def submit_task_feedback(task_id: str, payload: FeedbackPayload, background_tasks: BackgroundTasks):
    """
    用户提交对任务的反馈，触发反馈循环智能体
    """
    print(f"收到任务 {task_id} 的反馈: {payload.dict()}")
    
    # 在实际实现中，这里会调用agent_team.py中的AdaptorAgent
    background_tasks.add_task(process_feedback, task_id, payload)
    
    return {"status": "feedback received"}

@router.get("/system/status")
async def get_system_status():
    """
    查询后端智能体团队的当前工作状态
    """
    # 在实际实现中，这将从某种状态管理器获取
    return {
        "status": "IDLE" if current_plan else "PLANNING",
        "lastUpdated": datetime.now().isoformat()
    }

# 后台处理函数
async def process_plan_creation(payload: GoalPayload):
    """模拟智能体团队处理计划创建的后台任务"""
    global current_plan
    
    # 在实际实现中，这里会调用AdaptivePlanTeam的run方法
    # 现在使用模拟数据
    current_plan = {
        "planId": f"plan-{uuid.uuid4().hex[:8]}",
        "version": "1.0",
        "goal": payload.goal,
        "tasks": [
            {
                "taskId": f"task-{uuid.uuid4().hex[:6]}",
                "description": "进行20分钟的慢跑训练",
                "dueDate": "2025-07-21",
                "status": "PENDING",
                "dependsOn": []
            },
            {
                "taskId": f"task-{uuid.uuid4().hex[:6]}",
                "description": "进行核心力量训练",
                "dueDate": "2025-07-22",
                "status": "PENDING",
                "dependsOn": []
            }
        ],
        "changelog": "初始计划已创建"
    }
    
    print(f"已生成计划: {current_plan['planId']}")
    # 这里可以添加WebSocket通知

async def process_feedback(task_id: str, payload: FeedbackPayload):
    """模拟智能体处理反馈的后台任务"""
    global current_plan
    
    if current_plan is None:
        print("没有活跃计划，无法处理反馈")
        return
    
    # 模拟计划更新
    if payload.feedbackType == "TOO_HARD":
        current_plan["version"] = "1.1"
        current_plan["changelog"] = f"根据您的反馈'{payload.comment}'，已调整任务难度。"
        
        # 更新任务描述
        for task in current_plan["tasks"]:
            if task["taskId"] == task_id:
                task["description"] = "修改后的" + task["description"]
                break
    
    print(f"已处理反馈并更新计划版本: {current_plan['version']}")
    # 这里可以添加WebSocket通知 
 
 