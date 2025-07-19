# main.py

# 1. 首先导入无依赖的配置和日志记录器
from helios_backend import settings, logger

# 2. 导入需要被实例化的类
from helios_backend.models.clients import MultiModelClient
from helios_backend.agent_core import PlannerAgent, ResearcherAgent, CriticAgent, IntegratorAgent, user_proxy
import autogen

def main():
    """
    应用主入口点 (Composition Root)。
    负责实例化和"注入"所有依赖。
    """
    logger.info("================== Helios System Startup ==================")

    # 3. 实例化核心服务
    # 将settings对象注入到MultiModelClient的构造函数中
    model_client = MultiModelClient(settings=settings)
    
    # 4. 准备Agent的llm_config
    # 这是autogen需要的格式
    llm_config = {
        "config_list": model_client.get_config_list(),
        "cache_seed": 42,
    }
    
    # 5. 实例化所有Agent
    planner = PlannerAgent(llm_config=llm_config)
    researcher = ResearcherAgent(llm_config=llm_config)
    critic = CriticAgent(llm_config=llm_config)
    integrator = IntegratorAgent(llm_config=llm_config)

    logger.info("All agents initialized successfully.")

    # 6. 定义并启动GroupChat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, planner, researcher, critic, integrator],
        messages=[],
        max_round=15
    )

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    task = "分析当前AI Agent框架（如AutoGen, CrewAI, LangGraph）的优缺点，并为企业技术选型提供建议。"
    logger.info(f"Initiating task: {task}")

    user_proxy.initiate_chat(manager, message=task)
    
    logger.info("================== Helios System Shutdown ==================")

if __name__ == "__main__":
    main() 