import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { Task, Plan, AgentMessage, User, Challenge } from '../types';

interface AppState {
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
        }),
      }
    )
  )
); 