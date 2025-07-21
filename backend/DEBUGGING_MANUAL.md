# Helios自适应规划系统调试手册

## 1. 介绍

本手册为`helios_adaptive_plann`项目的多智能体系统提供调试和问题排查指南。我们的系统由四个核心智能体（分析师、研究员、策略师、适配器）组成，它们之间的协作过程可能会遇到各种问题。本手册旨在帮助开发者快速识别和解决这些问题。

## 2. 常见问题与排查思路

| 问题现象 | 可能原因 | 排查步骤 | 解决方案 |
| :--- | :--- | :--- | :--- |
| 智能体不响应或卡住 | - LLM API密钥无效或额度耗尽<br>- 系统消息有语法错误<br>- 等待一个不存在的工具调用响应 | 1. 检查日志中是否有API调用错误<br>2. 验证环境变量中的API密钥<br>3. 检查工具注册是否完整 | - 更新API密钥<br>- 修复系统消息<br>- 确保所有工具都已正确注册 |
| 计划陷入循环 | - 智能体之间形成指令循环<br>- 状态机未定义明确的终止条件 | 1. 检查跟踪ID的完整对话历史<br>2. 识别重复的消息模式<br>3. 检查FSM状态转换逻辑 | - 修改智能体的系统消息<br>- 在状态机中设置最大迭代次数<br>- 添加明确的退出条件 |
| 研究工具调用失败 | - API限流<br>- 网络连接问题<br>- 工具函数异常 | 1. 检查日志中的HTTP错误<br>2. 检查网络连接<br>3. 尝试手动调用工具函数 | - 实现重试机制<br>- 添加备用API<br>- 修复工具函数 |
| WebSocket连接断开 | - 后端重启<br>- 客户端网络问题<br>- 连接超时 | 1. 检查前端控制台日志<br>2. 检查后端WebSocket日志<br>3. 使用网络工具验证连接 | - 实现自动重连机制<br>- 增加心跳包<br>- 优化连接超时设置 |
| 前端界面无响应 | - JavaScript错误<br>- 状态管理问题<br>- 后端数据格式变更 | 1. 检查浏览器控制台错误<br>2. 验证API响应格式<br>3. 检查React组件生命周期 | - 修复JavaScript错误<br>- 更新状态管理逻辑<br>- 确保前后端数据契约一致 |

## 3. 日志检查与分析技术

### 3.1 结构化日志分析

所有系统日志都采用JSON格式输出，包含以下字段：
```json
{
  "timestamp": "2025-07-20T06:55:15Z",
  "level": "INFO",
  "trace_id": "trace-xyz-123",
  "agent_name": "ResearcherAgent",
  "event_type": "tool_call",
  "message": "Called web_search API",
  "details": {
    "query": "Python learning methods"
  }
}
```

可以使用以下Cursor AI提示快速分析日志：
> "分析以下JSON日志，找出所有ERROR级别的事件，并按agent_name分组统计出错次数。"

### 3.2 追踪ID的使用

每个用户会话都有一个唯一的追踪ID (`trace_id`)。要查看特定会话的全部日志：

```shell
grep "trace-xyz-123" helios_backend.log | jq
```

### 3.3 智能体通信链调试

使用 `ag2` 的 `GroupChatManager` 可以记录所有智能体之间的通信：

```python
groupchat.messages  # 包含所有消息历史
```

## 4. 高级调试技术

### 4.1 模拟特定智能体

在测试复杂场景时，可以模拟特定智能体的行为：

```python
# 模拟研究智能体，使其始终返回固定结果
class MockResearcherAgent:
    def generate_research_plan(self, goal):
        return "模拟的研究结果"

# 在agent_team.py中临时替换
team.researcher = MockResearcherAgent()
```

### 4.2 状态机检查工具

为了验证状态机逻辑，使用以下工具函数：

```python
def dump_fsm_state(team):
    """打印状态机当前状态和转换历史"""
    print(f"当前状态: {team.state}")
    print(f"状态转换历史: {team.state_history}")
    print(f"共享数据: {team.shared_data}")
```

### 4.3 API响应模拟

使用 `responses` 库模拟外部API：

```python
import responses

@responses.activate
def test_web_search():
    responses.add(
        responses.GET,
        "https://api.example.com/search",
        json={"results": [{"title": "测试结果"}]},
        status=200
    )
    # 测试代码...
```

## 5. 性能优化与监控

### 5.1 性能瓶颈识别

使用以下Cursor提示分析潜在的性能瓶颈：
> "分析这段Python代码，识别任何可能的性能瓶颈，特别是阻塞I/O操作和低效的数据结构。"

### 5.2 内存泄漏检测

使用 `memory_profiler` 监控内存使用：

```shell
pip install memory_profiler
python -m memory_profiler backend/main.py
```

## 6. 常见错误代码和解释

| 错误码 | 描述 | 可能原因 | 解决方案 |
| :--- | :--- | :--- | :--- |
| `ERR-LLM-001` | LLM API调用失败 | API密钥无效或额度耗尽 | 检查并更新API密钥 |
| `ERR-TOOL-002` | 工具调用超时 | 网络延迟或外部服务不可用 | 实现重试机制，增加超时时间 |
| `ERR-FSM-003` | 状态机转换错误 | 未定义的状态转换 | 检查并修复状态机定义 |
| `ERR-WS-004` | WebSocket连接断开 | 客户端网络问题或后端重启 | 实现自动重连机制 |
| `ERR-DB-005` | 数据库操作失败 | 连接问题或模式不匹配 | 检查数据库连接和模式定义 |

## 7. 健康检查与诊断脚本

使用以下脚本快速检查系统健康状态：

```shell
python scripts/system_health_check.py
```

该脚本会检查：
- LLM API连接状态
- 数据库连接
- 各种工具功能
- WebSocket服务器状态

## 8. 日志级别与详细度调整

通过环境变量调整日志级别：

```shell
# 设置为DEBUG可查看所有细节
export LOG_LEVEL=DEBUG

# 设置为INFO仅查看关键信息
export LOG_LEVEL=INFO

# 设置为ERROR仅查看错误
export LOG_LEVEL=ERROR
```

## 9. 与支持团队联系

如果上述方法无法解决问题，请联系支持团队：
- 技术支持邮箱: support@helios-team.com
- 内部Slack频道: #helios-support 
 
 