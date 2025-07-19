// 任务状态 - 对应后端FSM
export enum TaskStatus {
  PENDING = 'PENDING',
  PLANNING = 'PLANNING',
  EXECUTING = 'EXECUTING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED'
}

// AI智能体类型
export enum AgentRole {
  CHIEF_PROJECT_MANAGER = 'Chief_Project_Manager',
  ENGINEER = 'Engineer',
  TESTER = 'QA_Tester',
  ANALYST = 'Business_Analyst',
  DESIGNER = 'UX_Designer'
}

// 任务实体
export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: 'low' | 'medium' | 'high';
  planId?: string;
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
  assignedAgents: AgentRole[];
  progress: number;
  metadata?: Record<string, any>;
}

// 计划/项目实体
export interface Plan {
  id: string;
  name: string;
  description: string;
  color: string;
  icon?: string;
  createdAt: Date;
  taskIds: string[];
  progress: number;
}

// AI智能体消息
export interface AgentMessage {
  id: string;
  agentRole: AgentRole;
  type: 'thought' | 'action' | 'tool_call' | 'code' | 'result';
  content: string;
  timestamp: Date;
  taskId: string;
  metadata?: {
    toolName?: string;
    codeLanguage?: string;
    error?: boolean;
  };
}

// 用户实体
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  preferences: {
    theme?: 'dark' | 'light';
    accentColor?: string;
    modelPreference?: 'speed' | 'accuracy';
  };
}

// 挑战实体
export interface Challenge {
  id: string;
  title: string;
  description: string;
  category: 'productivity' | 'wellness' | 'learning' | 'creativity';
  progress: number;
  targetValue: number;
  unit: string;
  reward: {
    points: number;
    badge?: string;
  };
} 