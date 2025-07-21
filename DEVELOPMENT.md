# Helios Adaptive Planner 开发指南

本文档提供了 Helios Adaptive Planner 项目的开发流程、规范和最佳实践。

## 目录

1. [开发环境设置](#开发环境设置)
2. [Git 工作流程](#git-工作流程)
3. [代码规范](#代码规范)
4. [智能体开发指南](#智能体开发指南)
5. [测试指南](#测试指南)
6. [文档规范](#文档规范)

## 开发环境设置

### 后端环境

1. 创建并激活虚拟环境:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

2. 安装依赖:

```bash
cd backend
pip install -r requirements.txt
```

3. 配置环境变量:

```bash
cp .env.example .env
# 编辑.env文件，填写必要的API密钥
```

### 前端环境

1. 安装 Node.js (推荐使用 nvm 进行版本管理):

```bash
# 安装 LTS 版本
nvm install lts
nvm use lts
```

2. 安装依赖:

```bash
cd frontend
npm install
```

## Git 工作流程

我们采用基于功能分支的 Git 工作流程，确保代码质量和项目稳定性。

### 分支策略

![Git 分支策略](https://mermaid.ink/img/pako:eNpNkMFuwjAMhl8l8nmo1HZoD7uMadI4cOTQC4rsBLQQoSShExXv3iQdXXuwZX_-_8Z2h9oqQgZNwy9KmOJ_i6TiZW_OqMl0Yip1JK92Lx-mFdXIRZFNw9XZyK_E9RF9LHWpIoVYysa6KEJazFZvk2wKqHE4obSkaSm1l3bYcZvgHk2mHaEtPF2NbOBI0A3e_ODdxT_D5YSm0GDtEb32SQhhw4ZbDK5BH_iwFyx6cKK4eghPr-hP8LnEoVL2heqfcu4Q-ez6d9V3zw_oc-FsDzVJteXjdoRYSbIBdnA5smDgF7sfUQM=)

- `main`: 主分支，对应生产环境。只接受来自 `develop` 或 hotfix 分支的合并。
- `develop`: 开发集成分支，包含最新的开发特性，但可能不稳定。
- `feature/*`: 特性分支，用于开发新功能。从 `develop` 分支创建，完成后合并回 `develop`。
- `hotfix/*`: 热修复分支，用于修复生产环境中的紧急问题。从 `main` 分支创建，完成后同时合并到 `main` 和 `develop`。
- `release/*`: 发布分支，用于准备新版本发布。从 `develop` 分支创建，完成后合并到 `main` 和 `develop`。

### 分支命名规范

- 特性分支: `feature/简短描述`，例如: `feature/goal-analysis-agent`
- 修复分支: `fix/简短描述`，例如: `fix/memory-leak`
- 热修复分支: `hotfix/简短描述`，例如: `hotfix/critical-api-bug`
- 发布分支: `release/版本号`，例如: `release/v1.0.0`

### 提交消息规范

我们采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范:

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

类型包括:
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `style`: 不影响代码含义的更改（空白、格式化、缺少分号等）
- `refactor`: 既不修复错误也不添加功能的代码更改
- `perf`: 提高性能的代码更改
- `test`: 添加缺失的测试或纠正现有的测试
- `build`: 影响构建系统或外部依赖的更改
- `ci`: 对 CI 配置文件和脚本的更改

示例:
```
feat(agent): 添加目标分析智能体

实现了能够将用户模糊需求转化为SMART目标的智能体。

Closes #123
```

### 工作流程示例

```bash
# 1. 确保本地 develop 分支是最新的
git checkout develop
git pull origin develop

# 2. 创建新的特性分支
git checkout -b feature/goal-analysis-agent

# 3. 进行开发工作
# ... 编码和测试 ...

# 4. 提交更改
git add .
git commit -m "feat(agent): 添加目标分析智能体"

# 5. 将更改推送到远程仓库
git push origin feature/goal-analysis-agent

# 6. 创建 Pull Request 合并到 develop 分支
# (在 GitHub/GitLab 界面上操作)

# 7. 合并后删除特性分支
git branch -d feature/goal-analysis-agent
```

## 代码规范

### Python 代码规范

我们遵循 [PEP 8](https://peps.python.org/pep-0008/) 风格指南:

- 使用 4 个空格进行缩进
- 每行最多 79 个字符
- 使用空行分隔函数和类
- 导入顺序: 标准库、相关第三方库、本地应用/库
- 文档字符串使用 [Google 风格](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### TypeScript 代码规范

我们使用 ESLint 和 Prettier 来强制执行代码风格:

- 使用 2 个空格进行缩进
- 使用分号结束语句
- 优先使用单引号
- 使用箭头函数
- 使用 TypeScript 类型注释

## 智能体开发指南

### 智能体设计原则

1. **单一职责**: 每个智能体应专注于特定类型的任务
2. **清晰界限**: 智能体之间的交互界限应明确
3. **系统消息质量**: system_message 是智能体行为的关键，需精心设计
4. **工具函数分离**: 将复杂操作封装为工具函数
5. **错误恢复**: 智能体应能从失败中恢复

### 核心智能体开发流程

1. **定义职责**: 明确智能体的具体职责和边界
2. **设计系统消息**: 精心设计 system_message，定义智能体角色和行为准则
3. **实现基础类**: 继承自 `ConversableAgent`，配置基本参数
4. **添加工具函数**: 为智能体注册必要的工具函数
5. **单元测试**: 编写测试验证智能体行为
6. **集成测试**: 测试智能体与其他组件的交互

## 测试指南

### 单元测试

使用 pytest 框架进行单元测试:

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_goal_analyst.py

# 运行特定测试函数
pytest tests/test_goal_analyst.py::test_extract_entities
```

### 集成测试

集成测试验证多个智能体之间的协作:

```bash
# 运行集成测试
pytest tests/integration/test_agent_workflow.py
```

### 前端测试

使用 Vitest 运行前端测试:

```bash
cd frontend
npm test
```

## 文档规范

### 代码文档

- 所有公共函数、类和方法都应该有文档字符串
- 文档字符串应包含参数、返回值和异常的描述
- 复杂逻辑应添加内联注释

### 项目文档

- `README.md`: 项目概览、快速开始和基本使用说明
- `DEVELOPMENT.md`: 开发指南和规范
- `DEPLOYMENT.md`: 部署说明
- `/docs`: 存放详细的技术文档 