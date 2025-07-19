import { apiClient } from './config';
import { Task, TaskStatus } from '../types';
import { adaptTaskFromBackend, adaptTaskToBackend, adaptTaskUpdateToBackend } from './adapters';

export const taskApi = {
  // 获取所有任务
  getTasks: async (): Promise<Task[]> => {
    const response = await apiClient.get('/tasks');
    return response.data.map(adaptTaskFromBackend);
  },

  // 创建任务
  createTask: async (task: Partial<Task>): Promise<Task> => {
    // 假设当前用户ID为1，实际应从用户状态或会话中获取
    const userId = 1;
    const backendTask = adaptTaskToBackend(task, userId);
    const response = await apiClient.post('/tasks', backendTask);
    return adaptTaskFromBackend(response.data);
  },

  // 更新任务
  updateTask: async (id: string, updates: Partial<Task>): Promise<Task> => {
    const backendUpdates = adaptTaskUpdateToBackend(updates);
    const response = await apiClient.patch(`/tasks/${id}`, backendUpdates);
    return adaptTaskFromBackend(response.data);
  },

  // 删除任务
  deleteTask: async (id: string): Promise<void> => {
    await apiClient.delete(`/tasks/${id}`);
  },

  // 更新任务状态
  updateTaskStatus: async (id: string, status: TaskStatus): Promise<Task> => {
    const response = await apiClient.patch(`/tasks/${id}/status`, { status });
    return adaptTaskFromBackend(response.data);
  },
  updateTaskStatus: async (id: string, status: TaskStatus): Promise<Task> => {
    const response = await apiClient.patch(`/tasks/${id}/status`, { status });
    return adaptTaskFromBackend(response.data);
  },