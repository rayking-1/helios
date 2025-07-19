import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, Trophy, Brain, MessageCircle, User } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';

const tabs = [
  { id: 'planner', label: '计划', icon: Calendar },
  { id: 'challenge', label: '挑战', icon: Trophy },
  { id: 'ai', label: 'AI', icon: Brain },
  { id: 'treehole', label: '树洞', icon: MessageCircle },
] as const;

export const TabBar: React.FC = () => {
  const { activeView, setActiveView } = useAppStore();

  return (
    <nav className="border-t border-helios-border bg-helios-card">
      <div className="flex justify-around items-center h-16 max-w-lg mx-auto">
        {tabs.map(({ id, label, icon: Icon }) => (
          <motion.button
            key={id}
            onClick={() => setActiveView(id)}
            className="relative flex flex-col items-center justify-center w-full h-full"
            whileTap={{ scale: 0.95 }}
          >
            {activeView === id && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-helios-accent-primary bg-opacity-10"
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
            )}
            
            <Icon 
              size={20} 
              className={`mb-1 transition-colors duration-200 ${
                activeView === id 
                  ? 'text-helios-accent-primary' 
                  : 'text-helios-text-secondary'
              }`}
            />
            
            <span className={`text-xs transition-colors duration-200 ${
              activeView === id 
                ? 'text-helios-accent-primary' 
                : 'text-helios-text-tertiary'
            }`}>
              {label}
            </span>
          </motion.button>
        ))}
        
        {/* 个人中心 */}
        <button className="flex flex-col items-center justify-center w-full h-full">
          <User size={20} className="mb-1 text-helios-text-secondary" />
          <span className="text-xs text-helios-text-tertiary">我</span>
        </button>
      </div>
    </nav>
  );
}; 