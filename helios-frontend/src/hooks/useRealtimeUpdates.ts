import { useState, useEffect, useRef, useCallback } from 'react';
import { useAppStore } from '../store/useAppStore';

// 定义WebSocket消息类型
export interface WebSocketMessage {
  event: string;
  payload: any;
}

// 配置
const WS_RECONNECT_DELAY = 3000;
const WS_MAX_RETRIES = 5;
const WS_PING_INTERVAL = 30000;

// 获取WebSocket URL，支持不同环境配置
const getWebSocketUrl = (userId: string, taskId?: string): string => {
  const baseUrl = import.meta.env.VITE_API_WS_URL || `ws://${window.location.hostname}:8000`;
  
  // 根据技术报告04，支持两种WebSocket端点
  if (taskId) {
    // 任务特定的实时更新
    return `${baseUrl}/ws/tasks/${taskId}/messages`;
  } else {
    // 用户级别的全局更新
    return `${baseUrl}/ws/${userId}`;
  }
};

/**
 * 自定义Hook: 处理WebSocket实时通信
 * 
 * @param userId 当前用户ID
 * @param taskId 可选，特定任务ID
 * @returns 包含连接状态、最后接收的消息和控制方法的对象
 */
export const useRealtimeUpdates = (userId: string, taskId?: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [connectionAttempts, setConnectionAttempts] = useState(0);
  
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const pingIntervalRef = useRef<number | null>(null);
  
  // 从Zustand store获取更新方法
  const {
    updatePlan,
    addAgentMessage,
    updateSystemStatus,
    updateTaskStatus
  } = useAppStore();

  // 处理接收到的消息
  const handleMessage = useCallback((message: WebSocketMessage) => {
    setLastMessage(message);
    
    // 根据事件类型分发到不同的处理函数
    switch (message.event) {
      case 'PLAN_UPDATED':
        console.log('Plan updated:', message.payload.plan);
        updatePlan(message.payload.plan);
        break;
        
      case 'AGENT_MESSAGE':
        console.log('Agent message:', message.payload);
        addAgentMessage(message.payload);
        break;
        
      case 'STATUS_CHANGE':
        console.log('System status changed:', message.payload.status);
        updateSystemStatus(message.payload.status, message.payload.details);
        break;
        
      case 'TASK_STATUS_CHANGED':
        console.log('Task status changed:', message.payload.taskId, message.payload.status);
        updateTaskStatus(message.payload.taskId, message.payload.status);
        break;
        
      case 'FEEDBACK_PROCESSED':
        console.log('Feedback processed:', message.payload);
        // 这可能会触发UI通知或更新任务状态
        break;
        
      case 'PONG':
        // 心跳响应，不需要特殊处理
        break;
        
      default:
        console.log('Received unhandled message type:', message.event);
    }
  }, [updatePlan, addAgentMessage, updateSystemStatus, updateTaskStatus]);

  // 发送心跳以保持连接活跃
  const sendPing = useCallback(() => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      console.debug('Sending ping');
      socketRef.current.send(JSON.stringify({ event: 'PING' }));
    }
  }, []);

  // 连接WebSocket
  const connect = useCallback(() => {
    // 如果已经连接，则不重复连接
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    // 清除现有的重连计时器
    if (reconnectTimeoutRef.current) {
      window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    // 清除心跳计时器
    if (pingIntervalRef.current) {
      window.clearInterval(pingIntervalRef.current);
      pingIntervalRef.current = null;
    }

    // 超过最大重试次数，停止尝试
    if (connectionAttempts >= WS_MAX_RETRIES) {
      console.error(`Failed to connect after ${WS_MAX_RETRIES} attempts`);
      return;
    }

    const wsUrl = getWebSocketUrl(userId, taskId);
    console.log(`Connecting to WebSocket: ${wsUrl} (Attempt ${connectionAttempts + 1}/${WS_MAX_RETRIES})`);
    
    try {
      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket connection opened');
        setIsConnected(true);
        setConnectionAttempts(0); // 重置重试计数
        
        // 设置定期发送心跳的计时器
        pingIntervalRef.current = window.setInterval(sendPing, WS_PING_INTERVAL);
      };

      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          handleMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      socket.onclose = (event) => {
        console.log(`WebSocket connection closed (Code: ${event.code}): ${event.reason || 'No reason provided'}`);
        setIsConnected(false);
        
        // 清除心跳计时器
        if (pingIntervalRef.current) {
          window.clearInterval(pingIntervalRef.current);
          pingIntervalRef.current = null;
        }
        
        // 增加连接尝试计数
        setConnectionAttempts(prev => prev + 1);
        
        // 自动重连（使用指数退避策略）
        const delay = Math.min(WS_RECONNECT_DELAY * Math.pow(1.5, connectionAttempts), 30000);
        console.log(`Reconnecting in ${delay/1000} seconds...`);
        
        reconnectTimeoutRef.current = window.setTimeout(() => {
          console.log('Attempting to reconnect...');
          connect();
        }, delay);
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      
      // 如果创建连接失败，也尝试重连
      setConnectionAttempts(prev => prev + 1);
      reconnectTimeoutRef.current = window.setTimeout(connect, WS_RECONNECT_DELAY);
    }
  }, [userId, taskId, connectionAttempts, handleMessage, sendPing]);

  // 断开连接
  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    
    // 清除所有计时器
    if (reconnectTimeoutRef.current) {
      window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (pingIntervalRef.current) {
      window.clearInterval(pingIntervalRef.current);
      pingIntervalRef.current = null;
    }
    
    setIsConnected(false);
    setConnectionAttempts(0);
  }, []);

  // 发送消息
  const sendMessage = useCallback((message: any) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message));
    } else {
      console.error('Cannot send message: WebSocket is not connected');
      // 可能的UI通知：消息发送失败
    }
  }, []);

  // 组件挂载时连接，卸载时断开
  useEffect(() => {
    if (userId) {
      connect();
    }
    
    return () => {
      disconnect();
    };
  }, [userId, taskId, connect, disconnect]);

  // 返回状态和方法
  return {
    isConnected,            // 连接状态
    lastMessage,            // 最后收到的消息
    sendMessage,            // 发送消息的方法
    connect,                // 手动重连方法
    disconnect,             // 手动断开方法
    connectionAttempts      // 当前连接尝试次数
  };
};

export default useRealtimeUpdates; 