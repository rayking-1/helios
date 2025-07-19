import React from 'react';
import { motion } from 'framer-motion';
import { Folder, MoreVertical } from 'lucide-react';
import { Plan } from '../../types';

interface PlanCardProps {
  plan: Plan;
  taskCount: number;
  onClick?: () => void;
}

export const PlanCard: React.FC<PlanCardProps> = ({ plan, taskCount, onClick }) => {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="card h-48 cursor-pointer relative overflow-hidden group"
    >
      {/* 背景装饰 */}
      <div 
        className="absolute inset-0 opacity-5"
        style={{
          background: `linear-gradient(135deg, ${plan.color} 0%, transparent 100%)`
        }}
      />

      {/* 内容 */}
      <div className="relative h-full flex flex-col">
        <div className="flex items-start justify-between mb-4">
          <div 
            className="p-3 rounded-lg"
            style={{ backgroundColor: `${plan.color}20` }}
          >
            <Folder size={24} style={{ color: plan.color }} />
          </div>
          <button 
            onClick={(e) => {
              e.stopPropagation();
              // 打开计划菜单
            }}
            className="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-helios-bg rounded"
          >
            <MoreVertical size={16} className="text-helios-text-secondary" />
          </button>
        </div>

        <h3 className="text-lg font-medium text-helios-text-primary mb-2">
          {plan.name}
        </h3>
        
        <p className="text-sm text-helios-text-secondary flex-1 line-clamp-2">
          {plan.description}
        </p>

        <div className="flex items-center justify-between mt-4">
          <span className="text-sm text-helios-text-tertiary">
            {taskCount} 个任务
          </span>
          <div className="flex items-center gap-2">
            <div className="w-16 h-1 bg-helios-border rounded-full overflow-hidden">
              <div 
                className="h-full transition-all duration-500"
                style={{
                  width: `${plan.progress}%`,
                  backgroundColor: plan.color
                }}
              />
            </div>
            <span className="text-xs text-helios-text-tertiary">
              {plan.progress}%
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}; 