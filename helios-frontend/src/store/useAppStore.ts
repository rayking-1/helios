import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// 定义接口
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

export interface AgentMessage {
  agentName: string;
  message: string;
  timestamp: string;
}

interface AppState {
  // 用户信息
  user: {
    id: string;
    name: string;
    isAuthenticated: boolean;
  };
  
  // 计划数据
  currentPlan: Plan | null;
  planHistory: Plan[];
  
  // 智能体消息
  agentMessages: AgentMessage[];
  
  // 系统状态
  systemStatus: {
    status: 'IDLE' | 'PLANNING' | 'ERROR' | string;
    details: string | null;
    lastUpdated: string | null;
  };
  
  // 操作方法
  setUser: (id: string, name: string) => void;
  logout: () => void;
  updatePlan: (plan: Plan) => void;
  addAgentMessage: (message: AgentMessage) => void;
  clearAgentMessages: () => void;
  updateSystemStatus: (status: string, details?: string | null) => void;
  updateTaskStatus: (taskId: string, status: Task['status']) => void;
}

// 创建Zustand store
export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // 初始状态
      user: {
        id: '',
        name: '',
        isAuthenticated: false,
      },
      
      currentPlan: null,
      planHistory: [],
      
      agentMessages: [],
      
      systemStatus: {
        status: 'IDLE',
        details: null,
        lastUpdated: null,
      },
      
      // 用户操作
      setUser: (id: string, name: string) => set({
        user: {
          id,
          name,
          isAuthenticated: true,
        }
      }),
      
      logout: () => set({
        user: {
          id: '',
          name: '',
          isAuthenticated: false,
        },
        currentPlan: null,
        planHistory: [],
        agentMessages: [],
      }),
      
      // 计划更新
      updatePlan: (plan: Plan) => set((state) => {
        // 如果有现有计划，将其添加到历史记录
        const updatedHistory = state.currentPlan 
          ? [...state.planHistory, state.currentPlan] 
          : state.planHistory;
        
        // 最多保留5条历史记录
        const limitedHistory = updatedHistory.slice(-5);
        
        return {
          currentPlan: plan,
          planHistory: limitedHistory,
        };
      }),
      
      // 添加代理消息
      addAgentMessage: (message: AgentMessage) => set((state) => ({
        agentMessages: [...state.agentMessages, {
          ...message,
          // 如果消息没有时间戳，添加当前时间
          timestamp: message.timestamp || new Date().toISOString(),
        }],
      })),
      
      // 清除代理消息
      clearAgentMessages: () => set({
        agentMessages: []
      }),
      
      // 更新系统状态
      updateSystemStatus: (status: string, details: string | null = null) => set({
        systemStatus: {
          status,
          details,
          lastUpdated: new Date().toISOString(),
        }
      }),
      
      // 更新任务状态
      updateTaskStatus: (taskId: string, status: Task['status']) => set((state) => {
        if (!state.currentPlan) return {};
        
        const updatedTasks = state.currentPlan.tasks.map(task => 
          task.taskId === taskId ? { ...task, status } : task
        );
        
        return {
          currentPlan: {
            ...state.currentPlan,
            tasks: updatedTasks,
          }
        };
      }),
    }),
    {
      name: 'helios-store', // localStorage的键名
      partialize: (state) => ({
        // 只保存用户信息和当前计划到localStorage
        user: state.user,
        currentPlan: state.currentPlan,
      }),
    }
  )
);

