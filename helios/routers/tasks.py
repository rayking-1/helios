# helios/routers/tasks.py

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field

from helios.repositories.task_repository import TaskRepository
from helios.repositories.conversation_repository import ConversationRepository
from helios.database.dependencies import get_task_repository, get_conversation_repository
from helios.services import logger

# 导入 WebSocket 广播功能
# 使用 try/except 避免循环导入问题
try:
    from helios.routers.websocket import broadcast_message
except ImportError:
    # 如果 websocket 模块尚未加载，提供一个空函数
    async def broadcast_message(task_id, message):
        pass

# API模型
class TaskCreate(BaseModel):
    description: str
    priority: int = Field(default=10)
    user_id: int

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None

class TaskStatusUpdate(BaseModel):
    status: str

class TaskResult(BaseModel):
    summary: str
    details: dict

class MessageCreate(BaseModel):
    speaker: str
    message: str

class Message(BaseModel):
    id: int
    sequence_order: int
    speaker: str
    message: str
    created_at: str

    class Config:
        from_attributes = True

class Task(BaseModel):
    id: uuid.UUID
    description: str
    status: str
    priority: int
    user_id: int
    created_at: str
    updated_at: str
    result: Optional[dict] = None

    class Config:
        from_attributes = True

# 创建路由
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}}
)

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """创建新任务"""
    return task_repo.create(**task_data.model_dump())

@router.get("/", response_model=List[Task])
async def list_tasks(
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """获取任务列表，可选按状态或用户ID过滤"""
    if status and user_id:
        return task_repo.find(status=status, user_id=user_id)
    elif status:
        return task_repo.find_by_status(status)
    elif user_id:
        return task_repo.find_by_user_id(user_id)
    else:
        return task_repo.get_all()

@router.get("/pending", response_model=List[Task])
async def get_pending_tasks(
    limit: int = 10,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """获取待处理的任务"""
    return task_repo.find_pending_tasks(limit=limit)

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """获取单个任务的详细信息"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: uuid.UUID,
    task_data: TaskUpdate,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """更新任务信息"""
    # 过滤掉None值
    update_data = {k: v for k, v in task_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_task = task_repo.update(task_id, **update_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task

@router.patch("/{task_id}/status", response_model=Task)
async def update_task_status(
    task_id: uuid.UUID,
    status_data: TaskStatusUpdate,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """更新任务状态"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = task_repo.update(task_id, status=status_data.status)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task

@router.put("/{task_id}/result", response_model=Task)
async def set_task_result(
    task_id: uuid.UUID,
    result: TaskResult,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """设置任务结果"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 更新任务结果和状态
    return task_repo.update(
        task_id,
        result=result.model_dump(),
        status="COMPLETED"
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """删除任务"""
    success = task_repo.delete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/{task_id}/messages", response_model=List[Message])
async def get_task_messages(
    task_id: uuid.UUID,
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """获取任务的所有对话消息"""
    return conv_repo.find_by_task_id(task_id)

@router.post("/{task_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def add_task_message(
    task_id: uuid.UUID,
    message_data: MessageCreate,
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repository),
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """添加任务对话消息"""
    # 检查任务是否存在
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 添加消息
    message = conv_repo.add_message(
        task_id=task_id,
        speaker=message_data.speaker,
        message=message_data.message
    )
    
    # 在后台广播消息
    background_tasks.add_task(broadcast_message, str(task_id), message_data.model_dump())
    
    return message