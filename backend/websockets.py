from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # 使用字典存储连接，键为user_id
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """
        处理新的WebSocket连接
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"用户 {user_id} 已连接。当前活动连接数: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        """
        处理WebSocket断开连接
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"用户 {user_id} 已断开连接。当前活动连接数: {len(self.active_connections)}")

    async def broadcast_to_user(self, user_id: str, message: Dict[str, Any]):
        """
        向特定用户发送消息
        """
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
            logger.info(f"向用户 {user_id} 发送了消息: {message['event']}")
        else:
            logger.warning(f"尝试向未连接的用户 {user_id} 发送消息")

    async def broadcast(self, message: Dict[str, Any]):
        """
        广播消息给所有连接的用户
        """
        disconnected_users = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"向用户 {user_id} 发送消息时出错: {str(e)}")
                disconnected_users.append(user_id)

        # 清理已断开的连接
        for user_id in disconnected_users:
            self.disconnect(user_id)

# 创建全局连接管理器实例
manager = ConnectionManager()

# 创建示例消息结构
def create_plan_updated_message(plan_data):
    """创建计划更新消息"""
    return {
        "event": "PLAN_UPDATED",
        "payload": {
            "plan": plan_data
        }
    }

def create_agent_message(agent_name: str, message: str):
    """创建代理消息"""
    return {
        "event": "AGENT_MESSAGE",
        "payload": {
            "agentName": agent_name,
            "message": message,
            "timestamp": None  # 在实际使用时，会自动添加
        }
    }

def create_status_message(status: str, details: str = None):
    """创建状态消息"""
    return {
        "event": "STATUS_CHANGE",
        "payload": {
            "status": status,
            "details": details
        }
    }

# 示例 WebSocket 路由函数 (需要在主应用中注册)
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket连接处理函数"""
    await manager.connect(websocket, user_id)
    try:
        # 发送初始连接成功消息
        await websocket.send_json({
            "event": "CONNECTION_ESTABLISHED",
            "payload": {
                "message": "WebSocket连接已建立",
                "userId": user_id
            }
        })

        # 持续接收消息
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(f"收到来自用户 {user_id} 的消息: {message}")

            # 处理客户端消息
            # 在实际应用中，可能需要根据消息类型调用不同的处理函数
            response = {"event": "RECEIVED", "payload": {"originalMessage": message}}
            await websocket.send_json(response)

    except WebSocketDisconnect:
        logger.info(f"WebSocket断开: 用户 {user_id}")
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket处理错误: {str(e)}")
        manager.disconnect(user_id) 
 
from typing import Dict, List, Any
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # 使用字典存储连接，键为user_id
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """
        处理新的WebSocket连接
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"用户 {user_id} 已连接。当前活动连接数: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        """
        处理WebSocket断开连接
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"用户 {user_id} 已断开连接。当前活动连接数: {len(self.active_connections)}")

    async def broadcast_to_user(self, user_id: str, message: Dict[str, Any]):
        """
        向特定用户发送消息
        """
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
            logger.info(f"向用户 {user_id} 发送了消息: {message['event']}")
        else:
            logger.warning(f"尝试向未连接的用户 {user_id} 发送消息")

    async def broadcast(self, message: Dict[str, Any]):
        """
        广播消息给所有连接的用户
        """
        disconnected_users = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"向用户 {user_id} 发送消息时出错: {str(e)}")
                disconnected_users.append(user_id)

        # 清理已断开的连接
        for user_id in disconnected_users:
            self.disconnect(user_id)

# 创建全局连接管理器实例
manager = ConnectionManager()

# 创建示例消息结构
def create_plan_updated_message(plan_data):
    """创建计划更新消息"""
    return {
        "event": "PLAN_UPDATED",
        "payload": {
            "plan": plan_data
        }
    }

def create_agent_message(agent_name: str, message: str):
    """创建代理消息"""
    return {
        "event": "AGENT_MESSAGE",
        "payload": {
            "agentName": agent_name,
            "message": message,
            "timestamp": None  # 在实际使用时，会自动添加
        }
    }

def create_status_message(status: str, details: str = None):
    """创建状态消息"""
    return {
        "event": "STATUS_CHANGE",
        "payload": {
            "status": status,
            "details": details
        }
    }

# 示例 WebSocket 路由函数 (需要在主应用中注册)
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket连接处理函数"""
    await manager.connect(websocket, user_id)
    try:
        # 发送初始连接成功消息
        await websocket.send_json({
            "event": "CONNECTION_ESTABLISHED",
            "payload": {
                "message": "WebSocket连接已建立",
                "userId": user_id
            }
        })

        # 持续接收消息
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(f"收到来自用户 {user_id} 的消息: {message}")

            # 处理客户端消息
            # 在实际应用中，可能需要根据消息类型调用不同的处理函数
            response = {"event": "RECEIVED", "payload": {"originalMessage": message}}
            await websocket.send_json(response)

    except WebSocketDisconnect:
        logger.info(f"WebSocket断开: 用户 {user_id}")
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket处理错误: {str(e)}")
        manager.disconnect(user_id) 
 
 