# helios_backend/agents/__init__.py

# 此文件用于将本包（package）内的专用智能体模块暴露出去。
# 示例：如果您有一个名为 a_tool_agent.py 的文件，其中定义了 AToolAgent 类，
# 您可以在这里添加一行： from .a_tool_agent import AToolAgent
# 这样，其他模块就可以通过 `from helios_backend.agents import AToolAgent` 来导入。

# 关键原则：此 __init__.py 文件【严禁】从包外的任何模块（如 helios_backend.agent_core）导入任何东西。
# 这样做会重新引入循环依赖的风险。保持此文件只管理其内部模块。

# 目前可以留空，或根据您包内的实际模块进行填充。 