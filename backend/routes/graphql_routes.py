from typing import Dict, List, Optional, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
import strawberry
from strawberry.fastapi import GraphQLRouter
from backend.agent_team import AdaptivePlanTeam

router = APIRouter(tags=["graphql"])

# 定义GraphQL类型
@strawberry.type
class Task:
    task_id: str
    title: str
    description: str
    difficulty: int
    importance: int
    completed: bool
    tags: List[str]

@strawberry.type
class Day:
    day_number: int
    date: str
    tasks: List[Task]

@strawberry.type
class Week:
    week_number: int
    theme: str
    days: List[Day]

@strawberry.type
class Plan:
    plan_id: str
    version: int
    weeks: List[Week]

@strawberry.type
class GoalResult:
    plan_id: str
    initial_plan: Plan

@strawberry.type
class FeedbackResult:
    success: bool
    updated_plan: Optional[Plan]

# 定义Resolver
class Query:
    @strawberry.field
    def current_plan(self, plan_id: str) -> Optional[Plan]:
        # 这里应该从数据库或缓存中获取计划
        # 示例实现，实际使用时需要替换
        try:
            # 模拟获取计划
            # 在实际代码中，应该查询数据库或缓存
            return Plan(
                plan_id=plan_id,
                version=1,
                weeks=[]  # 实际会返回完整计划
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Plan not found: {str(e)}")

class Mutation:
    @strawberry.mutation
    def start_new_goal(self, prompt: str) -> GoalResult:
        try:
            # 创建AG2团队实例
            # 注意：这里假设AdaptivePlanTeam是正确实现的
            team = AdaptivePlanTeam()
            
            # 生成计划
            result = team.run(prompt)
            
            # 将结果转换为GraphQL类型
            # 注意：这需要根据实际AG2返回的数据结构进行适配
            plan_id = str(uuid.uuid4())
            
            # 假设result['plan']已经是正确的计划结构
            # 实际实现需要转换AG2返回的数据到GraphQL类型
            return GoalResult(
                plan_id=plan_id,
                initial_plan=Plan(
                    plan_id=plan_id,
                    version=1,
                    weeks=[]  # 实际会填充生成的计划数据
                )
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")

    @strawberry.mutation
    def submit_feedback(
        self, 
        plan_id: str, 
        task_id: str, 
        feedback_type: str,
        feedback_text: Optional[str] = None
    ) -> FeedbackResult:
        try:
            # 创建AG2团队实例
            team = AdaptivePlanTeam()
            
            # 构建反馈
            feedback = f"Task {task_id} feedback: {feedback_type}"
            if feedback_text:
                feedback += f" - {feedback_text}"
                
            # 处理反馈并更新计划
            result = team.process_feedback(feedback)
            
            # 将结果转换为GraphQL类型
            return FeedbackResult(
                success=True,
                updated_plan=Plan(
                    plan_id=plan_id,
                    version=2,  # 版本递增
                    weeks=[]  # 实际会填充更新的计划数据
                )
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process feedback: {str(e)}")

# 创建Strawberry Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# 创建GraphQL路由
graphql_router = GraphQLRouter(schema)

# 将GraphQL路由挂载到API路由下
router.include_router(graphql_router, prefix="/graphql") 