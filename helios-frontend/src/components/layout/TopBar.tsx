import React from 'react';
import { motion } from 'framer-motion';
import { Bell, Search, Sparkles } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';

export const TopBar: React.FC = () => {
  const { user, isAgentWorking } = useAppStore();

  return (
    <header className="h-16 border-b border-helios-border bg-helios-card/50 backdrop-blur-sm">
      <div className="h-full px-6 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-helios-accent-primary bg-opacity-10 rounded-lg flex items-center justify-center">
            <Sparkles size={18} className="text-helios-accent-primary" />
          </div>
          <span className="text-lg font-light text-helios-text-primary">Helios</span>
          
          {/* AI 工作状态指示器 */}
          {isAgentWorking && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-2 ml-4 px-3 py-1 bg-helios-accent-primary bg-opacity-10 rounded-full"
            >
              <div className="w-2 h-2 bg-helios-accent-primary rounded-full animate-breath" />
              <span className="text-xs text-helios-accent-primary">AI 工作中</span>
            </motion.div>
          )}
        </div>

        {/* 右侧操作 */}
        <div className="flex items-center gap-4">
          {/* 搜索按钮 */}
          <button className="text-helios-text-secondary hover:text-helios-text-primary transition-colors">
            <Search size={20} />
          </button>

          {/* 通知按钮 */}
          <button className="relative text-helios-text-secondary hover:text-helios-text-primary transition-colors">
            <Bell size={20} />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-helios-accent-primary rounded-full" />
          </button>

          {/* 用户头像 */}
          <div className="w-8 h-8 bg-helios-accent-primary bg-opacity-20 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-helios-accent-primary">
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}; 
    <header className="h-16 border-b border-helios-border bg-helios-bg flex items-center justify-between px-4 md:px-6">
      {/* 左侧 Logo */}
      <div className="flex items-center">
        <div className="text-helios-accent-primary font-medium text-xl">Helios</div>
      </div>

      {/* 中间搜索框 */}
      <div className="hidden md:flex flex-1 max-w-md mx-4">
        <div className="relative w-full">
          <input
            type="text"
            placeholder="搜索任务..."
            className="input-primary py-2 pl-10"
          />
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-helios-text-tertiary w-5 h-5" />
        </div>
      </div>

      {/* 右侧功能区 */}
      <div className="flex items-center gap-2 md:gap-4">
        <button className="w-9 h-9 rounded-full flex items-center justify-center text-helios-text-secondary hover:text-helios-text-primary hover:bg-helios-card transition-colors">
          <Bell size={20} />
        </button>
        
        <button className="w-9 h-9 rounded-full flex items-center justify-center text-helios-text-secondary hover:text-helios-text-primary hover:bg-helios-card transition-colors">
          <Settings size={20} />
        </button>

        {/* 用户头像 */}
        <button className="w-9 h-9 rounded-full bg-helios-accent-primary bg-opacity-20 flex items-center justify-center">
          <span className="text-sm text-helios-accent-primary font-medium">
            {user?.name?.charAt(0) || 'H'}
          </span>
        </button>
      </div>
    </header>
  );
            <span className="text-sm font-medium text-helios-accent-primary">
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}; 
    <header className="h-16 border-b border-helios-border bg-helios-bg flex items-center justify-between px-4 md:px-6">
      {/* 左侧 Logo */}
      <div className="flex items-center">
        <div className="text-helios-accent-primary font-medium text-xl">Helios</div>
      </div>

      {/* 中间搜索框 */}
      <div className="hidden md:flex flex-1 max-w-md mx-4">
        <div className="relative w-full">
          <input
            type="text"
            placeholder="搜索任务..."
            className="input-primary py-2 pl-10"
          />
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-helios-text-tertiary w-5 h-5" />
        </div>
      </div>

      {/* 右侧功能区 */}
      <div className="flex items-center gap-2 md:gap-4">
        <button className="w-9 h-9 rounded-full flex items-center justify-center text-helios-text-secondary hover:text-helios-text-primary hover:bg-helios-card transition-colors">
          <Bell size={20} />
        </button>
        
        <button className="w-9 h-9 rounded-full flex items-center justify-center text-helios-text-secondary hover:text-helios-text-primary hover:bg-helios-card transition-colors">
          <Settings size={20} />
        </button>

        {/* 用户头像 */}
        <button className="w-9 h-9 rounded-full bg-helios-accent-primary bg-opacity-20 flex items-center justify-center">
          <span className="text-sm text-helios-accent-primary font-medium">
            {user?.name?.charAt(0) || 'H'}
          </span>
        </button>
      </div>
    </header>
  );