// 导出简单的选择器
export const useUser = () => useAppStore(state => state.user);
export const useCurrentPlan = () => useAppStore(state => state.currentPlan);
export const useAgentMessages = () => useAppStore(state => state.agentMessages);
export const useSystemStatus = () => useAppStore(state => state.systemStatus); 
  // 用户状态
  user: User | null;
  setUser: (user: User | null) => void;
  
  // 任务状态
  tasks: Task[];
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  
  // 计划状态
  plans: Plan[];
  addPlan: (plan: Plan) => void;
  updatePlan: (id: string, updates: Partial<Plan>) => void;
  deletePlan: (id: string) => void;
  
  // 当前活动计划 - 适应性规划系统
  plan: string | null;
  setPlan: (plan: string | null) => void;
  
  // 对话历史 - 适应性规划系统
  conversationHistory: any[];
  setConversationHistory: (history: any[]) => void;
  addToConversationHistory: (message: any) => void;
  
  // AI智能体状态
  agentMessages: AgentMessage[];
  addAgentMessage: (message: AgentMessage) => void;
  clearAgentMessages: (taskId: string) => void;
  
  // 挑战状态
  challenges: Challenge[];
  updateChallengeProgress: (id: string, progress: number) => void;
  
  // UI状态
  activeView: 'planner' | 'challenge' | 'ai' | 'treehole';
  setActiveView: (view: AppState['activeView']) => void;
  isAgentWorking: boolean;
  setAgentWorking: (working: boolean) => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        // 初始状态
        user: null,
        tasks: [],
        plans: [],
        agentMessages: [],
        challenges: [],
        activeView: 'planner',
        isAgentWorking: false,
        plan: null,
        conversationHistory: [],
        
        // Actions
        setUser: (user) => set({ user }),
        
        addTask: (task) => set((state) => ({ 
          tasks: [...state.tasks, task] 
        })),
        
        updateTask: (id, updates) => set((state) => ({
          tasks: state.tasks.map(task => 
            task.id === id ? { ...task, ...updates, updatedAt: new Date() } : task
          )
        })),
        
        deleteTask: (id) => set((state) => ({
          tasks: state.tasks.filter(task => task.id !== id)
        })),
        
        addPlan: (plan) => set((state) => ({
          plans: [...state.plans, plan]
        })),
        
        updatePlan: (id, updates) => set((state) => ({
          plans: state.plans.map(plan =>
            plan.id === id ? { ...plan, ...updates } : plan
          )
        })),
        
        deletePlan: (id) => set((state) => ({
          plans: state.plans.filter(plan => plan.id !== id)
        })),
        
        // 适应性规划系统 - 当前计划
        setPlan: (plan) => set({ plan }),
        
        // 适应性规划系统 - 对话历史
        setConversationHistory: (history) => set({ conversationHistory: history }),
        
        addToConversationHistory: (message) => set((state) => ({
          conversationHistory: [...state.conversationHistory, message]
        })),
        
        addAgentMessage: (message) => set((state) => ({
          agentMessages: [...state.agentMessages, message]
        })),
        
        clearAgentMessages: (taskId) => set((state) => ({
          agentMessages: state.agentMessages.filter(msg => msg.taskId !== taskId)
        })),
        
        updateChallengeProgress: (id, progress) => set((state) => ({
          challenges: state.challenges.map(challenge =>
            challenge.id === id ? { ...challenge, progress } : challenge
          )
        })),
        
        setActiveView: (view) => set({ activeView: view }),
        setAgentWorking: (working) => set({ isAgentWorking: working }),
      }),
      {
        name: 'helios-storage',
        partialize: (state) => ({ 
          user: state.user,
          tasks: state.tasks,
          plans: state.plans,
          plan: state.plan,
          conversationHistory: state.conversationHistory,
        }),
      }
    )
  )
); 
        systemStatus: {
          status,
          details,
          lastUpdated: new Date().toISOString(),
        }
      }),
      
      // 更新任务状态
      updateTaskStatus: (taskId: string, status: Task['status']) => set((state) => {
        if (!state.currentPlan) return {};
        
        const updatedTasks = state.currentPlan.tasks.map(task => 
          task.taskId === taskId ? { ...task, status } : task
        );
        
        return {
          currentPlan: {
            ...state.currentPlan,
            tasks: updatedTasks,
          }
        };
      }),
    }),
    {
      name: 'helios-store', // localStorage的键名
      partialize: (state) => ({
        // 只保存用户信息和当前计划到localStorage
        user: state.user,
        currentPlan: state.currentPlan,
      }),
    }
  )
);

