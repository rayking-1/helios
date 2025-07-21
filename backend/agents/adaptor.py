from pyautogen.agentchat import ConversableAgent

class AdaptorAgent(ConversableAgent):
    def __init__(self, name: str, llm_config: dict, **kwargs):
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message="""你是一名反馈分析与适应专家。
            你倾听用户关于其计划进展的反馈。
            你的工作是解读反馈的意图（例如，计划太难、太容易、日程冲突）
            然后制定一个精确的请求给策略师代理，以生成新的、适应的计划。
            你的输出应该是一个指令，例如：'策略师，请重新生成未来2周的计划，工作量减少20%。'""",
            **kwargs,
        )

    def process_feedback(self, feedback_text: str) -> str:
        """
        分析用户反馈并制定重新规划请求。
        
        Args:
            feedback_text: 用户的反馈文本
            
        Returns:
            str: 给策略师的指令或无需行动的消息
        """
        # 在实际场景中，这将使用`interpret_feedback`工具（一个LLM调用）
        # 来理解情感和意图。
        feedback_text = feedback_text.lower()
        
        if "太难" in feedback_text or "困难" in feedback_text or "吃力" in feedback_text:
            return "策略师，用户认为当前计划太难。请为下周创建一个强度降低的修订计划。"
        elif "太简单" in feedback_text or "容易" in feedback_text or "不够挑战" in feedback_text:
            return "策略师，用户认为当前计划太简单。请生成一个包含更多挑战性任务的修订计划。"
        elif "时间不够" in feedback_text or "来不及" in feedback_text:
            return "策略师，用户时间不足以完成当前计划。请延长任务时间线或减少工作量。"
        elif "落后" in feedback_text or "没完成" in feedback_text:
            return "策略师，用户已经落后于计划。请重新安排后续任务并考虑调整难度。"
        elif "时间冲突" in feedback_text:     
            return "策略师，用户的时间冲突。请重新安排冲突部分时间以避免冲突。"
        elif "任务冲突" in feedback_text:
            return "策略师，用户的任务冲突。请重新安排冲突部分任务以避免冲突。" 
        else:
            return "根据反馈，无需采取行动。当前计划似乎适合用户的需求和能力。" 
        