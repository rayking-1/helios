# Helios Adaptive Planner - 核心智能体架构

本项目实现了基于AutoGen (ag2) 框架的自适应规划系统，使用多智能体协作构建高质量、可调整的计划。

## 架构概述

系统由四个核心智能体组成，每个智能体专注于特定功能：

1. **AnalystAgent (目标分析智能体)**：
   - 将用户的模糊意图解构为结构化的SMART目标
   - 使用工具：`ask_user_clarification`, `extract_entities`

2. **ResearcherAgent (方法研究智能体)**：
   - 发现并综合有效的、有证据支持的方法
   - 使用工具：`web_search`, `summarize_document`

3. **StrategistAgent (动态规划智能体)**：
   - 根据目标和方法构建详细的、可执行的计划
   - 使用工具：`create_task_graph`

4. **AdaptorAgent (反馈循环智能体)**：
   - 解读用户反馈并触发自适应重新规划
   - 使用工具：`interpret_feedback`

这些智能体通过`AdaptivePlanTeam`类协调，使用有限状态机(FSM)管理工作流程。

## 目录结构

```
backend/
├── agents/                  # 智能体模块
│   ├── analyst_agent.py     # 目标分析智能体
│   ├── researcher_agent.py  # 方法研究智能体
│   ├── strategist_agent.py  # 动态规划智能体
│   └── adaptor_agent.py     # 反馈循环智能体
├── tools/                   # 工具函数
│   ├── user_interaction_tools.py
│   ├── research_tools.py
│   ├── planning_tools.py
│   └── feedback_tools.py
├── tests/                   # 单元测试
│   ├── test_analyst_agent.py
│   ├── test_researcher_agent.py
│   ├── test_strategist_agent.py
│   └── test_adaptor_agent.py
├── examples/                # 使用示例
│   └── plan_example.py
└── agent_team.py            # 智能体团队协调类
```

## 快速开始

### 环境设置

1. 安装依赖:
```bash
pip install pyautogen fastapi uvicorn python-dotenv pytest httpx aiohttp
```

2. 配置环境变量:
```bash
# 在.env文件中配置API密钥
DASHSCOPE_API_KEY=your_dashscope_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 运行示例

```python
from backend.agent_team import AdaptivePlanTeam

# 设置LLM配置
config_list = [
    {
        "model": "qwen-max",
        "api_key": "your_dashscope_api_key"
    }
]

# 初始化团队
team = AdaptivePlanTeam(config_list=config_list)

# 处理用户目标
result = team.run("我想在3个月内学习Python数据科学，每周可以投入15小时")

# 处理用户反馈
feedback_result = team.process_feedback("我觉得这个计划有点太难了")
```

更详细的示例请参考`examples/plan_example.py`。

## 测试

运行单元测试:
```bash
cd backend
pytest
```

## 工作流程

1. **目标分析**: AnalystAgent将用户输入转换为结构化目标
2. **方法研究**: ResearcherAgent搜索和总结可行的方法
3. **计划生成**: StrategistAgent生成详细的行动计划
4. **反馈处理**: AdaptorAgent解读反馈并触发调整

整个流程由有限状态机控制，确保智能体之间的有序协作。

## 扩展

本系统设计为模块化，可以通过以下方式扩展:

- 添加新的智能体到团队中
- 为现有智能体增强或添加工具功能
- 调整状态机逻辑以支持更复杂的工作流
- 连接到外部数据源或API

## 引用

基于AutoGen (ag2) 框架:
- Microsoft AutoGen: https://microsoft.github.io/autogen/ 