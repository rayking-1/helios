# Helios Adaptive Planner

Helios是一个智能自适应规划系统，它利用多智能体协作框架帮助用户创建、管理和动态调整个人学习与发展计划。

## 项目概览

Helios由四个核心智能体组成的团队协作完成规划任务：

1. **AnalystAgent (分析智能体)** - 解析和明确用户的目标
2. **ResearcherAgent (研究智能体)** - 收集与目标相关的信息和资源
3. **StrategistAgent (策略智能体)** - 基于分析和研究创建结构化计划
4. **AdaptorAgent (适应智能体)** - 根据用户反馈动态调整计划

系统设计为全栈应用，包括Python后端、React前端，以及WebSocket实时通信。

## 架构与技术栈

### 后端
- **Framework**: FastAPI
- **智能体框架**: pyautogen (AutoGen)
- **数据库**: SQLAlchemy + SQLite/PostgreSQL
- **异步通信**: WebSockets

### 前端
- **Framework**: React + TypeScript
- **状态管理**: Zustand
- **UI组件**: Tailwind CSS
- **网络请求**: React Query

### 部署
- **容器化**: Docker + docker-compose
- **CI/CD**: GitHub Actions

## 快速开始

### 环境准备

1. 确保已安装以下软件:
   - Python 3.10+
   - Node.js 18+
   - Docker (可选，用于容器化部署)

2. 克隆项目:
   ```bash
   git clone https://github.com/your-org/helios_adaptive_planner.git
   cd helios_adaptive_planner
   ```

### Windows开发环境配置 (使用Cursor IDE)

