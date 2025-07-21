import { useState, useEffect } from 'react';
import { useQuery, useMutation } from 'react-query';
import { planApi } from '../../api/planApi';
import { useAppStore, useCurrentPlan, useSystemStatus, useAgentMessages } from '../../store/useAppStore';
import useWebSocketUpdates from '../../hooks/useWebSocketUpdates';
import { format } from 'date-fns';

// 导入组件（根据实际项目引入或创建）
import TaskList from '../tasks/TaskList';
import TaskCreationModal from '../tasks/TaskCreationModal';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';

const PlannerPage = () => {
  // 获取当前用户信息
  const user = useAppStore(state => state.user);
  
  // 从Zustand获取状态和方法
  const currentPlan = useCurrentPlan();
  const systemStatus = useSystemStatus();
  const agentMessages = useAgentMessages();
  const { updatePlan, updateSystemStatus, addAgentMessage, clearAgentMessages } = useAppStore();
  
  // 本地状态
  const [isCreatingGoal, setIsCreatingGoal] = useState(false);
  const [goalInput, setGoalInput] = useState('');
  const [timeframeInput, setTimeframeInput] = useState('');
  
  // 连接WebSocket
  const { isConnected: wsConnected } = useWebSocketUpdates(user.id);
  
  // 使用React Query获取当前计划
  const { 
    isLoading: planLoading, 
    error: planError,
    refetch: refetchPlan
  } = useQuery('currentPlan', planApi.getCurrentPlan, {
    enabled: !!user.isAuthenticated, // 只有用户登录后才加载
    onSuccess: (data) => {
      // 将数据存储到Zustand
      updatePlan(data);
    },
    onError: () => {
      // 清除当前存储的计划数据
      updatePlan(null);
    }
  });
  
  // 使用React Query获取系统状态
  const { 
    data: systemStatusData,
    refetch: refetchStatus
  } = useQuery('systemStatus', planApi.getSystemStatus, {
    enabled: !!user.isAuthenticated,
    refetchInterval: 10000, // 每10秒自动刷新一次
    onSuccess: (data) => {
      updateSystemStatus(data.status, null);
    }
  });
  
  // 创建计划的mutation
  const createPlanMutation = useMutation(planApi.createPlan, {
    onSuccess: () => {
      // 清除旧的消息
      clearAgentMessages();
      
      // 更新状态为规划中
      updateSystemStatus('PLANNING', '正在生成您的计划...');
      
      // 关闭输入界面
      setIsCreatingGoal(false);
      
      // 模拟智能体消息
      setTimeout(() => {
        addAgentMessage({
          agentName: 'AnalystAgent',
          message: '我正在分析您的目标...',
          timestamp: new Date().toISOString()
        });
      }, 1000);
      
      setTimeout(() => {
        addAgentMessage({
          agentName: 'ResearcherAgent',
          message: '正在研究实现这个目标的最佳方法...',
          timestamp: new Date().toISOString()
        });
      }, 3000);
      
      // 3秒后重新获取计划
      setTimeout(() => {
        refetchPlan();
        refetchStatus();
      }, 5000);
    },
    onError: (error) => {
      console.error('创建计划失败:', error);
      updateSystemStatus('ERROR', '无法创建计划，请稍后再试');
    }
  });
  
  // 处理目标提交
  const handleGoalSubmit = () => {
    if (!goalInput.trim()) return;
    
    createPlanMutation.mutate({
      goal: goalInput,
      timeframe: timeframeInput || undefined
    });
  };
  
  // 计算连接状态显示
  const connectionStatus = () => {
    if (wsConnected) {
      return <span className="text-green-500">已连接</span>;
    }
    return <span className="text-red-500">未连接</span>;
  };
  
  return (
    <div className="container mx-auto p-4">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold">自适应计划系统</h1>
        <div className="text-sm">
          WebSocket状态: {connectionStatus()}
        </div>
      </div>
      
      {/* 系统状态指示器 */}
      <div className="bg-gray-100 p-4 rounded-lg mb-6">
        <div className="flex justify-between items-center">
          <div>
            <span className="font-semibold">系统状态:</span>{' '}
            <span className={systemStatus.status === 'PLANNING' ? 'text-blue-500' : 'text-green-500'}>
              {systemStatus.status}
            </span>
            {systemStatus.details && <p className="text-sm text-gray-600">{systemStatus.details}</p>}
          </div>
          {systemStatus.status === 'PLANNING' && <LoadingSpinner />}
        </div>
      </div>
      
      {/* 目标创建区 */}
      {!currentPlan && !isCreatingGoal && (
        <div className="text-center py-12">
          <h2 className="text-xl mb-4">您还没有活跃的计划</h2>
          <Button onClick={() => setIsCreatingGoal(true)}>创建新计划</Button>
        </div>
      )}
      
      {isCreatingGoal && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl mb-4">创建新计划</h2>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              您的目标是什么?
            </label>
            <input
              type="text"
              value={goalInput}
              onChange={(e) => setGoalInput(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="例如: 我想在3个月内学习Python"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              时间范围 (可选)
            </label>
            <input
              type="text"
              value={timeframeInput}
              onChange={(e) => setTimeframeInput(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="例如: 3个月, 或 2023年底前"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button 
              variant="secondary" 
              onClick={() => setIsCreatingGoal(false)}
            >
              取消
            </Button>
            <Button 
              onClick={handleGoalSubmit}
              disabled={!goalInput.trim() || createPlanMutation.isLoading}
            >
              {createPlanMutation.isLoading ? '正在提交...' : '创建计划'}
            </Button>
          </div>
        </div>
      )}
      
      {/* 当前计划展示区 */}
      {currentPlan && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-semibold">{currentPlan.goal}</h2>
              <p className="text-gray-600 text-sm">
                版本: {currentPlan.version} | 
                计划ID: {currentPlan.planId}
              </p>
              {currentPlan.changelog && (
                <p className="text-sm bg-yellow-50 p-2 mt-2 rounded border border-yellow-200">
                  最近更新: {currentPlan.changelog}
                </p>
              )}
            </div>
            <Button onClick={() => refetchPlan()}>
              刷新计划
            </Button>
          </div>
          
          {/* 任务列表 */}
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-2">任务清单</h3>
            {planLoading ? (
              <p>加载中...</p>
            ) : (
              <TaskList tasks={currentPlan.tasks} />
            )}
          </div>
        </div>
      )}
      
      {/* 智能体消息流 */}
      {agentMessages.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium mb-2">智能体工作流</h3>
          <div className="bg-gray-50 p-4 rounded-lg max-h-64 overflow-y-auto">
            {agentMessages.map((msg, idx) => (
              <div key={idx} className="mb-2 pb-2 border-b">
                <div className="flex justify-between">
                  <span className="font-medium">{msg.agentName}</span>
                  <span className="text-xs text-gray-500">
                    {format(new Date(msg.timestamp), 'HH:mm:ss')}
                  </span>
                </div>
                <p className="text-sm">{msg.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* 错误展示 */}
      {planError && (
        <div className="bg-red-50 text-red-700 p-4 rounded-lg mt-4">
          无法加载计划数据。请确保您已登录并且有活跃的计划。
        </div>
      )}
    </div>
  );
};

export default PlannerPage; 
 
import { useQuery, useMutation } from 'react-query';
import { planApi } from '../../api/planApi';
import { useAppStore, useCurrentPlan, useSystemStatus, useAgentMessages } from '../../store/useAppStore';
import useWebSocketUpdates from '../../hooks/useWebSocketUpdates';
import { format } from 'date-fns';

// 导入组件（根据实际项目引入或创建）
import TaskList from '../tasks/TaskList';
import TaskCreationModal from '../tasks/TaskCreationModal';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';

const PlannerPage = () => {
  // 获取当前用户信息
  const user = useAppStore(state => state.user);
  
  // 从Zustand获取状态和方法
  const currentPlan = useCurrentPlan();
  const systemStatus = useSystemStatus();
  const agentMessages = useAgentMessages();
  const { updatePlan, updateSystemStatus, addAgentMessage, clearAgentMessages } = useAppStore();
  
  // 本地状态
  const [isCreatingGoal, setIsCreatingGoal] = useState(false);
  const [goalInput, setGoalInput] = useState('');
  const [timeframeInput, setTimeframeInput] = useState('');
  
  // 连接WebSocket
  const { isConnected: wsConnected } = useWebSocketUpdates(user.id);
  
  // 使用React Query获取当前计划
  const { 
    isLoading: planLoading, 
    error: planError,
    refetch: refetchPlan
  } = useQuery('currentPlan', planApi.getCurrentPlan, {
    enabled: !!user.isAuthenticated, // 只有用户登录后才加载
    onSuccess: (data) => {
      // 将数据存储到Zustand
      updatePlan(data);
    },
    onError: () => {
      // 清除当前存储的计划数据
      updatePlan(null);
    }
  });
  
  // 使用React Query获取系统状态
  const { 
    data: systemStatusData,
    refetch: refetchStatus
  } = useQuery('systemStatus', planApi.getSystemStatus, {
    enabled: !!user.isAuthenticated,
    refetchInterval: 10000, // 每10秒自动刷新一次
    onSuccess: (data) => {
      updateSystemStatus(data.status, null);
    }
  });
  
  // 创建计划的mutation
  const createPlanMutation = useMutation(planApi.createPlan, {
    onSuccess: () => {
      // 清除旧的消息
      clearAgentMessages();
      
      // 更新状态为规划中
      updateSystemStatus('PLANNING', '正在生成您的计划...');
      
      // 关闭输入界面
      setIsCreatingGoal(false);
      
      // 模拟智能体消息
      setTimeout(() => {
        addAgentMessage({
          agentName: 'AnalystAgent',
          message: '我正在分析您的目标...',
          timestamp: new Date().toISOString()
        });
      }, 1000);
      
      setTimeout(() => {
        addAgentMessage({
          agentName: 'ResearcherAgent',
          message: '正在研究实现这个目标的最佳方法...',
          timestamp: new Date().toISOString()
        });
      }, 3000);
      
      // 3秒后重新获取计划
      setTimeout(() => {
        refetchPlan();
        refetchStatus();
      }, 5000);
    },
    onError: (error) => {
      console.error('创建计划失败:', error);
      updateSystemStatus('ERROR', '无法创建计划，请稍后再试');
    }
  });
  
  // 处理目标提交
  const handleGoalSubmit = () => {
    if (!goalInput.trim()) return;
    
    createPlanMutation.mutate({
      goal: goalInput,
      timeframe: timeframeInput || undefined
    });
  };
  
  // 计算连接状态显示
  const connectionStatus = () => {
    if (wsConnected) {
      return <span className="text-green-500">已连接</span>;
    }
    return <span className="text-red-500">未连接</span>;
  };
  
  return (
    <div className="container mx-auto p-4">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold">自适应计划系统</h1>
        <div className="text-sm">
          WebSocket状态: {connectionStatus()}
        </div>
      </div>
      
      {/* 系统状态指示器 */}
      <div className="bg-gray-100 p-4 rounded-lg mb-6">
        <div className="flex justify-between items-center">
          <div>
            <span className="font-semibold">系统状态:</span>{' '}
            <span className={systemStatus.status === 'PLANNING' ? 'text-blue-500' : 'text-green-500'}>
              {systemStatus.status}
            </span>
            {systemStatus.details && <p className="text-sm text-gray-600">{systemStatus.details}</p>}
          </div>
          {systemStatus.status === 'PLANNING' && <LoadingSpinner />}
        </div>
      </div>
      
      {/* 目标创建区 */}
      {!currentPlan && !isCreatingGoal && (
        <div className="text-center py-12">
          <h2 className="text-xl mb-4">您还没有活跃的计划</h2>
          <Button onClick={() => setIsCreatingGoal(true)}>创建新计划</Button>
        </div>
      )}
      
      {isCreatingGoal && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl mb-4">创建新计划</h2>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              您的目标是什么?
            </label>
            <input
              type="text"
              value={goalInput}
              onChange={(e) => setGoalInput(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="例如: 我想在3个月内学习Python"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              时间范围 (可选)
            </label>
            <input
              type="text"
              value={timeframeInput}
              onChange={(e) => setTimeframeInput(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="例如: 3个月, 或 2023年底前"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button 
              variant="secondary" 
              onClick={() => setIsCreatingGoal(false)}
            >
              取消
            </Button>
            <Button 
              onClick={handleGoalSubmit}
              disabled={!goalInput.trim() || createPlanMutation.isLoading}
            >
              {createPlanMutation.isLoading ? '正在提交...' : '创建计划'}
            </Button>
          </div>
        </div>
      )}
      
      {/* 当前计划展示区 */}
      {currentPlan && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-semibold">{currentPlan.goal}</h2>
              <p className="text-gray-600 text-sm">
                版本: {currentPlan.version} | 
                计划ID: {currentPlan.planId}
              </p>
              {currentPlan.changelog && (
                <p className="text-sm bg-yellow-50 p-2 mt-2 rounded border border-yellow-200">
                  最近更新: {currentPlan.changelog}
                </p>
              )}
            </div>
            <Button onClick={() => refetchPlan()}>
              刷新计划
            </Button>
          </div>
          
          {/* 任务列表 */}
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-2">任务清单</h3>
            {planLoading ? (
              <p>加载中...</p>
            ) : (
              <TaskList tasks={currentPlan.tasks} />
            )}
          </div>
        </div>
      )}
      
      {/* 智能体消息流 */}
      {agentMessages.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium mb-2">智能体工作流</h3>
          <div className="bg-gray-50 p-4 rounded-lg max-h-64 overflow-y-auto">
            {agentMessages.map((msg, idx) => (
              <div key={idx} className="mb-2 pb-2 border-b">
                <div className="flex justify-between">
                  <span className="font-medium">{msg.agentName}</span>
                  <span className="text-xs text-gray-500">
                    {format(new Date(msg.timestamp), 'HH:mm:ss')}
                  </span>
                </div>
                <p className="text-sm">{msg.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* 错误展示 */}
      {planError && (
        <div className="bg-red-50 text-red-700 p-4 rounded-lg mt-4">
          无法加载计划数据。请确保您已登录并且有活跃的计划。
        </div>
      )}
    </div>
  );
};

export default PlannerPage; 
 
 