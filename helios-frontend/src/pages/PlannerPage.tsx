import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Plus, Calendar, ChevronRight, Clock, Target } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import { TaskCreationModal } from '../components/tasks/TaskCreationModal';
import { Button } from '../components/common/Button';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

export const PlannerPage: React.FC = () => {
  const { tasks, plans } = useAppStore();
  const [isCreatingTask, setIsCreatingTask] = useState(false);
  const [selectedPlanId, setSelectedPlanId] = useState<string | undefined>();
  const [viewMode, setViewMode] = useState<'timeline' | 'plans'>('timeline');

  // 任务分组
  const groupedTasks = useMemo(() => {
    const today = tasks.filter(t => t.dueDate && isToday(new Date(t.dueDate)));
    const tomorrow = tasks.filter(t => t.dueDate && isTomorrow(new Date(t.dueDate)));
    const thisWeek = tasks.filter(t => t.dueDate && isThisWeek(new Date(t.dueDate)) && !isToday(new Date(t.dueDate)) && !isTomorrow(new Date(t.dueDate)));
    const noDueDate = tasks.filter(t => !t.dueDate);

    return { today, tomorrow, thisWeek, noDueDate };
  }, [tasks]);

  // 今日统计
  const todayStats = {
    total: groupedTasks.today.length,
    completed: groupedTasks.today.filter(t => t.status === 'COMPLETED').length,
    inProgress: groupedTasks.today.filter(t => t.status === 'EXECUTING').length,
  };

  // 辅助函数
  const isToday = (date: Date) => {
    const today = new Date();
    return date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear();
  };

  const isTomorrow = (date: Date) => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return date.getDate() === tomorrow.getDate() &&
      date.getMonth() === tomorrow.getMonth() &&
      date.getFullYear() === tomorrow.getFullYear();
  };

  const isThisWeek = (date: Date) => {
    const today = new Date();
    const weekStart = new Date(today);
    weekStart.setDate(today.getDate() - today.getDay());
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);
    
    return date >= weekStart && date <= weekEnd;
  };

  return (
    <div className="h-full overflow-y-auto bg-helios-bg">
      {/* 页面头部 */}
      <div className="p-6 border-b border-helios-border bg-helios-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-light text-helios-text-primary">
              {format(new Date(), 'M月d日 EEEE', { locale: zhCN })}
            </h1>
            <p className="text-helios-text-secondary mt-1">
              今日 {todayStats.total} 项任务，已完成 {todayStats.completed} 项
            </p>
          </div>
          
          <Button
            variant="primary"
            icon={<Plus size={20} />}
            onClick={() => setIsCreatingTask(true)}
          >
            新任务
          </Button>
        </div>

        {/* 视图切换 */}
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('timeline')}
            className={`px-4 py-2 rounded-lg transition-all ${
              viewMode === 'timeline'
                ? 'bg-helios-accent-primary bg-opacity-10 text-helios-accent-primary'
                : 'text-helios-text-secondary hover:text-helios-text-primary'
            }`}
          >
            时间线
          </button>
          <button
            onClick={() => setViewMode('plans')}
            className={`px-4 py-2 rounded-lg transition-all ${
              viewMode === 'plans'
                ? 'bg-helios-accent-primary bg-opacity-10 text-helios-accent-primary'
                : 'text-helios-text-secondary hover:text-helios-text-primary'
            }`}
          >
            计划
          </button>
        </div>
      </div>

      {/* 主内容区 */}
      <div className="p-6">
        {viewMode === 'timeline' ? (
          <div className="space-y-8">
            {/* 今日任务 */}
            {groupedTasks.today.length > 0 && (
              <TaskSection
                title="今日"
                icon={<Clock size={20} />}
                tasks={groupedTasks.today}
                accentColor="text-helios-accent-primary"
              />
            )}

            {/* 明日任务 */}
            {groupedTasks.tomorrow.length > 0 && (
              <TaskSection
                title="明日"
                icon={<Calendar size={20} />}
                tasks={groupedTasks.tomorrow}
                accentColor="text-helios-accent-secondary"
              />
            )}

            {/* 本周任务 */}
            {groupedTasks.thisWeek.length > 0 && (
              <TaskSection
                title="本周"
                icon={<Target size={20} />}
                tasks={groupedTasks.thisWeek}
                accentColor="text-helios-accent-warning"
              />
            )}

            {/* 无日期任务 */}
            {groupedTasks.noDueDate.length > 0 && (
              <TaskSection
                title="未安排"
                tasks={groupedTasks.noDueDate}
                accentColor="text-helios-text-secondary"
              />
            )}

            {/* 空状态 */}
            {tasks.length === 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center py-16"
              >
                <div className="inline-flex items-center justify-center w-24 h-24 bg-helios-card rounded-full mb-6">
                  <Calendar size={40} className="text-helios-accent-primary" />
                </div>
                <h3 className="text-xl font-light text-helios-text-primary mb-2">
                  开始新的一天
                </h3>
                <p className="text-helios-text-secondary mb-6">
                  创建您的第一个任务，让 AI 团队开始工作
                </p>
                <Button
                  variant="primary"
                  icon={<Plus size={20} />}
                  onClick={() => setIsCreatingTask(true)}
                >
                  创建任务
                </Button>
              </motion.div>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {plans.map(plan => (
              <PlanCard 
                key={plan.id} 
                plan={plan} 
                onClick={() => setSelectedPlanId(plan.id)}
              />
            ))}
            
            {/* 添加计划卡片 */}
            <button 
              className="h-48 rounded-xl border border-dashed border-helios-border flex flex-col items-center justify-center gap-3 text-helios-text-secondary hover:text-helios-text-primary hover:border-helios-text-tertiary transition-all"
            >
              <Plus size={24} />
              <span>新建计划</span>
            </button>
          </div>
        )}
      </div>

      {/* 任务创建模态框 */}
      <TaskCreationModal
        isOpen={isCreatingTask}
        onClose={() => setIsCreatingTask(false)}
        planId={selectedPlanId}
      />
    </div>
  );
};