// 导出简单的选择器
export const useUser = () => useAppStore(state => state.user);
export const useCurrentPlan = () => useAppStore(state => state.currentPlan);
export const useAgentMessages = () => useAppStore(state => state.agentMessages);
export const useSystemStatus = () => useAppStore(state => state.systemStatus); 
  // 用户状态
  user: User | null;
  setUser: (user: User | null) => void;
  
  // 任务状态
  tasks: Task[];
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  
  // 计划状态
  plans: Plan[];
  addPlan: (plan: Plan) => void;
  updatePlan: (id: string, updates: Partial<Plan>) => void;
  deletePlan: (id: string) => void;
  
  // 当前活动计划 - 适应性规划系统
  plan: string | null;
  setPlan: (plan: string | null) => void;
  
  // 对话历史 - 适应性规划系统
  conversationHistory: any[];
  setConversationHistory: (history: any[]) => void;
  addToConversationHistory: (message: any) => void;
  
  // AI智能体状态
  agentMessages: AgentMessage[];
  addAgentMessage: (message: AgentMessage) => void;
  clearAgentMessages: (taskId: string) => void;
  
  // 挑战状态
  challenges: Challenge[];
  updateChallengeProgress: (id: string, progress: number) => void;
  
  // UI状态
  activeView: 'planner' | 'challenge' | 'ai' | 'treehole';
  setActiveView: (view: AppState['activeView']) => void;
  isAgentWorking: boolean;
  setAgentWorking: (working: boolean) => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        // 初始状态
        user: null,
        tasks: [],
        plans: [],
        agentMessages: [],
        challenges: [],
        activeView: 'planner',
        isAgentWorking: false,
        plan: null,
        conversationHistory: [],
        
        // Actions
        setUser: (user) => set({ user }),
        
        addTask: (task) => set((state) => ({ 
          tasks: [...state.tasks, task] 
        })),
        
        updateTask: (id, updates) => set((state) => ({
          tasks: state.tasks.map(task => 
            task.id === id ? { ...task, ...updates, updatedAt: new Date() } : task
          )
        })),
        
        deleteTask: (id) => set((state) => ({
          tasks: state.tasks.filter(task => task.id !== id)
        })),
        
        addPlan: (plan) => set((state) => ({
          plans: [...state.plans, plan]
        })),
        
        updatePlan: (id, updates) => set((state) => ({
          plans: state.plans.map(plan =>
            plan.id === id ? { ...plan, ...updates } : plan
          )
        })),
        
        deletePlan: (id) => set((state) => ({
          plans: state.plans.filter(plan => plan.id !== id)
        })),
        
        // 适应性规划系统 - 当前计划
        setPlan: (plan) => set({ plan }),
        
        // 适应性规划系统 - 对话历史
        setConversationHistory: (history) => set({ conversationHistory: history }),
        
        addToConversationHistory: (message) => set((state) => ({
          conversationHistory: [...state.conversationHistory, message]
        })),
        
        addAgentMessage: (message) => set((state) => ({
          agentMessages: [...state.agentMessages, message]
        })),
        
        clearAgentMessages: (taskId) => set((state) => ({
          agentMessages: state.agentMessages.filter(msg => msg.taskId !== taskId)
        })),
        
        updateChallengeProgress: (id, progress) => set((state) => ({
          challenges: state.challenges.map(challenge =>
            challenge.id === id ? { ...challenge, progress } : challenge
          )
        })),
        
        setActiveView: (view) => set({ activeView: view }),
        setAgentWorking: (working) => set({ isAgentWorking: working }),
      }),
      {
        name: 'helios-storage',
        partialize: (state) => ({ 
          user: state.user,
          tasks: state.tasks,
          plans: state.plans,
          plan: state.plan,
          conversationHistory: state.conversationHistory,
        }),
      }
    )
  )
); 