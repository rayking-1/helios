"""
适应性规划API路由
提供与智能体规划系统交互的API接口
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
import logging
from pydantic import BaseModel

# 导入智能体团队
from helios_backend.agent_team import AdaptivePlanTeam

# 设置日志记录器
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/plan",
    tags=["plan"],
    responses={404: {"description": "Not found"}},
)

# 创建全局智能体团队实例
# 注意：在生产环境中，应该考虑将其作为依赖注入或使用更合适的状态管理方式
agent_team = AdaptivePlanTeam()

# 定义请求和响应模型
class GoalRequest(BaseModel):
    """目标请求模型"""
    goal: str
    user_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    """反馈请求模型"""
    text: str
    ratings: Optional[Dict[str, int]] = None
    priority_changes: Optional[List[Dict[str, Any]]] = None
    user_id: Optional[str] = None

class PlanResponse(BaseModel):
    """计划响应模型"""
    success: bool
    plan: Optional[str] = None
    error: Optional[str] = None
    conversation_id: Optional[str] = None

# 规划会话存储
# 在生产环境中，应该使用数据库存储
active_sessions: Dict[str, Dict[str, Any]] = {}

@router.post("/generate", response_model=PlanResponse)
async def generate_plan(request: GoalRequest, background_tasks: BackgroundTasks):
    """
    生成新的适应性计划
    
    根据用户目标，使用多智能体系统生成详细计划
    """
    try:
        logger.info(f"收到新的规划请求: {request.goal[:50]}...")
        
        # 启动规划会话（异步处理）
        background_tasks.add_task(
            process_plan_generation,
            request.goal,
            request.user_id
        )
        
        # 立即返回接收确认
        return {
            "success": True,
            "plan": "正在生成计划，请稍候...",
            "conversation_id": request.user_id or "default"
        }
    except Exception as e:
        logger.error(f"生成计划时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"生成计划失败: {str(e)}"
        )

@router.post("/feedback", response_model=PlanResponse)
async def submit_feedback(request: FeedbackRequest, background_tasks: BackgroundTasks):
    """
    提交对计划的反馈
    
    根据用户反馈，调整现有计划
    """
    try:
        logger.info(f"收到反馈: {request.text[:50]}...")
        
        # 提交反馈（异步处理）
        background_tasks.add_task(
            process_feedback_submission,
            request.text,
            request.ratings,
            request.priority_changes,
            request.user_id
        )
        
        # 立即返回接收确认
        return {
            "success": True,
            "plan": "正在处理反馈，请稍候...",
            "conversation_id": request.user_id or "default"
        }
    except Exception as e:
        logger.error(f"处理反馈时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"处理反馈失败: {str(e)}"
        )

@router.get("/status/{conversation_id}", response_model=PlanResponse)
async def get_planning_status(conversation_id: str):
    """
    获取规划会话状态
    
    查询特定会话的当前状态和计划内容
    """
    try:
        if conversation_id not in active_sessions:
            raise HTTPException(
                status_code=404,
                detail=f"找不到会话ID: {conversation_id}"
            )
        
        session = active_sessions[conversation_id]
        
        return {
            "success": True,
            "plan": session.get("plan", "尚未生成计划"),
            "conversation_id": conversation_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取会话状态时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"获取会话状态失败: {str(e)}"
        )

# 后台任务处理函数
def process_plan_generation(goal: str, user_id: Optional[str] = None):
    """异步处理规划生成"""
    try:
        session_id = user_id or "default"
        
        # 启动规划会话
        result = agent_team.start_planning_session(goal)
        
        # 存储结果
        active_sessions[session_id] = {
            "plan": result.get("plan", ""),
            "history": result.get("history", []),
            "status": "completed" if result.get("success", False) else "failed"
        }
        
        logger.info(f"规划会话完成: {session_id}")
    except Exception as e:
        logger.error(f"规划生成过程中发生错误: {str(e)}", exc_info=True)
        active_sessions[user_id or "default"] = {
            "plan": f"生成计划时发生错误: {str(e)}",
            "status": "failed"
        }

def process_feedback_submission(
    feedback_text: str,
    ratings: Optional[Dict[str, int]] = None,
    priority_changes: Optional[List[Dict[str, Any]]] = None,
    user_id: Optional[str] = None
):
    """异步处理反馈提交"""
    try:
        session_id = user_id or "default"
        
        # 构建反馈数据
        feedback_data = {
            "text": feedback_text
        }
        
        if ratings:
            feedback_data["ratings"] = ratings
            
        if priority_changes:
            feedback_data["priority_changes"] = priority_changes
        
        # 提交反馈
        result = agent_team.provide_feedback(feedback_data)
        
        # 更新存储的结果
        if session_id in active_sessions:
            active_sessions[session_id].update({
                "plan": result.get("updated_plan", ""),
                "history": result.get("history", []),
                "status": "updated" if result.get("success", False) else "failed"
            })
        else:
            active_sessions[session_id] = {
                "plan": result.get("updated_plan", ""),
                "history": result.get("history", []),
                "status": "updated" if result.get("success", False) else "failed"
            }
        
        logger.info(f"反馈处理完成: {session_id}")
    except Exception as e:
        logger.error(f"处理反馈过程中发生错误: {str(e)}", exc_info=True)
        if user_id or "default" in active_sessions:
            active_sessions[user_id or "default"].update({
                "status": "failed",
                "error": f"处理反馈时发生错误: {str(e)}"
            })
        else:
            active_sessions[user_id or "default"] = {
                "plan": "处理反馈时发生错误",
                "status": "failed",
                "error": str(e)
            } 