// 任务分组组件
const TaskSection: React.FC<{
  title: string;
  icon?: React.ReactNode;
  tasks: any[];
  accentColor: string;
}> = ({ title, icon, tasks, accentColor }) => {
  return (
    <div>
      <div className="flex items-center gap-2 mb-4">
        {icon && <span className={accentColor}>{icon}</span>}
        <h2 className={`text-lg font-medium ${accentColor}`}>{title}</h2>
        <span className="text-helios-text-tertiary text-sm ml-2">
          {tasks.length} 项任务
        </span>
      </div>
      
      <div className="space-y-3">
        {tasks.map(task => (
          <TaskItem key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
};

// 任务项组件
const TaskItem: React.FC<{ task: any }> = ({ task }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-helios-card rounded-lg border border-helios-border p-4 hover:border-helios-text-tertiary transition-all"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <input 
            type="checkbox" 
            checked={task.status === 'COMPLETED'}
            className="w-5 h-5 rounded-full border-2 border-helios-border checked:bg-helios-accent-primary checked:border-transparent focus:ring-0 focus:ring-offset-0 transition-colors"
          />
          <span className={`font-medium ${task.status === 'COMPLETED' ? 'text-helios-text-tertiary line-through' : 'text-helios-text-primary'}`}>
            {task.title}
          </span>
        </div>
        
        <ChevronRight size={18} className="text-helios-text-tertiary" />
      </div>
      
      {task.description && (
        <p className="text-helios-text-secondary text-sm ml-8 mt-2 line-clamp-1">
          {task.description}
        </p>
      )}
    </motion.div>
  );
};

// 计划卡片组件
const PlanCard: React.FC<{ plan: any; onClick: () => void }> = ({ plan, onClick }) => {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="bg-helios-card rounded-xl border border-helios-border p-6 cursor-pointer hover:border-helios-text-tertiary transition-all"
    >
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-medium text-helios-text-primary">{plan.name}</h3>
        <div 
          className="w-8 h-8 rounded-full flex items-center justify-center"
          style={{ backgroundColor: plan.color }}
        >
          {plan.icon || <Calendar size={16} className="text-white" />}
        </div>
      </div>
      
      <p className="text-helios-text-secondary mb-6 line-clamp-2">
        {plan.description}
      </p>
      
      <div className="flex justify-between items-center">
        <div className="text-sm text-helios-text-tertiary">
          {plan.taskIds.length} 项任务
        </div>
        
        <div className="w-full max-w-[120px] bg-helios-border rounded-full h-1.5">
          <div 
            className="h-1.5 rounded-full" 
            style={{ 
              width: `${plan.progress}%`,
              backgroundColor: plan.color
            }}
          />
        </div>
      </div>
    </motion.div>
  );
}; 