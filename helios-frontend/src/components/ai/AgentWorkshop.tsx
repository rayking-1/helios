import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Code, Zap, CheckCircle, AlertCircle } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { AgentMessage, AgentRole } from '../../types';

const agentIcons: Record<AgentRole, React.ElementType> = {
  [AgentRole.CHIEF_PROJECT_MANAGER]: Bot,
  [AgentRole.ENGINEER]: Code,
  [AgentRole.TESTER]: CheckCircle,
  [AgentRole.ANALYST]: Zap,
  [AgentRole.DESIGNER]: AlertCircle,
};

const agentColors: Record<AgentRole, string> = {
  [AgentRole.CHIEF_PROJECT_MANAGER]: 'text-helios-accent-primary',
  [AgentRole.ENGINEER]: 'text-helios-accent-secondary',
  [AgentRole.TESTER]: 'text-helios-accent-success',
  [AgentRole.ANALYST]: 'text-helios-accent-warning',
  [AgentRole.DESIGNER]: 'text-helios-text-primary',
};

export const AgentWorkshop: React.FC = () => {
  const { agentMessages, isAgentWorking } = useAppStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [agentMessages]);

  return (
    <div className="h-full flex flex-col bg-helios-bg">
      {/* 标题栏 */}
      <div className="p-6 border-b border-helios-border">
        <h2 className="text-2xl font-light text-helios-text-primary">AI 工作坊</h2>
        <p className="text-helios-text-secondary mt-1">实时查看AI团队的协作过程</p>
      </div>

      {/* 消息流 */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <AnimatePresence initial={false}>
          {agentMessages.map((message) => (
            <MessageItem key={message.id} message={message} />
          ))}
        </AnimatePresence>

        {/* 工作状态指示器 */}
        {isAgentWorking && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-3 text-helios-text-secondary"
          >
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-helios-accent-primary rounded-full animate-breath" />
              <span className="w-2 h-2 bg-helios-accent-primary rounded-full animate-breath delay-100" />
              <span className="w-2 h-2 bg-helios-accent-primary rounded-full animate-breath delay-200" />
            </div>
            <span className="text-sm">AI团队正在思考...</span>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

const MessageItem: React.FC<{ message: AgentMessage }> = ({ message }) => {
  const Icon = agentIcons[message.agentRole];
  const colorClass = agentColors[message.agentRole];

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      transition={{ duration: 0.3 }}
      className="flex gap-4"
    >
      {/* 智能体头像 */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full bg-helios-card flex items-center justify-center ${colorClass}`}>
        <Icon size={20} />
      </div>

      {/* 消息内容 */}
      <div className="flex-1">
        <div className="flex items-baseline gap-2 mb-1">
          <span className={`font-medium ${colorClass}`}>
            {message.agentRole.replace(/_/g, ' ')}
          </span>
          <span className="text-xs text-helios-text-tertiary">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>

        <div className={`
          ${message.type === 'code' ? 'font-mono bg-helios-card p-3 rounded-lg' : ''}
          ${message.type === 'thought' ? 'italic text-helios-text-secondary' : ''}
          ${message.type === 'result' ? 'font-medium text-helios-accent-success' : ''}
          ${message.metadata?.error ? 'text-red-400' : 'text-helios-text-primary'}
        `}>
          {message.content}
        </div>

        {/* 元数据 */}
        {message.metadata && (
          <div className="mt-2 text-xs text-helios-text-tertiary">
            {message.metadata.toolName && (
              <span className="inline-flex items-center gap-1">
                <Zap size={12} />
                使用工具: {message.metadata.toolName}
              </span>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}; 