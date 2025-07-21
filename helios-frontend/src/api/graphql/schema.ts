import { gql } from '@apollo/client';

// Plan类型的片段，可在多个查询/变更中复用
export const PLAN_FRAGMENT = gql`
  fragment PlanFields on Plan {
    planId
    version
    weeks {
      weekNumber
      theme
      days {
        dayNumber
        date
        tasks {
          taskId
          title
          description
          difficulty
          importance
          completed
          tags
        }
      }
    }
  }
`;

// 生成计划的Mutation
export const GENERATE_PLAN = gql`
  mutation GeneratePlan($prompt: String!) {
    startNewGoal(prompt: $prompt) {
      planId
      initialPlan {
        ...PlanFields
      }
    }
  }
  ${PLAN_FRAGMENT}
`;

// 提交反馈的Mutation
export const SUBMIT_FEEDBACK = gql`
  mutation SubmitFeedback($planId: ID!, $taskId: ID!, $feedbackType: String!, $feedbackText: String) {
    submitFeedback(
      planId: $planId,
      taskId: $taskId,
      feedbackType: $feedbackType,
      feedbackText: $feedbackText
    ) {
      success
      updatedPlan {
        ...PlanFields
      }
    }
  }
  ${PLAN_FRAGMENT}
`;

// 获取当前计划的Query
export const GET_CURRENT_PLAN = gql`
  query GetCurrentPlan($planId: ID!) {
    currentPlan(planId: $planId) {
      ...PlanFields
    }
  }
  ${PLAN_FRAGMENT}
`; 