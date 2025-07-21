import { useState, useEffect, useRef, useCallback } from 'react';
import { useAppStore } from '../store/useAppStore'; // 假设使用了Zustand作为状态管理

interface WebSocketMessage {
  event: string;
  payload: any;
}

// 可配置的WebSocket URL
const getWebSocketUrl = (userId: string): string => {
  const baseUrl = import.meta.env.VITE_API_WS_URL || `ws://${window.location.hostname}:8000`;
  return `${baseUrl}/ws/${userId}`;
};

export const useWebSocketUpdates = (userId: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  
  // 从Zustand store获取更新方法
  const { updatePlan, addAgentMessage, updateSystemStatus } = useAppStore();

  // 处理接收到的消息
  const handleMessage = useCallback((message: WebSocketMessage) => {
    setLastMessage(message);
    
    // 根据事件类型分发到不同的处理函数
    switch (message.event) {
      case 'PLAN_UPDATED':
        updatePlan(message.payload.plan);
        break;
      case 'AGENT_MESSAGE':
        addAgentMessage(message.payload);
        break;
      case 'STATUS_CHANGE':
        updateSystemStatus(message.payload.status, message.payload.details);
        break;
      case 'CONNECTION_ESTABLISHED':
        console.log('WebSocket连接已建立:', message.payload);
        break;
      default:
        console.log('收到未处理的消息类型:', message.event);
    }
  }, [updatePlan, addAgentMessage, updateSystemStatus]);

  // 连接WebSocket
  const connect = useCallback(() => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      return; // 已连接，不需要重新连接
    }

    // 清除现有的重连计时器
    if (reconnectTimeoutRef.current) {
      window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    const wsUrl = getWebSocketUrl(userId);
    console.log(`正在连接到WebSocket: ${wsUrl}`);
    
    try {
      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket连接已打开');
        setIsConnected(true);
      };

      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          handleMessage(message);
        } catch (error) {
          console.error('解析WebSocket消息失败:', error);
        }
      };

      socket.onclose = (event) => {
        console.log(`WebSocket连接已关闭 (Code: ${event.code}): ${event.reason || '无原因'}`);
        setIsConnected(false);
        
        // 自动重连（延迟3秒）
        reconnectTimeoutRef.current = window.setTimeout(() => {
          console.log('尝试重新连接...');
          connect();
        }, 3000);
      };

      socket.onerror = (error) => {
        console.error('WebSocket错误:', error);
      };
    } catch (error) {
      console.error('创建WebSocket连接失败:', error);
    }
  }, [userId, handleMessage]);

  // 断开连接
  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    
    if (reconnectTimeoutRef.current) {
      window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    setIsConnected(false);
  }, []);

  // 发送消息
  const sendMessage = useCallback((message: any) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message));
    } else {
      console.error('无法发送消息: WebSocket未连接');
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
  }, [userId, connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    connect,
    disconnect
  };
};

export default useWebSocketUpdates; 
 
import { useAppStore } from '../store/useAppStore'; // 假设使用了Zustand作为状态管理

interface WebSocketMessage {
  event: string;
  payload: any;
}

// 可配置的WebSocket URL
const getWebSocketUrl = (userId: string): string => {
  const baseUrl = import.meta.env.VITE_API_WS_URL || `ws://${window.location.hostname}:8000`;
  return `${baseUrl}/ws/${userId}`;
};

export const useWebSocketUpdates = (userId: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  
  // 从Zustand store获取更新方法
  const { updatePlan, addAgentMessage, updateSystemStatus } = useAppStore();

  // 处理接收到的消息
  const handleMessage = useCallback((message: WebSocketMessage) => {
    setLastMessage(message);
    
    // 根据事件类型分发到不同的处理函数
    switch (message.event) {
      case 'PLAN_UPDATED':
        updatePlan(message.payload.plan);
        break;
      case 'AGENT_MESSAGE':
        addAgentMessage(message.payload);
        break;
      case 'STATUS_CHANGE':
        updateSystemStatus(message.payload.status, message.payload.details);
        break;
      case 'CONNECTION_ESTABLISHED':
        console.log('WebSocket连接已建立:', message.payload);
        break;
      default:
        console.log('收到未处理的消息类型:', message.event);
    }
  }, [updatePlan, addAgentMessage, updateSystemStatus]);

  // 连接WebSocket
  const connect = useCallback(() => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      return; // 已连接，不需要重新连接
    }

    // 清除现有的重连计时器
    if (reconnectTimeoutRef.current) {
      window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    const wsUrl = getWebSocketUrl(userId);
    console.log(`正在连接到WebSocket: ${wsUrl}`);
    
    try {
      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket连接已打开');
        setIsConnected(true);
      };

      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          handleMessage(message);
        } catch (error) {
          console.error('解析WebSocket消息失败:', error);
        }
      };

      socket.onclose = (event) => {
        console.log(`WebSocket连接已关闭 (Code: ${event.code}): ${event.reason || '无原因'}`);
        setIsConnected(false);
        
        // 自动重连（延迟3秒）
        reconnectTimeoutRef.current = window.setTimeout(() => {
          console.log('尝试重新连接...');
          connect();
        }, 3000);
      };

      socket.onerror = (error) => {
        console.error('WebSocket错误:', error);
      };
    } catch (error) {
      console.error('创建WebSocket连接失败:', error);
    }
  }, [userId, handleMessage]);

  // 断开连接
  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    
    if (reconnectTimeoutRef.current) {
      window.clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    setIsConnected(false);
  }, []);

  // 发送消息
  const sendMessage = useCallback((message: any) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message));
    } else {
      console.error('无法发送消息: WebSocket未连接');
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
  }, [userId, connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    connect,
    disconnect
  };
};

export default useWebSocketUpdates; 
 
 