"""
Agent Team Module

该模块提供了一个智能体团队类，用于编排四个核心智能体的协作。
"""

# 尝试使用不同的pyautogen导入方式
try:
    import pyautogen
    # 尝试导入必要的类
    try:
        from pyautogen.agentchat import GroupChat, GroupChatManager, UserProxyAgent
    except ImportError:
        # 如果没有agentchat子模块，尝试直接导入
        from pyautogen import GroupChat, GroupChatManager, UserProxyAgent
except ImportError:
    # 如果导入pyautogen失败，则尝试传统的autogen导入
    try:
        import autogen
        from autogen import GroupChat, GroupChatManager, UserProxyAgent
    except ImportError:
        raise ImportError("无法导入pyautogen或autogen库。请确保已安装必要的依赖。")

from typing import Dict, Any, List, Optional
import logging

from agents.analyst import AnalystAgent
from agents.researcher import ResearcherAgent
from agents.strategist import StrategistAgent
from agents.adaptor import AdaptorAgent
from tools.user_interaction_tools import ask_user_clarification

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdaptivePlanTeam:
    """
    自适应规划团队
    
    该类编排四个核心智能体的协作，实现从目标分析到计划生成的完整流程。
    使用有限状态机管理智能体之间的交互。
    """
    
    # 定义状态机状态
    STATES = {
        "INIT": "初始化状态",
        "ANALYZING": "目标分析中",
        "RESEARCHING": "方法研究中", 
        "PLANNING": "计划制定中",
        "FEEDBACK": "反馈处理中",
        "COMPLETE": "完成状态",
        "ERROR": "错误状态"
    }
    
    def __init__(self, 
                 config_list: List[Dict[str, Any]],
                 user_proxy=None):
        """
        初始化自适应规划团队
        
        Args:
            config_list: LLM配置列表
            user_proxy: 用户代理实例，如果为None则创建一个新的
        """
        self.config_list = config_list
        self.llm_config = {"config_list": config_list}
        
        self.state = self.STATES["INIT"]
        self._setup_agents(user_proxy)
        self._setup_groupchat()
        
        logger.info("自适应规划团队初始化完成")
    
    def _setup_agents(self, user_proxy):
        """
        设置团队中的智能体
        
        Args:
            user_proxy: 用户代理实例或None
        """
        # 如果未提供user_proxy，则创建一个新的
        if user_proxy is None:
            self.user_proxy = UserProxyAgent(
                name="User",
                human_input_mode="TERMINATE",
                max_consecutive_auto_reply=0,
                system_message="你是最终用户。你的目标将由系统分析，转化为详细计划。",
                code_execution_config={"last_n_messages": 2, "work_dir": "workspace"}
            )
        else:
            self.user_proxy = user_proxy
        
        # 注册用户交互工具
        self.user_proxy.register_function(
            function_map={"ask_user_clarification": ask_user_clarification}
        )
        
        # 创建四个核心智能体
        self.analyst = AnalystAgent(
            name="Analyst",
            llm_config=self.llm_config
        )
        
        self.researcher = ResearcherAgent(
            name="Researcher",
            llm_config=self.llm_config
        )
        
        self.strategist = StrategistAgent(
            name="Strategist",
            llm_config=self.llm_config
        )
        
        self.adaptor = AdaptorAgent(
            name="Adaptor",
            llm_config=self.llm_config
        )
        
        # 存储智能体之间共享的数据
        self.shared_data = {
            "structured_goal": None,
            "research_report": None,
            "plan": None,
            "feedback": None
        }
    
    def _setup_groupchat(self):
        """设置GroupChat和GroupChatManager"""
        # 创建所有参与者的列表
        self.participants = [
            self.user_proxy,
            self.analyst,
            self.researcher,
            self.strategist,
            self.adaptor
        ]
        
        # 创建GroupChat
        self.groupchat = GroupChat(
            agents=self.participants,
            messages=[],
            max_round=50
        )
        
        # 创建GroupChatManager
        self.manager = GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config
        )
    
    def _fsm_transition(self, current_speaker, message_content):
        """
        有限状态机转换逻辑
        
        Args:
            current_speaker: 当前发言的智能体
            message_content: 消息内容
        
        Returns:
            str: 下一个发言者的名称
        """
        logger.info(f"当前状态: {self.state}, 当前发言者: {current_speaker.name}")
        
        # 初始状态
        if self.state == self.STATES["INIT"]:
            self.state = self.STATES["ANALYZING"]
            return "Analyst"
        
        # 目标分析状态
        elif self.state == self.STATES["ANALYZING"]:
            if current_speaker.name == "Analyst" and "structured_goal" in message_content:
                try:
                    # 尝试解析结构化目标
                    import json
                    self.shared_data["structured_goal"] = json.loads(message_content)
                    self.state = self.STATES["RESEARCHING"]
                    return "Researcher"
                except:
                    pass
            return "Analyst"  # 继续分析
        
        # 研究方法状态
        elif self.state == self.STATES["RESEARCHING"]:
            if current_speaker.name == "Researcher" and "research_report" in message_content:
                self.shared_data["research_report"] = message_content
                self.state = self.STATES["PLANNING"]
                return "Strategist"
            return "Researcher"  # 继续研究
        
        # 制定计划状态
        elif self.state == self.STATES["PLANNING"]:
            if current_speaker.name == "Strategist" and "plan" in message_content:
                self.shared_data["plan"] = message_content
                self.state = self.STATES["COMPLETE"]
                return "User"  # 返回给用户
            return "Strategist"  # 继续制定计划
        
        # 处理反馈状态
        elif self.state == self.STATES["FEEDBACK"]:
            if current_speaker.name == "Adaptor":
                if "无需采取行动" in message_content:
                    self.state = self.STATES["COMPLETE"]
                    return "User"
                else:
                    self.state = self.STATES["PLANNING"]
                    return "Strategist"  # 重新规划
            return "Adaptor"
        
        # 完成状态 - 默认返回用户
        return "User"
    
    def run(self, user_objective: str):
        """
        启动自适应规划团队处理用户目标
        
        Args:
            user_objective: 用户的初始目标描述
            
        Returns:
            Dict: 处理结果，包含结构化目标、研究报告和最终计划
        """
        logger.info(f"开始处理用户目标: {user_objective}")
        
        # 重置状态
        self.state = self.STATES["INIT"]
        self.shared_data = {
            "structured_goal": None,
            "research_report": None,
            "plan": None,
            "feedback": None
        }
        
        # 配置GroupChatManager使用我们的状态机
        self.manager.orchestrate_chat(
            director=self._fsm_transition,
            initial_message=f"请帮我分析并制定以下目标的执行计划: {user_objective}"
        )
        
        return {
            "structured_goal": self.shared_data["structured_goal"],
            "research_report": self.shared_data["research_report"],
            "plan": self.shared_data["plan"]
        }
    
    def process_feedback(self, feedback: str):
        """
        处理用户对计划的反馈
        
        Args:
            feedback: 用户反馈文本
            
        Returns:
            Dict: 处理结果
        """
        logger.info(f"处理用户反馈: {feedback}")
        
        # 设置为反馈状态
        self.state = self.STATES["FEEDBACK"]
        self.shared_data["feedback"] = feedback
        
        # 将反馈发送给AdaptorAgent
        self.manager.orchestrate_chat(
            director=self._fsm_transition,
            initial_message=f"用户对计划的反馈: {feedback}"
        )
        
        return {
            "original_plan": self.shared_data["plan"],
            "feedback": feedback,
            "updated_plan": self.shared_data["plan"]  # 如果有重新规划，这里会更新
        } 