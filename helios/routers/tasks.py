# helios/routers/tasks.py

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime

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

# 按照技术报告04添加的新模型
class FeedbackPayload(BaseModel):
    """用户对任务的反馈数据模型"""
    feedbackType: str  # 反馈类型，例如：'TOO_HARD', 'TOO_EASY', 'UNCLEAR'等
    comment: Optional[str] = None  # 用户的具体反馈文本
    timestamp: datetime = Field(default_factory=datetime.now)  # 反馈时间，默认为当前时间

class FeedbackResponse(BaseModel):
    """反馈提交后的响应模型"""
    status: str
    taskId: str
    receivedAt: datetime

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
    return task_repo.find_by_status("PENDING", limit=limit)

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
    """更新任务的基本信息"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = {k: v for k, v in task_data.model_dump().items() if v is not None}
    updated_task = task_repo.update(task_id, **update_data)
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
    return updated_task

@router.put("/{task_id}/result", response_model=Task)
async def set_task_result(
    task_id: uuid.UUID,
    result: TaskResult,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """设置任务的执行结果"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = task_repo.update(
        task_id,
        result={
            "summary": result.summary,
            "details": result.details
        }
    )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """删除任务"""
    task_repo.delete(task_id)
    return None

@router.get("/{task_id}/messages", response_model=List[Message])
async def get_task_messages(
    task_id: uuid.UUID,
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """获取与任务相关的消息历史"""
    return conv_repo.find_by_task_id(task_id)

@router.post("/{task_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def add_task_message(
    task_id: uuid.UUID,
    message_data: MessageCreate,
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repository),
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """为任务添加新消息"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    message = conv_repo.add_message(
        task_id=task_id,
        speaker=message_data.speaker,
        message=message_data.message
    )
    
    # 异步广播消息
    background_tasks.add_task(
        broadcast_message,
        task_id=task_id,
        message={
            "id": message.id,
            "sequence_order": message.sequence_order,
            "speaker": message.speaker,
            "message": message.message,
            "created_at": message.created_at.isoformat(),
        }
    )
    
    return message

# 新增端点：提交任务反馈
@router.post("/{task_id}/feedback", response_model=FeedbackResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_task_feedback(
    task_id: uuid.UUID,
    feedback: FeedbackPayload,
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """
    接收用户对特定任务的反馈，并触发适应性循环
    
    此端点实现了技术报告04中定义的API接口规范，用于处理任务反馈
    """
    # 验证任务是否存在
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    logger.info(f"收到任务 {task_id} 的反馈: {feedback.feedbackType}")
    
    # 异步处理反馈（避免阻塞API响应）
    background_tasks.add_task(
        process_feedback,
        task_id=task_id,
        feedback=feedback
    )
    
    # 立即返回接收确认
    return {
        "status": "feedback received",
        "taskId": str(task_id),
        "receivedAt": datetime.now()
    }

async def process_feedback(task_id: uuid.UUID, feedback: FeedbackPayload):
    """后台处理任务反馈的异步函数"""
    try:
        logger.info(f"处理任务 {task_id} 的反馈")
        
        # 这里应该调用适配器智能体或反馈处理系统
        # 在实际实现中，这可能包括：
        # 1. 调用FeedbackAgent处理反馈
        # 2. 根据反馈类型触发不同的处理逻辑
        # 3. 更新任务或生成新的计划
        
        # 模拟处理延迟
        import asyncio
        await asyncio.sleep(1)
        
        # 通过WebSocket广播反馈已被处理的消息
        await broadcast_message(
            task_id=task_id,
            message={
                "event": "FEEDBACK_PROCESSED",
                "taskId": str(task_id),
                "feedbackType": feedback.feedbackType,
                "processedAt": datetime.now().isoformat()
            }
        )
        
        logger.info(f"任务 {task_id} 的反馈处理完成")
    except Exception as e:
        logger.error(f"处理任务 {task_id} 的反馈时出错: {str(e)}")