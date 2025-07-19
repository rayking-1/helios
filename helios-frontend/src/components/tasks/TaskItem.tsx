import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Check, Clock, AlertCircle, MoreVertical, Trash2, Edit } from 'lucide-react';
import { Task, TaskStatus } from '../../types';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

interface TaskItemProps {
  task: Task;
  onUpdate?: (id: string, updates: Partial<Task>) => void;
  onDelete?: (id: string) => void;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete }) => {
  const [showMenu, setShowMenu] = useState(false);

  const statusIcons = {
    [TaskStatus.PENDING]: <Clock size={16} className="text-helios-text-secondary" />,
    [TaskStatus.PLANNING]: <AlertCircle size={16} className="text-helios-accent-warning" />,
    [TaskStatus.EXECUTING]: <div className="w-4 h-4 border-2 border-helios-accent-primary border-t-transparent rounded-full animate-spin" />,
    [TaskStatus.COMPLETED]: <Check size={16} className="text-helios-accent-success" />,
    [TaskStatus.FAILED]: <AlertCircle size={16} className="text-red-400" />,
  };

  const priorityColors = {
    low: 'bg-gray-600',
    medium: 'bg-helios-accent-warning',
    high: 'bg-red-400',
  };

  const handleToggleComplete = () => {
    if (onUpdate) {
      onUpdate(task.id, {
        status: task.status === TaskStatus.COMPLETED ? TaskStatus.PENDING : TaskStatus.COMPLETED,
      });
    }
  };

  return (
    <div className="group relative">
      <motion.div
        whileHover={{ x: 4 }}
        className="card p-4 flex items-center gap-4 cursor-pointer"
        onClick={handleToggleComplete}
      >
        {/* 状态图标 */}
        <div className="flex-shrink-0">
          {statusIcons[task.status]}
        </div>

        {/* 任务内容 */}
        <div className="flex-1 min-w-0">
          <h4 className={`text-helios-text-primary ${
            task.status === TaskStatus.COMPLETED ? 'line-through opacity-60' : ''
          }`}>
            {task.title}
          </h4>
          
          {task.description && (
            <p className="text-sm text-helios-text-secondary mt-1 truncate">
              {task.description}
            </p>
          )}

          {/* 元信息 */}
          <div className="flex items-center gap-4 mt-2">
            {/* 优先级 */}
            <div className="flex items-center gap-1">
              <div className={`w-2 h-2 rounded-full ${priorityColors[task.priority]}`} />
              <span className="text-xs text-helios-text-tertiary capitalize">
                {task.priority}
              </span>
            </div>

            {/* 截止日期 */}
            {task.dueDate && (
              <span className="text-xs text-helios-text-tertiary">
                {format(new Date(task.dueDate), 'MM/dd', { locale: zhCN })}
              </span>
            )}

            {/* 进度 */}
            {task.progress > 0 && task.progress < 100 && (
              <div className="flex items-center gap-2">
                <div className="w-16 h-1 bg-helios-border rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-helios-accent-primary"
                    initial={{ width: 0 }}
                    animate={{ width: `${task.progress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
                <span className="text-xs text-helios-text-tertiary">
                  {task.progress}%
                </span>
              </div>
            )}
          </div>
        </div>

        {/* 操作菜单 */}
        <div className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowMenu(!showMenu);
            }}
            className="p-2 hover:bg-helios-bg rounded-lg transition-colors"
          >
            <MoreVertical size={16} className="text-helios-text-secondary" />
          </button>
        </div>
      </motion.div>

      {/* 下拉菜单 */}
      {showMenu && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="absolute right-4 top-12 bg-helios-card border border-helios-border rounded-lg shadow-xl z-10 py-1 min-w-[120px]"
        >
          <button
            onClick={() => {
              // 编辑功能
              setShowMenu(false);
            }}
            className="w-full px-4 py-2 text-left text-sm text-helios-text-primary hover:bg-helios-bg transition-colors flex items-center gap-2"
          >
            <Edit size={14} />
            编辑
          </button>
          
          <button
            onClick={() => {
              if (onDelete) onDelete(task.id);
              setShowMenu(false);
            }}
            className="w-full px-4 py-2 text-left text-sm text-red-400 hover:bg-helios-bg transition-colors flex items-center gap-2"
          >
            <Trash2 size={14} />
            删除
          </button>
        </motion.div>
      )}
    </div>
  );
}; 