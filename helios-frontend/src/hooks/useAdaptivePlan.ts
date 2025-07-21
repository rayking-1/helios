import { useMutation } from '@apollo/client';
import { useState } from 'react';
import { GENERATE_PLAN, SUBMIT_FEEDBACK } from '../api/graphql/schema';
import { useAppStore } from '../store/useAppStore';

interface UseAdaptivePlanProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

/**
 * 用于生成和更新自适应计划的Hook
 * 集成了GraphQL mutations和Zustand状态管理
 */
export const useAdaptivePlan = ({ onSuccess, onError }: UseAdaptivePlanProps = {}) => {
  const { updatePlan } = useAppStore();
  const [currentPlanId, setCurrentPlanId] = useState<string | null>(null);

  // 生成新计划的mutation
  const [generatePlan, { loading: generating, error: generateError }] = useMutation(GENERATE_PLAN, {
    onCompleted: (data) => {
      const { planId, initialPlan } = data.startNewGoal;
      
      // 更新Zustand store中的计划状态
      updatePlan(initialPlan);
      
      // 保存计划ID以便后续使用
      setCurrentPlanId(planId);
      
      // 调用成功回调
      onSuccess?.();
    },
    onError: (error) => {
      console.error('生成计划失败:', error);
      onError?.(error);
    }
  });

  // 提交反馈的mutation
  const [submitFeedback, { loading: submitting, error: submitError }] = useMutation(SUBMIT_FEEDBACK, {
    onCompleted: (data) => {
      const { updatedPlan } = data.submitFeedback;
      
      // 更新Zustand store中的计划状态
      updatePlan(updatedPlan);
      
      // 调用成功回调
      onSuccess?.();
    },
    onError: (error) => {
      console.error('提交反馈失败:', error);
      onError?.(error);
    }
  });

  // 生成新计划的函数
  const generateNewPlan = (prompt: string) => {
    generatePlan({
      variables: { prompt }
    });
  };

  // 提交任务反馈的函数
  const provideFeedback = (taskId: string, feedbackType: 'TOO_EASY' | 'TOO_HARD', feedbackText?: string) => {
    if (!currentPlanId) {
      console.error('没有活动的计划ID，无法提交反馈');
      return;
    }

    submitFeedback({
      variables: {
        planId: currentPlanId,
        taskId,
        feedbackType,
        feedbackText
      }
    });
  };

  return {
    generateNewPlan,
    provideFeedback,
    currentPlanId,
    loading: generating || submitting,
    error: generateError || submitError
  };
}; 