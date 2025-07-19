import { apiClient } from './config';
import { AgentMessage } from '../types';

// 后端消息类型
interface BackendMessage {
  id: number;
  sequence_order: number;
  speaker: string;
  message: string;
  created_at: string;
}

// 将后端消息转换为前端 AgentMessage
function adaptMessageFromBackend(backendMessage: BackendMessage): AgentMessage {
  return {
    id: backendMessage.id.toString(),
    agentRole: backendMessage.speaker as any, // 后端的 speaker 对应前端的 agentRole
    type: 'thought', // 默认类型
    content: backendMessage.message,
    timestamp: new Date(backendMessage.created_at),
    taskId: '', // 需要在调用时填充
    metadata: {},
  };
}

export const agentApi = {
  // 获取任务的智能体消息
  getAgentMessages: async (taskId: string): Promise<AgentMessage[]> => {
    const response = await apiClient.get(`/tasks/${taskId}/messages`);
    return response.data.map((msg: BackendMessage) => ({
      ...adaptMessageFromBackend(msg),
      taskId
    }));
  },

  // 建立 WebSocket 连接以实时接收消息
  connectToAgentStream: (taskId: string, onMessage: (message: AgentMessage) => void) => {
    // 获取 API 基础 URL 的主机部分
    const apiUrl = new URL(apiClient.defaults.baseURL || 'http://localhost:8000');
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${apiUrl.host}/ws/tasks/${taskId}/messages`;
    
    const ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
      try {
        const backendMessage = JSON.parse(event.data);
        const message = adaptMessageFromBackend(backendMessage);
        message.taskId = taskId;
        onMessage(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    return ws;
  },

  // 向智能体发送用户输入
  sendUserInput: async (taskId: string, input: string): Promise<void> => {
    await apiClient.post(`/tasks/${taskId}/messages`, { 
      speaker: 'user',
      message: input
    });
  },
  getAgentMessages: async (taskId: string): Promise<AgentMessage[]> => {
    const response = await apiClient.get(`/tasks/${taskId}/messages`);
    return response.data.map((msg: BackendMessage) => ({
      ...adaptMessageFromBackend(msg),
      taskId
    }));
  },

  // 建立 WebSocket 连接以实时接收消息
  connectToAgentStream: (taskId: string, onMessage: (message: AgentMessage) => void) => {
    // 获取 API 基础 URL 的主机部分
    const apiUrl = new URL(apiClient.defaults.baseURL || 'http://localhost:8000');
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${apiUrl.host}/ws/tasks/${taskId}/messages`;
    
    const ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
      try {
        const backendMessage = JSON.parse(event.data);
        const message = adaptMessageFromBackend(backendMessage);
        message.taskId = taskId;
        onMessage(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    return ws;
  },

  // 向智能体发送用户输入
  sendUserInput: async (taskId: string, input: string): Promise<void> => {
    await apiClient.post(`/tasks/${taskId}/messages`, { 
      speaker: 'user',
      message: input
    });
  },