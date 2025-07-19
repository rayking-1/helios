# main.py
import os
from dotenv import load_dotenv

# ========================[ 关键指令 ]========================
# 在导入任何其他自定义模块（尤其是配置模块）之前，
# 必须立即调用 load_dotenv()。
# 这将确保 .env 文件中的所有变量都已加载到系统环境中，
# 供后续所有模块安全使用。
load_dotenv()
# ==========================================================

from autogen import GroupChat, GroupChatManager
from helios_backend.config import logger, llm_config
from helios_backend.agent_core import PlannerAgent, ResearcherAgent, CriticAgent, IntegratorAgent, user_proxy
from helios_backend.tools import web_search  # 导入web_search工具函数

def main():
    """
    主函数，负责初始化并运行整个智能体工作流。
    """
    logger.info("================== New Task Start ==================")
    
    try:
        # 步骤 1: 实例化并解包所有智能体
        logger.info("Initializing agents...")
        planner = PlannerAgent()
        researcher = ResearcherAgent()
        critic = CriticAgent()
        integrator = IntegratorAgent()
        
        # 注册工具函数到UserProxyAgent
        user_proxy.function_map = {
            "web_search": web_search  # 将web_search函数注册到function_map
        }
        logger.info("Registered web_search tool to UserProxyAgent")
        
        logger.info("All agents initialized successfully")
    
    # 步骤 2: 定义有限状态机（FSM）驱动的群聊
    # allowed_transitions 定义了智能体之间严格的对话顺序，构成了确定性的工作流。
        logger.info("Setting up FSM-driven group chat...")
    groupchat = GroupChat(
        agents=[user_proxy, planner, researcher, critic, integrator],
        messages=[],
        max_round=20,
        allowed_transitions={
            user_proxy: [planner],
            planner: [researcher],
            researcher: [critic],
            critic: [planner, researcher, integrator], # Critic可以决定返回修改或继续
            integrator: [user_proxy] # 整合者最终将答案返回给用户代理
        }
    )

    # 步骤 3: 创建群聊管理器
    manager = GroupChatManager(
        groupchat=groupchat, 
        llm_config=llm_config
    )
        logger.info("Group chat manager initialized")

    # 步骤 4: 定义并启动初始任务
        # 使用一个需要实时信息的请求来测试web_search工具
        initial_task = "请研究一下什么是'AutoGen'框架，并总结它的主要特点和优势。"
    
        logger.info("🚀 Helios系统启动，开始执行任务...")
        logger.info(f"📝 初始任务: {initial_task}")
    
    user_proxy.initiate_chat(
        manager,
        message=initial_task,
    )
    
        logger.info("✅ 任务执行完毕，Helios系统关闭。")
        
        final_response = user_proxy.last_message().get("content", "No final response found.")
        logger.info(f"Final integrated response:\n---\n{final_response}\n---")
        
    except Exception as e:
        # 捕获所有未预料到的异常作为最后防线
        logger.error(f"An unexpected error occurred during the Helios workflow.", exc_info=True)
        # exc_info=True 会自动将异常堆栈信息附加到日志中，非常便于调试
        logger.error("The task has failed and will be terminated.")
        
    finally:
        logger.info("================== Task End ==================\n")

# FSM工作流可视化
# 使用 Mermaid 语法清晰展示智能体协作流程
# graph TD
#     A[Start: UserProxy] --> B(Planner);
#     B --> C(Researcher);
#     C --> D{Critic};
#     D -- Revise Plan --> B;
#     D -- Redo Research --> C;
#     D -- Approve --> E(Integrator);
#     E --> F[End: UserProxy];

if __name__ == "__main__":
    main() 