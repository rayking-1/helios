# agent_core.py
from autogen import AssistantAgent, UserProxyAgent
from config import llm_config, config_list_instance
import logging

# 设置日志记录器
logger = logging.getLogger(__name__)

# 定义web_search工具的JSON Schema描述
web_search_tool_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "通过DuckDuckGo搜索引擎查询最新信息，获取实时的网络数据。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要在互联网上搜索的查询词或问题。"
                }
            },
            "required": ["query"]
        }
    }
}

# 1. 规划师 (Planner)
class PlannerAgent(AssistantAgent):
    """将用户请求分解为清晰、分步计划的专家。"""
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Planner",
            system_message="""你是一位顶级的规划专家。
你的唯一任务是深入理解用户请求，并将其拆解成一个清晰、详细、可执行、分步的计划。
计划的每一步都必须是具体的、可操作的，并且逻辑上前后关联。
在计划的末尾，你必须明确指示研究员（Researcher）开始执行计划的第一步。
不要执行计划，你的职责仅限于规划。""",
            llm_config=llm_config,
            *args, **kwargs
        )
        logger.info(f"Agent '{self.name}' initialized with LLM config")

# 2. 研究员 (Researcher)
class ResearcherAgent(AssistantAgent):
    """严格按照计划执行信息搜集的研究员。"""
    def __init__(self, *args, **kwargs):
        # 为研究员添加工具配置
        researcher_llm_config = llm_config.copy()
        researcher_llm_config["tools"] = [web_search_tool_schema]
        
        super().__init__(
            name="Researcher",
            system_message="""你是一名高效的信息研究员。
你的职责是严格按照规划师（Planner）提供的计划，系统地搜集和整理信息。
你必须一次只执行计划中的一个步骤。

你有一个强大的'web_search'工具可以使用：
- 对于任何需要最新事实、数据或外部信息的请求，你必须使用'web_search'工具。
- 首先，制定一个清晰的搜索查询。
- 然后，使用该查询调用工具。
- 最后，综合搜索结果来回答用户的请求。
- 不要编造信息，尽可能引用来源URL。

在完成当前步骤的信息搜集后，清晰地总结你的发现，并将其呈现给评论家（Critic）进行评估。
不要自己进行规划或整合，只专注于执行研究任务。""",
            llm_config=researcher_llm_config,
            *args, **kwargs
        )
        logger.info(f"Agent '{self.name}' initialized with LLM config and web_search tool")

# 3. 评论家 (Critic)
class CriticAgent(AssistantAgent):
    """负责质量控制，对计划和结果进行批判性评估。"""
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Critic",
            system_message="""你是一位思维严谨、注重细节的评论家。
你的任务是严格评估规划师的计划和研究员的发现。
1. 检查计划是否存在逻辑漏洞、不一致或可以优化的地方。
2. 评估研究员的发现是否全面、准确，并与计划目标完全一致。
提出具体的、建设性的反馈和改进建议，并将你的评估结果同时反馈给规划师和研究员。
你的目标是提升最终成果的质量，而不是简单地批评。""",
            llm_config=llm_config,
            *args, **kwargs
        )
        logger.info(f"Agent '{self.name}' initialized with LLM config")

# 4. 整合者 (Integrator)
class IntegratorAgent(AssistantAgent):
    """综合所有信息，生成最终高质量报告的专家。"""
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Integrator",
            system_message="""你是一位资深的整合专家。
你的任务是综合规划师的最终计划、研究员的所有发现以及评论家的所有反馈。
基于所有这些信息，撰写一份全面、流畅、高质量的最终报告或答案。
确保最终产出内容结构清晰、逻辑严密，并完全满足用户的原始请求。
在输出最终答案前，必须以 'TERMINATE' 结束你的发言。""",
            llm_config=llm_config,
            *args, **kwargs
        )
        logger.info(f"Agent '{self.name}' initialized with LLM config")

# 5. 用户代理 (UserProxy)
try:
    logger.info("Initializing UserProxy agent...")
    user_proxy = UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",  # 在全自动模式下运行
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False, # 出于安全考虑，默认禁用代码执行
        default_auto_reply="请继续下一步，或在完成后输出 'TERMINATE'。",
    )
    logger.info(f"Agent '{user_proxy.name}' initialized successfully")
except Exception as e:
    logger.error("Failed to initialize UserProxy agent", exc_info=True)
    raise

# 工厂函数：用于在主程序中统一获取所有智能体实例
def get_agents():
    """
    实例化并返回项目中所有定义的智能体。
    
    Returns:
        tuple: 包含所有实例化智能体的元组
    """
    logger.info("Creating all agent instances...")
    try:
        planner = PlannerAgent()
        researcher = ResearcherAgent()
        critic = CriticAgent()
        integrator = IntegratorAgent()
        
        logger.info("All agent instances created successfully")
        return planner, researcher, critic, integrator, user_proxy
    except Exception as e:
        logger.error("Failed to create agent instances", exc_info=True)
        raise 