#### Python环境设置
1. 安装Python:
   - 访问 [Python官方网站](https://www.python.org/downloads/windows/) 下载并安装Python 3.10+
   - 安装过程中，确保勾选 "Add Python to PATH" 选项

2. 创建并激活虚拟环境:
   ```powershell
   # 在PowerShell中
   python -m venv venv
   .\venv\Scripts\activate
   
   # 检查Python版本
   python --version
   ```

3. 安装项目依赖:
   ```powershell
   pip install -r requirements.txt
   ```

4. 设置环境变量:
   - 复制 `env-template.txt` 并重命名为 `.env`
   - 编辑 `.env` 文件，填入必要的API密钥和配置
   - 在PowerShell中设置PYTHONPATH:
   ```powershell
   $env:PYTHONPATH="$(Get-Location)"
   ```

#### Node.js环境设置
1. 安装nvm-windows:
   - 访问 [nvm-windows releases](https://github.com/coreybutler/nvm-windows/releases) 下载最新版本
   - 运行安装程序，完成安装

2. 安装Node.js LTS版本:
   ```powershell
   nvm install lts
   nvm use <version_number>  # 例如: nvm use 20.11.1
   
   # 验证安装
   node -v
   npm -v
   ```

3. 安装前端依赖:
   ```powershell
   cd helios-frontend
   npm install
   ```

#### Cursor IDE配置
1. 安装Cursor IDE:
   - 从 [Cursor官方网站](https://cursor.sh/) 下载并安装

2. 安装推荐的扩展插件:
   - 打开Cursor，按下 `Ctrl+Shift+X` 进入扩展市场
   - 搜索并安装以下插件:
     - Python (Microsoft)
     - ESLint (Microsoft)
     - Prettier - Code formatter
     - Tailwind CSS IntelliSense

3. 配置调试环境:
   - 项目中已包含 `.vscode/launch.json` 配置
   - 按下 `Ctrl+Shift+D` 打开调试面板
   - 选择 "Python: Backend Server" 或 "Node.js: Frontend Server" 来调试相应服务

4. 使用AI辅助开发:
   - 使用 `Ctrl+K` 打开AI助手
   - 参考 [ag2 智能体团队开发指南](./DEVELOPMENT.md) 中的Prompt示例进行开发
   - 查看详细的 [Cursor IDE 开发指南](./CURSOR_GUIDE.md) 获取更多技巧

### 后端启动

1. 激活虚拟环境(如未激活):
   ```bash
   # Windows
   .\venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. 验证环境配置:
   ```bash
   python backend/utils/verify_env.py
   ```

3. 启动后端服务:
   ```bash
   python backend/main.py
   ```

### 前端启动

1. 安装依赖(如未安装):
   ```bash
   cd helios-frontend
   npm install
   ```

2. 启动开发服务器:
   ```bash
   npm run dev
   ```

3. 访问应用:
   浏览器中打开 [http://localhost:5173](http://localhost:5173)

### Docker部署 (生产环境)

使用docker-compose一键启动所有服务:

```bash
docker-compose up -d
```

## 项目结构

```
helios_adaptive_planner/
├── backend/                 # Python后端
│   ├── agents/              # 智能体定义
│   │   ├── analyst_agent.py
│   │   ├── researcher_agent.py
│   │   ├── strategist_agent.py
│   │   └── adaptor_agent.py
│   ├── tools/               # 智能体工具函数
│   ├── routers/             # FastAPI路由
│   ├── database/            # 数据库模型和会话管理
│   └── main.py              # 应用入口
├── helios-frontend/         # React前端
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── hooks/           # 自定义Hooks
│   │   ├── store/           # Zustand状态
│   │   └── pages/           # 页面组件
│   └── package.json
├── tests/                   # 测试目录
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── e2e/                 # 端到端测试
├── docker-compose.yml       # Docker编排配置
└── README.md
```

## 开发指南

### 测试

运行后端测试:
```bash
cd backend
python -m pytest
```

运行前端测试:
```bash
cd helios-frontend
npm test
```

运行端到端测试:
```bash
cd backend
python -m pytest tests/e2e/
```

### 性能优化

系统包含两个专用的性能优化指南:

- [前端性能优化指南](helios-frontend/PERFORMANCE_OPTIMIZATION.md)
- [后端性能优化指南](backend/PERFORMANCE_OPTIMIZATION.md)

### 调试指南

项目提供了全面的调试和排错文档:

- [调试手册](backend/DEBUGGING_MANUAL.md) - 包含常见问题解决方案
- [故障排查指南](TROUBLESHOOTING.md) - 环境和配置问题排查

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议!

1. Fork项目仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的修改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

请确保您的代码符合项目的编码风格，并且所有测试都能通过。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 
```
helios_adaptive_planner/
├── helios/                    # FastAPI 后端
│   ├── database/              # 数据库层 (SQLAlchemy ORM)
│   ├── repositories/          # 数据访问层 (仓储模式)
│   ├── routers/               # API 路由
│   ├── security/              # 认证和授权
│   └── services/              # 业务服务
├── helios_backend/            # 智能体后端
│   ├── agents/                # 智能体定义
│   │   ├── goal_analyst.py    # 目标分析智能体
│   │   ├── methodology_researcher.py  # 方法研究智能体
│   │   ├── dynamic_planner.py  # 动态规划智能体
│   │   └── feedback_adapter.py  # 反馈适应智能体
│   ├── tools/                 # 工具函数
│   ├── agent_team.py          # 多智能体协作系统
│   └── model_config.py        # LLM 模型配置
├── helios-frontend/           # React 前端
│   ├── src/
│   │   ├── api/               # API 调用
│   │   ├── components/        # React 组件
│   │   ├── hooks/             # 自定义 Hooks
│   │   └── store/             # 状态管理 (Zustand)
│   └── package.json           # 依赖和脚本
└── examples/                  # 示例脚本
```

## 开发指南

### 调试配置

使用Cursor IDE调试项目:

1. 按 `Ctrl+Shift+D` 打开调试侧边栏
2. 选择相应的启动配置:
   - `Python: Backend Server`: 启动智能体后端
   - `Python: FastAPI Server`: 启动API服务
   - `Node.js: Frontend Server`: 启动前端开发服务器

### 测试

运行测试:

```bash
# 智能体后端测试
cd helios_backend
pytest

# API服务测试
cd helios
pytest
```

## 部署

详细部署说明请参阅 [DEPLOYMENT.md](DEPLOYMENT.md)

## 技术栈

- **后端**: Python, FastAPI, SQLAlchemy, AutoGen (ag2)
- **前端**: React, TypeScript, Zustand, TailwindCSS
- **数据库**: PostgreSQL
- **容器化**: Docker, Docker Compose
- **云部署**: AWS (App Runner, RDS, ECR)

## 许可证

[MIT License](LICENSE) 
```
helios_adaptive_planner/
├── backend/                 # Python后端
│   ├── agents/              # 智能体定义
│   │   ├── analyst_agent.py
│   │   ├── researcher_agent.py
│   │   ├── strategist_agent.py
│   │   └── adaptor_agent.py
│   ├── tools/               # 智能体工具函数
│   ├── routers/             # FastAPI路由
│   ├── database/            # 数据库模型和会话管理
│   └── main.py              # 应用入口
├── helios-frontend/         # React前端
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── hooks/           # 自定义Hooks
│   │   ├── store/           # Zustand状态
│   │   └── pages/           # 页面组件
│   └── package.json
├── tests/                   # 测试目录
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── e2e/                 # 端到端测试
├── docker-compose.yml       # Docker编排配置
└── README.md
```

## 开发指南

### 测试

运行后端测试:
```bash
cd backend
python -m pytest
```

运行前端测试:
```bash
cd helios-frontend
npm test
```

运行端到端测试:
```bash
cd backend
python -m pytest tests/e2e/
```

### 性能优化

系统包含两个专用的性能优化指南:

- [前端性能优化指南](helios-frontend/PERFORMANCE_OPTIMIZATION.md)
- [后端性能优化指南](backend/PERFORMANCE_OPTIMIZATION.md)

### 调试指南

项目提供了全面的调试和排错文档:

- [调试手册](backend/DEBUGGING_MANUAL.md) - 包含常见问题解决方案
- [故障排查指南](TROUBLESHOOTING.md) - 环境和配置问题排查

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议!

1. Fork项目仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的修改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

请确保您的代码符合项目的编码风格，并且所有测试都能通过。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 
```
helios_adaptive_planner/
├── helios/                    # FastAPI 后端
│   ├── database/              # 数据库层 (SQLAlchemy ORM)
│   ├── repositories/          # 数据访问层 (仓储模式)
│   ├── routers/               # API 路由
│   ├── security/              # 认证和授权
│   └── services/              # 业务服务
├── helios_backend/            # 智能体后端
│   ├── agents/                # 智能体定义
│   │   ├── goal_analyst.py    # 目标分析智能体
│   │   ├── methodology_researcher.py  # 方法研究智能体
│   │   ├── dynamic_planner.py  # 动态规划智能体
│   │   └── feedback_adapter.py  # 反馈适应智能体
│   ├── tools/                 # 工具函数
│   ├── agent_team.py          # 多智能体协作系统
│   └── model_config.py        # LLM 模型配置
├── helios-frontend/           # React 前端
│   ├── src/
│   │   ├── api/               # API 调用
│   │   ├── components/        # React 组件
│   │   ├── hooks/             # 自定义 Hooks
│   │   └── store/             # 状态管理 (Zustand)
│   └── package.json           # 依赖和脚本
└── examples/                  # 示例脚本
```

## 开发指南

### 调试配置

使用Cursor IDE调试项目:

1. 按 `Ctrl+Shift+D` 打开调试侧边栏
2. 选择相应的启动配置:
   - `Python: Backend Server`: 启动智能体后端
   - `Python: FastAPI Server`: 启动API服务
   - `Node.js: Frontend Server`: 启动前端开发服务器

### 测试

运行测试:

```bash
# 智能体后端测试
cd helios_backend
pytest

# API服务测试
cd helios
pytest
```

## 部署

详细部署说明请参阅 [DEPLOYMENT.md](DEPLOYMENT.md)

## 技术栈

- **后端**: Python, FastAPI, SQLAlchemy, AutoGen (ag2)
- **前端**: React, TypeScript, Zustand, TailwindCSS
- **数据库**: PostgreSQL
- **容器化**: Docker, Docker Compose
- **云部署**: AWS (App Runner, RDS, ECR)

## 许可证

[MIT License](LICENSE) 