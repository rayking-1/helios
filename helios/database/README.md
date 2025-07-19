# Helios 持久化层

本文档提供了 Helios 项目持久化层的使用说明和技术细节。

## 架构概述

Helios 持久化层采用仓储模式（Repository Pattern）设计，将业务逻辑与数据访问逻辑解耦，提高代码的可维护性和可测试性。主要组件包括：

1. **数据库模型（Models）**：使用 SQLAlchemy ORM 定义的实体模型
2. **仓储类（Repositories）**：提供数据访问抽象层
3. **依赖注入（Dependencies）**：用于 FastAPI 的依赖注入系统

## 核心实体

- **User**：系统用户
- **Task**：用户创建的任务
- **ConversationMessage**：任务执行过程中的对话消息

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库连接

在 `.env` 文件中添加数据库连接字符串：

```
DATABASE_URL=postgresql://username:password@localhost:5432/helios
```

### 3. 初始化数据库

```python
from helios.database.migrations import create_tables

# 创建所有表
create_tables()
```

### 4. 使用仓储类

```python
from sqlalchemy.orm import Session
from helios.repositories.task_repository import TaskRepository
from helios.database.session import SessionLocal

# 创建数据库会话
db = SessionLocal()

try:
    # 创建任务仓储
    task_repo = TaskRepository(db)
    
    # 创建新任务
    new_task = task_repo.create(
        description="测试任务",
        user_id=1,
        priority=5
    )
    
    # 查询任务
    task = task_repo.get(new_task.id)
    
    # 更新任务状态
    updated_task = task_repo.update_status(task.id, "IN_PROGRESS")
finally:
    db.close()
```

## 在 FastAPI 中使用

在 FastAPI 路由中，可以使用依赖注入系统获取仓储实例：

```python
from fastapi import APIRouter, Depends
from helios.repositories.task_repository import TaskRepository
from helios.database.dependencies import get_task_repository

router = APIRouter()

@router.get("/tasks/{task_id}")
async def get_task(
    task_id: str,
    task_repo: TaskRepository = Depends(get_task_repository)
):
    return task_repo.get(task_id)
```

## 数据库迁移

当模型定义发生变化时，可以使用以下方法更新数据库结构：

```python
from helios.database.migrations import reset_database

# 警告：这将删除所有数据
reset_database()
```

在生产环境中，建议使用 Alembic 进行数据库迁移。

## 测试

在测试中，可以使用内存数据库（如 SQLite）替代实际的数据库：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helios.database.models import Base
from helios.repositories.task_repository import TaskRepository

# 创建内存数据库
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
Base.metadata.create_all(bind=engine)

# 创建测试会话
db = TestingSessionLocal()

# 创建仓储
task_repo = TaskRepository(db)

# 进行测试...
``` 