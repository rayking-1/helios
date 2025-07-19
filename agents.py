import autogen
from config import config_list, logger

# 为所有智能体定义一个统一的、理想的LLM配置
llm_config = {"config_list": config_list, "timeout": 600}

logger.info("Initializing agents with configuration...")

# 定义 UserProxyAgent (用户代理)
user_proxy = autogen.UserProxyAgent(
   name="User_Proxy",
   human_input_mode="NEVER",
   max_consecutive_auto_reply=10,
   code_execution_config={"work_dir": "groupchat", "use_docker": False},  # 禁用Docker要求
   system_message="A human admin. You will provide the initial problem and approve the final plan. Your approval is required to proceed with execution."
)
logger.info(f"Agent '{user_proxy.name}' initialized")

# 定义 Critic 智能体 (批判家/审核员)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="As a Critic, your role is to meticulously review plans and completed work. Double-check for alignment with the initial request. Identify potential issues, logical flaws, or overlooked details. Provide constructive, actionable feedback. If the work is satisfactory and complete, state 'Everything looks good and the plan is approved.' and await final integration.",
    llm_config=llm_config
)
logger.info(f"Agent '{critic.name}' initialized with LLM config")

# 定义 Integrator 智能体 (整合者)
integrator = autogen.AssistantAgent(
    name="Integrator",
    llm_config=llm_config,
    system_message="As the Integrator, your responsibilities are precise and sequential: 1. Analyze Dialogue: Carefully review the entire conversation history. Identify the initial user request and all subsequent contributions from other agents, especially the final approval from the Critic. 2. Incremental Synthesis: Your primary goal is to synthesize new information. Do not repeat summaries or code that has already been presented. Your output must build upon the previous messages. 3. Final Output Generation: Once the Critic has approved the work, consolidate all approved components, code, and text into a single, coherent, and complete final response. 4. Task Completion Check: After generating the final output, verify that the initial request has been fully and satisfactorily resolved. 5. Termination Protocol: If the task is complete and no further actions are needed, you MUST end your final message with the single word TERMINATE on a new line. This is a strict, non-negotiable requirement. If the task is not yet complete, do not use this keyword."
)
logger.info(f"Agent '{integrator.name}' initialized with LLM config")

# Log that all agents have been initialized
logger.info("All agents have been successfully initialized") 