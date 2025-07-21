import { apiClient } from './config';

// 类型定义
export interface Task {
  taskId: string;
  description: string;
  dueDate: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  dependsOn: string[];
}

export interface Plan {
  planId: string;
  version: string;
  goal: string;
  tasks: Task[];
  changelog?: string;
}

export interface FeedbackPayload {
  feedbackType: 'TOO_HARD' | 'TOO_EASY' | 'UNCLEAR' | 'NOT_RELEVANT' | 'OTHER';
  comment?: string;
  timestamp?: string;
}

export interface SystemStatus {
  status: string;
  details: string | null;
}

/**
 * 自适应规划系统API
 * 按照技术报告04中的接口定义实现
 */
export const planApi = {
  // 启动新规划
  startNewPlan: async (goal: string): Promise<{ planId: string }> => {
    const response = await apiClient.post('/api/v1/plans', { goal });
    return response.data;
  },
  
  // 获取当前计划
  getCurrentPlan: async (planId?: string): Promise<Plan> => {
    // 如果提供了planId则获取特定计划，否则获取当前激活的计划
    const endpoint = planId ? `/api/v1/plans/${planId}` : '/api/v1/plans/current';
    const response = await apiClient.get(endpoint);
    return response.data;
  },
  
  // 获取计划历史版本
  getPlanHistory: async (planId: string): Promise<Plan[]> => {
    const response = await apiClient.get(`/api/v1/plans/${planId}/history`);
    return response.data;
  },
  
  // 查询任务状态
  getTaskDetails: async (taskId: string): Promise<Task> => {
    const response = await apiClient.get(`/api/v1/tasks/${taskId}`);
    return response.data;
  },
  
  // 提交任务反馈
  submitTaskFeedback: async (taskId: string, feedback: FeedbackPayload): Promise<{ status: string }> => {
    const response = await apiClient.post(`/api/v1/tasks/${taskId}/feedback`, feedback);
    return response.data;
  },
  
  // 获取系统状态
  getSystemStatus: async (): Promise<SystemStatus> => {
    const response = await apiClient.get('/api/v1/system/status');
    return response.data;
  },
  
  // 更新任务状态（例如标记完成）
  updateTaskStatus: async (taskId: string, status: Task['status']): Promise<Task> => {
    const response = await apiClient.patch(`/api/v1/tasks/${taskId}/status`, { status });
    return response.data;
  }
};

export default planApi; 
 
 