# Cursor IDE 开发指南

本指南详细介绍如何使用Cursor IDE有效地开发Helios自适应规划系统，特别是如何利用其AI辅助功能进行智能体开发。

## Cursor IDE简介

Cursor是一个基于VSCode的AI增强型代码编辑器，它集成了强大的AI辅助功能，可以帮助您更高效地编写、理解和重构代码。

### 主要AI功能
- **AI Chat (Ctrl+K)**: 与AI助手对话，生成代码、解释代码、获取建议
- **生成测试 (Ctrl+Shift+L)**: 为选中的代码自动生成测试
- **代码解释**: 让AI解释选定的代码片段
- **错误诊断**: AI帮助诊断和修复代码错误

## 安装和配置

1. 从[Cursor官网](https://cursor.sh/)下载并安装最新版本
2. 首次启动时，登录或创建账号
3. 打开项目文件夹 (File > Open Folder...)
4. 自动安装推荐的扩展（查看`.vscode/extensions.json`）

## 开发智能体的最佳实践

### 1. 创建新智能体

使用AI Chat (Ctrl+K) 生成智能体基本结构：

```
请使用pyautogen框架创建一个名为[智能体名称]Agent的新智能体类，
它继承自autogen.ConversableAgent。

这个智能体的主要职责是：[描述职责]

它需要包含以下方法：
1. __init__: 接收name、llm_config等参数，设置system_message
2. [主要方法名]: 实现核心功能
3. [其他方法名]: 辅助功能

请确保代码遵循PEP 8规范，并包含详细的文档字符串。
```

### 2. 改进系统消息

系统消息是智能体行为的关键。使用AI优化system_message：

```
分析以下智能体的system_message，并提出改进建议：

[粘贴当前system_message]

请考虑以下方面：
1. 角色定义是否明确
2. 任务描述是否具体
3. 输出格式是否规范
4. 约束条件是否清晰
```

### 3. 生成智能体单元测试

选中整个智能体类，按下Ctrl+Shift+L，并使用以下提示：

```
为这个智能体类生成完整的pytest单元测试。

测试应该包括：
1. 测试初始化参数设置正确
2. 测试主要方法在正常输入下的行为
3. 测试主要方法在边界情况下的行为
4. 使用mock/monkeypatch模拟依赖

请确保测试覆盖所有公共方法和关键功能路径。
```

### 4. 使用AI调试问题

遇到问题时，选中相关代码和错误消息，使用Ctrl+K：

```
我遇到了以下错误：
[粘贴错误消息]

相关代码：
[粘贴相关代码]

请分析问题原因，并提供解决方案。
```

## 智能体开发Prompt示例

### AnalystAgent开发

```
请使用pyautogen框架实现一个AnalystAgent（分析智能体）类，继承自autogen.ConversableAgent。

此智能体负责分析和明确用户目标，具体职责包括：
1. 识别用户输入中的模糊或不明确的目标表述
2. 通过提问引导用户明确具体的目标、时间框架和约束条件
3. 将模糊目标转化为结构化的SMART目标

需要实现以下方法：
1. process_message(message: str) -> str: 分析输入消息，返回结构化目标或提出澄清问题
2. 所有必要的辅助方法

智能体需要能够调用ask_user_clarification工具获取更多信息。
```

### ResearcherAgent开发

```
请使用pyautogen框架实现一个ResearcherAgent（研究智能体）类，继承自autogen.ConversableAgent。

此智能体负责查找和整理与用户目标相关的信息和方法，具体职责包括：
1. 根据结构化目标生成相关的研究查询
2. 调用web_search工具搜索相关信息
3. 整合和总结找到的信息，形成研究报告

需要实现以下方法：
1. generate_research_plan(structured_goal: dict) -> str: 生成研究计划并执行研究
2. summarize_findings(search_results: list) -> str: 总结研究发现
3. 所有必要的辅助方法
```

### StrategistAgent开发

```
请使用pyautogen框架实现一个StrategistAgent（策略智能体）类，继承自autogen.ConversableAgent。

此智能体负责根据分析结果和研究创建详细的行动计划，具体职责包括：
1. 根据结构化目标和研究报告设计行动计划
2. 创建包含任务、截止日期和依赖关系的计划
3. 确保计划具有合理的结构和可行性

需要实现以下方法：
1. generate_plan(goal: dict, research: str) -> str: 生成详细的JSON格式行动计划
2. validate_plan(plan: list) -> bool: 验证计划的有效性和逻辑性
3. 所有必要的辅助方法
```

### AdaptorAgent开发

```
请使用pyautogen框架实现一个AdaptorAgent（适应智能体）类，继承自autogen.ConversableAgent。

此智能体负责处理用户反馈并调整计划，具体职责包括：
1. 解析和分类用户反馈
2. 根据反馈类型确定调整策略
3. 生成修订计划的指令

需要实现以下方法：
1. process_feedback(feedback_text: str) -> str: 分析用户反馈并产生相应的调整建议
2. classify_feedback(feedback: str) -> str: 将反馈分类为预定义的类别
3. 所有必要的辅助方法
```

## 使用AI辅助开发前端组件

开发React组件时的示例提示：

```
请创建一个React组件，用于显示智能体生成的计划。

组件需求：
1. 使用TypeScript和函数式组件
2. 使用Tailwind CSS进行样式设置
3. 接收plan对象作为props，包含tasks数组
4. 每个任务显示标题、截止日期和完成状态
5. 允许用户点击任务提交反馈

组件应具有响应式设计，在移动设备上也能良好显示。
```

## 调试技巧

1. 使用Cursor的内联调试功能（鼠标悬停在变量上）
2. 在调试面板中设置断点（F9）
3. 使用"运行和调试"面板（Ctrl+Shift+D）选择适当的启动配置
4. 使用调试控制台查看变量值和执行表达式

## 注意事项

- 确保在生成代码后进行审核，不要完全依赖AI生成的代码
- 生成的测试可能需要手动调整以适应特定场景
- 保持prompt简洁明确，必要时分步骤生成复杂代码
- 定期更新Cursor以获取最新的AI功能 
 

本指南详细介绍如何使用Cursor IDE有效地开发Helios自适应规划系统，特别是如何利用其AI辅助功能进行智能体开发。

## Cursor IDE简介

Cursor是一个基于VSCode的AI增强型代码编辑器，它集成了强大的AI辅助功能，可以帮助您更高效地编写、理解和重构代码。

### 主要AI功能
- **AI Chat (Ctrl+K)**: 与AI助手对话，生成代码、解释代码、获取建议
- **生成测试 (Ctrl+Shift+L)**: 为选中的代码自动生成测试
- **代码解释**: 让AI解释选定的代码片段
- **错误诊断**: AI帮助诊断和修复代码错误

## 安装和配置

1. 从[Cursor官网](https://cursor.sh/)下载并安装最新版本
2. 首次启动时，登录或创建账号
3. 打开项目文件夹 (File > Open Folder...)
4. 自动安装推荐的扩展（查看`.vscode/extensions.json`）

## 开发智能体的最佳实践

### 1. 创建新智能体

使用AI Chat (Ctrl+K) 生成智能体基本结构：

```
请使用pyautogen框架创建一个名为[智能体名称]Agent的新智能体类，
它继承自autogen.ConversableAgent。

这个智能体的主要职责是：[描述职责]

它需要包含以下方法：
1. __init__: 接收name、llm_config等参数，设置system_message
2. [主要方法名]: 实现核心功能
3. [其他方法名]: 辅助功能

请确保代码遵循PEP 8规范，并包含详细的文档字符串。
```

### 2. 改进系统消息

系统消息是智能体行为的关键。使用AI优化system_message：

```
分析以下智能体的system_message，并提出改进建议：

[粘贴当前system_message]

请考虑以下方面：
1. 角色定义是否明确
2. 任务描述是否具体
3. 输出格式是否规范
4. 约束条件是否清晰
```

### 3. 生成智能体单元测试

选中整个智能体类，按下Ctrl+Shift+L，并使用以下提示：

```
为这个智能体类生成完整的pytest单元测试。

测试应该包括：
1. 测试初始化参数设置正确
2. 测试主要方法在正常输入下的行为
3. 测试主要方法在边界情况下的行为
4. 使用mock/monkeypatch模拟依赖

请确保测试覆盖所有公共方法和关键功能路径。
```

### 4. 使用AI调试问题

遇到问题时，选中相关代码和错误消息，使用Ctrl+K：

```
我遇到了以下错误：
[粘贴错误消息]

相关代码：
[粘贴相关代码]

请分析问题原因，并提供解决方案。
```

## 智能体开发Prompt示例

### AnalystAgent开发

```
请使用pyautogen框架实现一个AnalystAgent（分析智能体）类，继承自autogen.ConversableAgent。

此智能体负责分析和明确用户目标，具体职责包括：
1. 识别用户输入中的模糊或不明确的目标表述
2. 通过提问引导用户明确具体的目标、时间框架和约束条件
3. 将模糊目标转化为结构化的SMART目标

需要实现以下方法：
1. process_message(message: str) -> str: 分析输入消息，返回结构化目标或提出澄清问题
2. 所有必要的辅助方法

智能体需要能够调用ask_user_clarification工具获取更多信息。
```

### ResearcherAgent开发

```
请使用pyautogen框架实现一个ResearcherAgent（研究智能体）类，继承自autogen.ConversableAgent。

此智能体负责查找和整理与用户目标相关的信息和方法，具体职责包括：
1. 根据结构化目标生成相关的研究查询
2. 调用web_search工具搜索相关信息
3. 整合和总结找到的信息，形成研究报告

需要实现以下方法：
1. generate_research_plan(structured_goal: dict) -> str: 生成研究计划并执行研究
2. summarize_findings(search_results: list) -> str: 总结研究发现
3. 所有必要的辅助方法
```

### StrategistAgent开发

```
请使用pyautogen框架实现一个StrategistAgent（策略智能体）类，继承自autogen.ConversableAgent。

此智能体负责根据分析结果和研究创建详细的行动计划，具体职责包括：
1. 根据结构化目标和研究报告设计行动计划
2. 创建包含任务、截止日期和依赖关系的计划
3. 确保计划具有合理的结构和可行性

需要实现以下方法：
1. generate_plan(goal: dict, research: str) -> str: 生成详细的JSON格式行动计划
2. validate_plan(plan: list) -> bool: 验证计划的有效性和逻辑性
3. 所有必要的辅助方法
```

### AdaptorAgent开发

```
请使用pyautogen框架实现一个AdaptorAgent（适应智能体）类，继承自autogen.ConversableAgent。

此智能体负责处理用户反馈并调整计划，具体职责包括：
1. 解析和分类用户反馈
2. 根据反馈类型确定调整策略
3. 生成修订计划的指令

需要实现以下方法：
1. process_feedback(feedback_text: str) -> str: 分析用户反馈并产生相应的调整建议
2. classify_feedback(feedback: str) -> str: 将反馈分类为预定义的类别
3. 所有必要的辅助方法
```

## 使用AI辅助开发前端组件

开发React组件时的示例提示：

```
请创建一个React组件，用于显示智能体生成的计划。

组件需求：
1. 使用TypeScript和函数式组件
2. 使用Tailwind CSS进行样式设置
3. 接收plan对象作为props，包含tasks数组
4. 每个任务显示标题、截止日期和完成状态
5. 允许用户点击任务提交反馈

组件应具有响应式设计，在移动设备上也能良好显示。
```

## 调试技巧

1. 使用Cursor的内联调试功能（鼠标悬停在变量上）
2. 在调试面板中设置断点（F9）
3. 使用"运行和调试"面板（Ctrl+Shift+D）选择适当的启动配置
4. 使用调试控制台查看变量值和执行表达式

## 注意事项

- 确保在生成代码后进行审核，不要完全依赖AI生成的代码
- 生成的测试可能需要手动调整以适应特定场景
- 保持prompt简洁明确，必要时分步骤生成复杂代码
- 定期更新Cursor以获取最新的AI功能 
 
 