# Helios Adaptive Planner - 前后端集成指南

本文档提供了 Helios Adaptive Planner 项目前后端集成的技术细节与操作指南。

## 1. 架构概述

系统采用了现代的前后端分离架构：

- **后端**: FastAPI (Python) RESTful API + WebSocket 服务
- **前端**: React (TypeScript) + Zustand 状态管理
- **通信**: HTTP API + WebSocket 实时通信
- **部署**: Docker 容器化 + GitHub Actions CI/CD

## 2. API接口

### 2.1 核心端点

| 功能 | HTTP方法 | 端点路径 | 描述 |
|------|----------|----------|------|
| 启动新规划 | POST | `/api/v1/plans` | 接收用户初始目标，启动多智能体协作流程 |
| 获取当前计划 | GET | `/api/v1/plans/current` | 获取用户当前激活的最新版本计划 |
| 查询任务状态 | GET | `/api/v1/tasks/{taskId}` | 获取特定任务的详细信息和状态 |
| 提交任务反馈 | POST | `/api/v1/tasks/{taskId}/feedback` | 用户提交对任务的反馈，触发反馈循环智能体 |
| 获取系统状态 | GET | `/api/v1/system/status` | 查询后端智能体团队的当前工作状态 |

### 2.2 请求与响应格式

所有API响应均为JSON格式。请求体需要符合定义的Pydantic模型。

示例：
```json
// POST /api/v1/plans 请求体
{
  "goal": "我想在3个月内学习Python数据科学",
  "timeframe": "3个月",
  "constraints": ["每周投入15小时"]
}
```

## 3. WebSocket集成

### 3.1 连接端点

WebSocket连接端点: `ws://[host]/ws/{user_id}`

### 3.2 消息类型

系统通过WebSocket发送的消息类型包括：

- `PLAN_UPDATED`: 当计划被创建或更新时
- `AGENT_MESSAGE`: 当智能体产生新的消息时
- `STATUS_CHANGE`: 当系统状态变化时
- `CONNECTION_ESTABLISHED`: 当WebSocket连接建立时

### 3.3 前端集成

在前端代码中，使用`useWebSocketUpdates` Hook来处理WebSocket连接和消息：

```typescript
const { isConnected, lastMessage, sendMessage } = useWebSocketUpdates(userId);
```

## 4. 状态管理

前端使用Zustand进行状态管理，主要状态包括：

- 用户信息
- 当前计划
- 计划历史
- 智能体消息
- 系统状态

## 5. 环境变量配置

项目使用`.env`文件管理环境变量。重要配置项包括：

### 后端环境变量
- `PORT`: 服务端口
- `SECRET_KEY`: 安全密钥
- `DATABASE_URL`: 数据库连接字符串
- `LLM API密钥`: 各种大语言模型API密钥

### 前端环境变量
- `VITE_API_BASE_URL`: 后端API基础URL
- `VITE_API_WS_URL`: WebSocket连接URL

## 6. 部署流程

### 6.1 Docker容器化

项目使用Docker进行容器化部署，包含三个主要服务：
- `backend`: 后端API服务
- `frontend`: 前端静态服务
- `db`: PostgreSQL数据库

### 6.2 CI/CD流程

使用GitHub Actions进行CI/CD，工作流程：
1. 运行单元测试
2. 构建前端并部署到Vercel
3. 构建后端Docker镜像并推送到Docker Hub
4. 通过SSH连接部署服务器并更新容器

## 7. 快速启动指南

1. 克隆项目仓库
2. 创建`.env`文件（参考`.env.example`）
3. 启动容器：`docker-compose up -d`
4. 访问前端: `http://localhost`
5. 访问API文档: `http://localhost:8000/docs`

## 8. 故障排除

常见问题及解决方案：

- WebSocket连接失败: 检查CORS配置和代理设置
- 数据库连接错误: 验证DATABASE_URL格式和权限
- API调用失败: 检查授权令牌和请求格式

## 9. 开发指南

### 前端开发

添加新组件或页面时:
1. 创建组件文件
2. 使用`useWebSocketUpdates`和`useAppStore`获取实时数据
3. 使用`planApi`进行API调用

### 后端开发

添加新端点时:
1. 在`routes/`目录下创建或更新路由文件
2. 定义Pydantic模型
3. 实现异步处理函数
4. 更新WebSocket通知逻辑 
 

