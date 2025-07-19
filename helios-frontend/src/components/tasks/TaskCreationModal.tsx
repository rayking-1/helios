import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Calendar, Flag, Users } from 'lucide-react';
import { Button } from '../common/Button';
import { useAppStore } from '../../store/useAppStore';
import { Task, TaskStatus, AgentRole } from '../../types';

interface TaskCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
  planId?: string;
}

export const TaskCreationModal: React.FC<TaskCreationModalProps> = ({
  isOpen,
  onClose,
  planId
}) => {
  const { addTask, setAgentWorking } = useAppStore();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [dueDate, setDueDate] = useState('');
  const [selectedAgents, setSelectedAgents] = useState<AgentRole[]>([
    AgentRole.CHIEF_PROJECT_MANAGER
  ]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const newTask: Task = {
      id: `task-${Date.now()}`,
      title,
      description,
      status: TaskStatus.PENDING,
      priority,
      planId,
      createdAt: new Date(),
      updatedAt: new Date(),
      dueDate: dueDate ? new Date(dueDate) : undefined,
      assignedAgents: selectedAgents,
      progress: 0,
    };

    addTask(newTask);
    setAgentWorking(true);
    
    // 模拟AI开始处理
    setTimeout(() => {
      setAgentWorking(false);
    }, 3000);

    onClose();
    resetForm();
  };

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setPriority('medium');
    setDueDate('');
    setSelectedAgents([AgentRole.CHIEF_PROJECT_MANAGER]);
  };

  const priorityOptions = [
    { value: 'low', label: '低', color: 'text-gray-400' },
    { value: 'medium', label: '中', color: 'text-helios-accent-warning' },
    { value: 'high', label: '高', color: 'text-red-400' },
  ];

  const agentOptions = Object.values(AgentRole).map(role => ({
    value: role,
    label: role.replace(/_/g, ' '),
  }));

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 背景遮罩 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
          />

          {/* 模态框 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-x-4 top-1/2 -translate-y-1/2 max-w-2xl mx-auto z-50"
          >
            <div className="bg-helios-card rounded-2xl p-6 border border-helios-border">
              {/* 标题栏 */}
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-light text-helios-text-primary">
                  创建新任务
                </h3>
                <button
                  onClick={onClose}
                  className="text-helios-text-secondary hover:text-helios-text-primary transition-colors"
                >
                  <X size={24} />
                </button>
              </div>

              {/* 表单 */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* 任务标题 */}
                <div>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="任务目标..."
                    className="input-primary text-lg"
                    required
                    autoFocus
                  />
                </div>

                {/* 任务描述 */}
                <div>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="详细描述（可选）..."
                    className="input-primary min-h-[100px] resize-none"
                    rows={3}
                  />
                </div>

                {/* 属性设置 */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* 优先级 */}
                  <div>
                    <label className="block text-sm text-helios-text-secondary mb-2">
                      <Flag size={16} className="inline mr-1" />
                      优先级
                    </label>
                    <div className="flex gap-2">
                      {priorityOptions.map(({ value, label, color }) => (
                        <button
                          key={value}
                          type="button"
                          onClick={() => setPriority(value as any)}
                          className={`
                            flex-1 py-2 px-3 rounded-lg border transition-all
                            ${priority === value
                              ? 'border-helios-accent-primary bg-helios-accent-primary bg-opacity-10'
                              : 'border-helios-border hover:border-helios-text-tertiary'
                            }
                          `}
                        >
                          <span className={priority === value ? color : 'text-helios-text-secondary'}>
                            {label}
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* 截止日期 */}
                  <div>
                    <label className="block text-sm text-helios-text-secondary mb-2">
                      <Calendar size={16} className="inline mr-1" />
                      截止日期
                    </label>
                    <input
                      type="date"
                      value={dueDate}
                      onChange={(e) => setDueDate(e.target.value)}
                      className="input-primary"
                      min={new Date().toISOString().split('T')[0]}
                    />
                  </div>

                  {/* AI智能体选择 */}
                  <div>
                    <label className="block text-sm text-helios-text-secondary mb-2">
                      <Users size={16} className="inline mr-1" />
                      分配智能体
                    </label>
                    <select
                      multiple
                      value={selectedAgents}
                      onChange={(e) => {
                        const selected = Array.from(e.target.selectedOptions, option => option.value as AgentRole);
                        setSelectedAgents(selected);
                      }}
                      className="input-primary"
                      size={3}
                    >
                      {agentOptions.map(({ value, label }) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* 提交按钮 */}
                <div className="flex gap-3 pt-4">
                  <Button type="submit" variant="primary" className="flex-1">
                    启动 AI 团队
                  </Button>
                  <Button type="button" variant="secondary" onClick={onClose}>
                    取消
                  </Button>
                </div>
              </form>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}; 