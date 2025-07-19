import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';

export const LoginPage: React.FC = () => {
  const { setUser } = useAppStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // 模拟登录请求
    setTimeout(() => {
      setUser({
        id: '1',
        email: email,
        name: 'Helios 用户',
        preferences: {}
      });
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-helios-bg flex items-center justify-center p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-light text-helios-accent-primary">Helios</h1>
          <p className="text-helios-text-secondary mt-2">AI智能体协作系统</p>
        </div>
        
        {/* 登录表单 */}
        <div className="bg-helios-card rounded-xl border border-helios-border p-8">
          <h2 className="text-xl font-light text-helios-text-primary mb-6">登录</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm text-helios-text-secondary mb-1">
                邮箱
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-primary"
                placeholder="your@email.com"
                required
              />
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm text-helios-text-secondary mb-1">
                密码
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-primary"
                placeholder="••••••••"
                required
              />
            </div>
            
            <div className="pt-2">
              <button
                type="submit"
                disabled={isLoading}
                className={`
                  w-full py-3 px-4 rounded-lg font-medium transition-all
                  bg-helios-accent-primary text-white
                  ${isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-opacity-90'}
                `}
              >
                {isLoading ? '登录中...' : '登录'}
              </button>
            </div>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-sm text-helios-text-tertiary">
              演示账号可使用任意邮箱和密码登录
            </p>
          </div>
        </div>
        
        {/* 底部信息 */}
        <div className="mt-8 text-center text-xs text-helios-text-tertiary">
          <p>© {new Date().getFullYear()} Helios AI 协作平台</p>
        </div>
      </motion.div>
    </div>
  );
}; 