本文档提供了 Helios Adaptive Planner 项目前后端集成的技术细节与操作指南。

## 1. 架构概述

系统采用了现代的前后端分离架构：

- **后端**: FastAPI (Python) RESTful API + WebSocket 服务
- **前端**: React (TypeScript) + Zustand 状态管理
- **通信**: HTTP API + WebSocket 实时通信
- **部署**: Docker 容器化 + GitHub Actions CI/CD

## 2. API接口

### 2.1 核心端点

| 功能 | HTTP方法 | 端点路径 | 描述 |
|------|----------|----------|------|
| 启动新规划 | POST | `/api/v1/plans` | 接收用户初始目标，启动多智能体协作流程 |
| 获取当前计划 | GET | `/api/v1/plans/current` | 获取用户当前激活的最新版本计划 |
| 查询任务状态 | GET | `/api/v1/tasks/{taskId}` | 获取特定任务的详细信息和状态 |
| 提交任务反馈 | POST | `/api/v1/tasks/{taskId}/feedback` | 用户提交对任务的反馈，触发反馈循环智能体 |
| 获取系统状态 | GET | `/api/v1/system/status` | 查询后端智能体团队的当前工作状态 |

### 2.2 请求与响应格式

所有API响应均为JSON格式。请求体需要符合定义的Pydantic模型。

示例：
```json
// POST /api/v1/plans 请求体
{
  "goal": "我想在3个月内学习Python数据科学",
  "timeframe": "3个月",
  "constraints": ["每周投入15小时"]
}
```

## 3. WebSocket集成

### 3.1 连接端点

WebSocket连接端点: `ws://[host]/ws/{user_id}`

### 3.2 消息类型

系统通过WebSocket发送的消息类型包括：

- `PLAN_UPDATED`: 当计划被创建或更新时
- `AGENT_MESSAGE`: 当智能体产生新的消息时
- `STATUS_CHANGE`: 当系统状态变化时
- `CONNECTION_ESTABLISHED`: 当WebSocket连接建立时

### 3.3 前端集成

在前端代码中，使用`useWebSocketUpdates` Hook来处理WebSocket连接和消息：

```typescript
const { isConnected, lastMessage, sendMessage } = useWebSocketUpdates(userId);
```

## 4. 状态管理

前端使用Zustand进行状态管理，主要状态包括：

- 用户信息
- 当前计划
- 计划历史
- 智能体消息
- 系统状态

## 5. 环境变量配置

项目使用`.env`文件管理环境变量。重要配置项包括：

### 后端环境变量
- `PORT`: 服务端口
- `SECRET_KEY`: 安全密钥
- `DATABASE_URL`: 数据库连接字符串
- `LLM API密钥`: 各种大语言模型API密钥

### 前端环境变量
- `VITE_API_BASE_URL`: 后端API基础URL
- `VITE_API_WS_URL`: WebSocket连接URL

## 6. 部署流程

### 6.1 Docker容器化

项目使用Docker进行容器化部署，包含三个主要服务：
- `backend`: 后端API服务
- `frontend`: 前端静态服务
- `db`: PostgreSQL数据库

### 6.2 CI/CD流程

使用GitHub Actions进行CI/CD，工作流程：
1. 运行单元测试
2. 构建前端并部署到Vercel
3. 构建后端Docker镜像并推送到Docker Hub
4. 通过SSH连接部署服务器并更新容器

## 7. 快速启动指南

1. 克隆项目仓库
2. 创建`.env`文件（参考`.env.example`）
3. 启动容器：`docker-compose up -d`
4. 访问前端: `http://localhost`
5. 访问API文档: `http://localhost:8000/docs`

## 8. 故障排除

常见问题及解决方案：

- WebSocket连接失败: 检查CORS配置和代理设置
- 数据库连接错误: 验证DATABASE_URL格式和权限
- API调用失败: 检查授权令牌和请求格式

## 9. 开发指南

### 前端开发

添加新组件或页面时:
1. 创建组件文件
2. 使用`useWebSocketUpdates`和`useAppStore`获取实时数据
3. 使用`planApi`进行API调用

### 后端开发

添加新端点时:
1. 在`routes/`目录下创建或更新路由文件
2. 定义Pydantic模型
3. 实现异步处理函数
4. 更新WebSocket通知逻辑 
 
 