from pyautogen.agentchat import ConversableAgent
import json

class AnalystAgent(ConversableAgent):
    def __init__(self, name: str, llm_config: dict, **kwargs):
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message="""你是一名目标解构专家。你的任务是帮助用户将模糊的目标转化为具体、可衡量、可实现、相关且有时间限制（SMART）的目标。

            如果用户的目标不明确或缺乏细节，你必须提出澄清问题以收集必要的信息。不要做假设。你的最终输出必须是一个表示SMART目标的结构化JSON对象。""",
            **kwargs,
        )

    def process_message(self, message: str) -> str:
        """
        分析用户的消息，判断它是明确的目标还是需要澄清。
        
        Args:
            message: 用户输入的消息
            
        Returns:
            str: 如果目标明确，返回JSON格式的结构化目标；
                 如果目标模糊，返回调用ask_user_clarification工具的指令
        """
        # 这是一个简化的逻辑占位符。实际实现可能涉及调用LLM来评估模糊性。
        is_ambiguous = not all(kw in message.lower() for kw in ["what", "by when"])

        if is_ambiguous:
            # 在实际场景中，这将是一个更智能的问题。
            question = "这个目标似乎有点模糊。你能具体说明你想实现*什么*以及*何时*实现吗？"
            # 代理将在这里配置调用工具。
            # 目前，我们返回问题以模拟流程。
            return f"ACTION: ask_user_clarification(question='{question}')"
        else:
            # 提取实体和构建目标的占位符。
            structured_goal = {"goal": message, "status": "clarified"}
            return json.dumps(structured_goal, indent=2) 