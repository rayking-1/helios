from pyautogen.agentchat import ConversableAgent
import json

class StrategistAgent(ConversableAgent):
    def __init__(self, name: str, llm_config: dict, **kwargs):
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message="""你是一名总体规划师。你是将策略转化为行动的专家。
            
            你将收到一个结构化的目标和一份关于方法的研究报告。
            你的工作是将这些输入综合成详细的、可执行的计划。
            最终输出必须是一个表示任务列表的有效JSON对象。
            每个任务必须有一个id、描述、截止日期和依赖项列表。
            使用`create_task_graph`工具验证计划的逻辑。""",
            **kwargs,
        )

    def generate_plan(self, goal: dict, research: str) -> str:
        """
        生成最终的JSON计划。
        
        Args:
            goal: 结构化目标字典
            research: 研究报告文本
            
        Returns:
            str: JSON格式的计划
        """
        # 在实际场景中，这将是一个复杂的LLM调用，将目标和研究作为上下文
        # 并要求LLM根据系统提示的规则生成计划。
        # 为了模拟，我们返回一个硬编码的计划。
        plan_json = [
            {"id": "task_1", "description": "研究Python基础知识", "due_date": "2025-08-01", "depends_on": []},
            {"id": "task_2", "description": "完成第一章项目", "due_date": "2025-08-05", "depends_on": ["task_1"]},
            {"id": "task_3", "description": "学习数据分析库", "due_date": "2025-08-10", "depends_on": ["task_2"]},
            {"id": "task_4", "description": "完成实际数据集分析", "due_date": "2025-08-20", "depends_on": ["task_3"]}
        ]
        return json.dumps(plan_json, indent=2) 