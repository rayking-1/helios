# helios/routers/websocket.py

import json
import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from starlette.websockets import WebSocketState

from helios.services import logger
from helios.repositories.task_repository import TaskRepository
from helios.repositories.conversation_repository import ConversationRepository
from helios.database.dependencies import get_task_repository, get_conversation_repository

router = APIRouter(tags=["websocket"])

# 存储活动连接的字典
# 格式: {task_id: [websocket1, websocket2, ...]}
active_connections: Dict[str, List[WebSocket]] = {}

async def get_task_or_404(
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """获取任务或返回404错误"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.websocket("/ws/tasks/{task_id}/messages")
async def websocket_task_messages(
    websocket: WebSocket,
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository),
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """WebSocket端点，用于实时接收任务消息"""
    # 检查任务是否存在
    task = task_repo.get(task_id)
    if not task:
        await websocket.close(code=1000)
        return
    
    # 接受WebSocket连接
    await websocket.accept()
    
    # 将连接添加到活动连接列表
    if str(task_id) not in active_connections:
        active_connections[str(task_id)] = []
    active_connections[str(task_id)].append(websocket)
    
    logger.info(f"WebSocket连接已建立: 任务ID={task_id}")
    
    try:
        # 发送现有消息历史
        messages = conv_repo.find_by_task_id(task_id)
        for message in messages:
            await websocket.send_text(json.dumps({
                "id": message.id,
                "sequence_order": message.sequence_order,
                "speaker": message.speaker,
                "message": message.message,
                "created_at": message.created_at.isoformat(),
            }))
        
        # 持续监听消息
        while True:
            data = await websocket.receive_text()
            # 处理接收到的消息（如果需要）
            logger.info(f"收到WebSocket消息: {data}")
    except WebSocketDisconnect:
        # 连接断开时，从活动连接列表中移除
        if str(task_id) in active_connections:
            active_connections[str(task_id)].remove(websocket)
            if not active_connections[str(task_id)]:
                del active_connections[str(task_id)]
        logger.info(f"WebSocket连接已断开: 任务ID={task_id}")
    except Exception as e:
        logger.error(f"WebSocket错误: {str(e)}")
        # 如果连接仍然活跃，则关闭它
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close(code=1011)

async def broadcast_message(task_id: uuid.UUID, message: Dict[str, Any]):
    """向所有连接到特定任务的客户端广播消息"""
    if str(task_id) not in active_connections:
        return
    
    disconnected = []
    for websocket in active_connections[str(task_id)]:
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            disconnected.append(websocket)
    
    # 清理断开的连接
    for ws in disconnected:
        active_connections[str(task_id)].remove(ws)
    
    if not active_connections[str(task_id)]:
        del active_connections[str(task_id)] 
 
 
 
 

import json
import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from starlette.websockets import WebSocketState

from helios.services import logger
from helios.repositories.task_repository import TaskRepository
from helios.repositories.conversation_repository import ConversationRepository
from helios.database.dependencies import get_task_repository, get_conversation_repository

router = APIRouter(tags=["websocket"])

# 存储活动连接的字典
# 格式: {task_id: [websocket1, websocket2, ...]}
active_connections: Dict[str, List[WebSocket]] = {}

async def get_task_or_404(
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    """获取任务或返回404错误"""
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.websocket("/ws/tasks/{task_id}/messages")
async def websocket_task_messages(
    websocket: WebSocket,
    task_id: uuid.UUID,
    task_repo: TaskRepository = Depends(get_task_repository),
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """WebSocket端点，用于实时接收任务消息"""
    # 检查任务是否存在
    task = task_repo.get(task_id)
    if not task:
        await websocket.close(code=1000)
        return
    
    # 接受WebSocket连接
    await websocket.accept()
    
    # 将连接添加到活动连接列表
    if str(task_id) not in active_connections:
        active_connections[str(task_id)] = []
    active_connections[str(task_id)].append(websocket)
    
    logger.info(f"WebSocket连接已建立: 任务ID={task_id}")
    
    try:
        # 发送现有消息历史
        messages = conv_repo.find_by_task_id(task_id)
        for message in messages:
            await websocket.send_text(json.dumps({
                "id": message.id,
                "sequence_order": message.sequence_order,
                "speaker": message.speaker,
                "message": message.message,
                "created_at": message.created_at.isoformat(),
            }))
        
        # 持续监听消息
        while True:
            data = await websocket.receive_text()
            # 处理接收到的消息（如果需要）
            logger.info(f"收到WebSocket消息: {data}")
    except WebSocketDisconnect:
        # 连接断开时，从活动连接列表中移除
        if str(task_id) in active_connections:
            active_connections[str(task_id)].remove(websocket)
            if not active_connections[str(task_id)]:
                del active_connections[str(task_id)]
        logger.info(f"WebSocket连接已断开: 任务ID={task_id}")
    except Exception as e:
        logger.error(f"WebSocket错误: {str(e)}")
        # 如果连接仍然活跃，则关闭它
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close(code=1011)

async def broadcast_message(task_id: uuid.UUID, message: Dict[str, Any]):
    """向所有连接到特定任务的客户端广播消息"""
    if str(task_id) not in active_connections:
        return
    
    disconnected = []
    for websocket in active_connections[str(task_id)]:
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            disconnected.append(websocket)
    
    # 清理断开的连接
    for ws in disconnected:
        active_connections[str(task_id)].remove(ws)
    
    if not active_connections[str(task_id)]:
        del active_connections[str(task_id)] 
 
 
 
 