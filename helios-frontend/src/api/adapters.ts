import { Task, TaskStatus } from '../types';

// 后端 Task 类型
export interface BackendTask {
  id: string;
  description: string;
  status: string;
  priority: number;
  user_id: number;
  created_at: string;
  updated_at: string;
  result?: Record<string, any>;
}

// 将后端 Task 转换为前端 Task
export function adaptTaskFromBackend(backendTask: BackendTask): Task {
  // 将数字优先级转换为字符串优先级
  const priorityMap: Record<number, 'low' | 'medium' | 'high'> = {
    0: 'low',
    5: 'medium',
    10: 'high',
  };
  
  return {
    id: backendTask.id,
    title: backendTask.description, // 后端的 description 对应前端的 title
    description: backendTask.description, // 复用 description
    status: backendTask.status as TaskStatus,
    priority: priorityMap[backendTask.priority] || 'medium',
    createdAt: new Date(backendTask.created_at),
    updatedAt: new Date(backendTask.updated_at),
    assignedAgents: [], // 后端暂无此字段
    progress: backendTask.result ? 100 : 0, // 如果有结果，则进度为100%
    metadata: backendTask.result,
  };
}

// 将前端 Task 转换为后端 Task 创建请求
export function adaptTaskToBackend(frontendTask: Partial<Task>, userId: number): any {
  // 将字符串优先级转换为数字优先级
  const priorityMap: Record<string, number> = {
    low: 0,
    medium: 5,
    high: 10,
  };
  
  return {
    description: frontendTask.title || frontendTask.description || '',
    priority: frontendTask.priority ? priorityMap[frontendTask.priority] : 5,
    user_id: userId,
  };
}

// 将前端 Task 更新转换为后端 Task 更新请求
export function adaptTaskUpdateToBackend(updates: Partial<Task>): any {
  const backendUpdates: any = {};
  
  if (updates.title || updates.description) {
    backendUpdates.description = updates.title || updates.description;
  }
  
  if (updates.status) {
    backendUpdates.status = updates.status;
  }
  
  if (updates.priority) {
    const priorityMap: Record<string, number> = {
      low: 0,
      medium: 5,
      high: 10,
    };
    backendUpdates.priority = priorityMap[updates.priority];
  }
  
  return backendUpdates;
} 
 
 
 
 

// 后端 Task 类型
export interface BackendTask {
  id: string;
  description: string;
  status: string;
  priority: number;
  user_id: number;
  created_at: string;
  updated_at: string;
  result?: Record<string, any>;
}

// 将后端 Task 转换为前端 Task
export function adaptTaskFromBackend(backendTask: BackendTask): Task {
  // 将数字优先级转换为字符串优先级
  const priorityMap: Record<number, 'low' | 'medium' | 'high'> = {
    0: 'low',
    5: 'medium',
    10: 'high',
  };
  
  return {
    id: backendTask.id,
    title: backendTask.description, // 后端的 description 对应前端的 title
    description: backendTask.description, // 复用 description
    status: backendTask.status as TaskStatus,
    priority: priorityMap[backendTask.priority] || 'medium',
    createdAt: new Date(backendTask.created_at),
    updatedAt: new Date(backendTask.updated_at),
    assignedAgents: [], // 后端暂无此字段
    progress: backendTask.result ? 100 : 0, // 如果有结果，则进度为100%
    metadata: backendTask.result,
  };
}

// 将前端 Task 转换为后端 Task 创建请求
export function adaptTaskToBackend(frontendTask: Partial<Task>, userId: number): any {
  // 将字符串优先级转换为数字优先级
  const priorityMap: Record<string, number> = {
    low: 0,
    medium: 5,
    high: 10,
  };
  
  return {
    description: frontendTask.title || frontendTask.description || '',
    priority: frontendTask.priority ? priorityMap[frontendTask.priority] : 5,
    user_id: userId,
  };
}

// 将前端 Task 更新转换为后端 Task 更新请求
export function adaptTaskUpdateToBackend(updates: Partial<Task>): any {
  const backendUpdates: any = {};
  
  if (updates.title || updates.description) {
    backendUpdates.description = updates.title || updates.description;
  }
  
  if (updates.status) {
    backendUpdates.status = updates.status;
  }
  
  if (updates.priority) {
    const priorityMap: Record<string, number> = {
      low: 0,
      medium: 5,
      high: 10,
    };
    backendUpdates.priority = priorityMap[updates.priority];
  }
  
  return backendUpdates;
} 
 
 
 
 