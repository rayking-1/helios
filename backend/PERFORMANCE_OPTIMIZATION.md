# Helios Backend 性能优化指南

本文档提供了针对Helios自适应规划系统后端的性能优化策略和最佳实践。

## 1. LLM调用优化

LLM (大语言模型) 调用是系统中最耗时也是最昂贵的操作，优化这部分能显著提升系统响应速度和降低成本。

### 1.1 实现LLM响应缓存

```python
import hashlib
import json
from functools import lru_cache
from typing import Dict, Any, Optional

class LLMCache:
    """LLM响应缓存，减少重复调用"""
    
    def __init__(self, max_size: int = 1000):
        self.get_response = lru_cache(maxsize=max_size)(self._get_response)
        
    def _get_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        # 这个方法被lru_cache装饰，实际上缓存逻辑由装饰器处理
        return None
        
    def get_cache_key(self, model: str, messages: list, temperature: float) -> str:
        """生成缓存键"""
        # 将请求参数序列化为字符串并计算哈希值
        data = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature
        }, sort_keys=True)
        return hashlib.md5(data.encode()).hexdigest()
        
    async def get_cached_response(
        self, 
        model: str, 
        messages: list, 
        temperature: float = 0.7
    ) -> Optional[Dict[str, Any]]:
        """尝试获取缓存的响应"""
        cache_key = self.get_cache_key(model, messages, temperature)
        return self.get_response(cache_key)
        
    def add_to_cache(
        self, 
        model: str, 
        messages: list, 
        temperature: float,
        response: Dict[str, Any]
    ) -> None:
        """添加响应到缓存"""
        cache_key = self.get_cache_key(model, messages, temperature)
        # 强制将结果添加到LRU缓存
        self.get_response.__wrapped__.__cache__[cache_key] = response
        
# 使用示例
llm_cache = LLMCache()

async def get_llm_response(model: str, messages: list, temperature: float = 0.7) -> Dict[str, Any]:
    # 首先尝试从缓存获取
    cached_response = await llm_cache.get_cached_response(model, messages, temperature)
    if cached_response:
        return cached_response
        
    # 缓存未命中，调用实际的LLM API
    response = await call_llm_api(model, messages, temperature)
    
    # 将结果添加到缓存
    llm_cache.add_to_cache(model, messages, temperature, response)
    
    return response
```

### 1.2 智能体并行调用

对于某些可以并行处理的任务，可以使用asyncio同时调用多个智能体:

```python
import asyncio
from typing import Dict, List

async def parallel_agent_processing(user_goal: str) -> Dict[str, Any]:
    """并行处理用户目标，同时调用多个智能体"""
    
    async def analyst_task():
        """分析师智能体任务"""
        return await analyst_agent.process_message(user_goal)
        
    async def researcher_task():
        """研究员智能体任务"""
        return await researcher_agent.generate_research_plan({"goal": user_goal})
    
    # 并行执行两个任务
    analyst_result, researcher_result = await asyncio.gather(
        analyst_task(),
        researcher_task()
    )
    
    # 合并结果
    return {
        "analysis": analyst_result,
        "research": researcher_result
    }
```

### 1.3 LLM Token优化

减少发送到LLM的Token数量可以降低成本并提高速度:

```python
def optimize_system_message(system_message: str) -> str:
    """优化系统消息以减少token数量"""
    # 移除不必要的空白和换行符
    system_message = " ".join(system_message.split())
    
    # 简化指令，保留核心内容
    # 这里可以根据具体系统消息内容进行更精细的优化
    
    return system_message

def truncate_conversation_history(messages: List[Dict[str, str]], max_tokens: int = 3000) -> List[Dict[str, str]]:
    """截断对话历史以适应token限制"""
    # 保留system message和最近的用户消息
    system_message = next((m for m in messages if m["role"] == "system"), None)
    recent_messages = messages[-5:]  # 最近5条消息
    
    truncated_messages = []
    if system_message:
        truncated_messages.append(system_message)
        
    # 添加最近的消息
    truncated_messages.extend(recent_messages)
    
    # 确保不重复添加system message
    return [m for i, m in enumerate(truncated_messages) 
            if i == 0 or truncated_messages[i] != truncated_messages[0]]
```

## 2. 数据库优化

### 2.1 索引优化

为频繁查询的字段添加索引:

```python
# SQLAlchemy模型优化示例
from sqlalchemy import Column, Index, String, Integer, DateTime

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    plan_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    
    # 添加复合索引，用于按用户ID和计划ID查询任务
    __table_args__ = (
        Index('idx_user_plan', user_id, plan_id),
        Index('idx_status_due', status, due_date),
    )
```

通过Alembic迁移脚本添加索引:

```python
# migrations/versions/xxxx_add_indexes.py
from alembic import op

def upgrade():
    # 为user表的email字段创建索引
    op.create_index('idx_user_email', 'users', ['email'], unique=True)
    
    # 为tasks表创建复合索引
    op.create_index('idx_task_user_status', 'tasks', ['user_id', 'status'])

def downgrade():
    op.drop_index('idx_user_email', table_name='users')
    op.drop_index('idx_task_user_status', table_name='tasks')
```

### 2.2 查询优化

优化数据库查询以减少IO操作:

```python
# 优化前 - 多次查询
async def get_user_plans(user_id: str):
    plans = await db.plans.find_many({"user_id": user_id})
    
    result = []
    for plan in plans:
        # 每个计划单独查询任务，导致N+1查询问题
        tasks = await db.tasks.find_many({"plan_id": plan.id})
        plan_data = plan.dict()
        plan_data["tasks"] = tasks
        result.append(plan_data)
        
    return result

# 优化后 - 使用联结或预加载
from sqlalchemy.orm import selectinload

async def get_user_plans(user_id: str):
    # 使用selectinload一次性加载所有相关任务
    query = (
        select(Plan)
        .where(Plan.user_id == user_id)
        .options(selectinload(Plan.tasks))
    )
    
    result = await db.execute(query)
    plans = result.scalars().all()
    
    return [plan.to_dict() for plan in plans]
```

### 2.3 连接池优化

配置合适的数据库连接池大小:

```python
# database/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 根据服务器CPU核心数和内存设置合适的连接池大小
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,           # 连接池中保持的连接数
    max_overflow=20,        # 允许超出pool_size的连接数量
    pool_timeout=30,        # 等待连接的超时时间（秒）
    pool_recycle=1800,      # 回收连接的时间（秒）
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
```

## 3. API响应时间优化

### 3.1 异步处理长时间运行的任务

使用后台任务处理耗时操作:

```python
from fastapi import BackgroundTasks
from uuid import uuid4

# tasks.py
async def generate_plan_task(goal: str, user_id: str, task_id: str):
    """后台生成计划的任务"""
    try:
        # 生成计划的耗时过程
        plan = await agent_team.generate_plan(goal)
        
        # 存储结果
        await db.plans.create(
            id=str(uuid4()),
            user_id=user_id,
            goal=goal,
            tasks=plan["tasks"]
        )
        
        # 更新任务状态
        await db.tasks.update_one(
            {"id": task_id},
            {"$set": {"status": "completed"}}
        )
        
        # 通过WebSocket通知前端
        await websocket_manager.send_to_user(
            user_id, 
            {"type": "PLAN_GENERATED", "taskId": task_id}
        )
    except Exception as e:
        logger.error(f"Plan generation failed: {e}")
        await db.tasks.update_one(
            {"id": task_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )

# API端点
@router.post("/api/v1/plans")
async def create_plan(
    request: PlanRequest, 
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id)
):
    # 创建任务记录
    task_id = str(uuid4())
    task = await db.tasks.create(
        id=task_id,
        type="plan_generation",
        status="pending",
        user_id=user_id
    )
    
    # 在后台运行耗时任务
    background_tasks.add_task(
        generate_plan_task, 
        request.goal, 
        user_id, 
        task_id
    )
    
    # 立即返回任务ID
    return {"taskId": task_id, "status": "pending"}
```

### 3.2 实现API响应缓存

使用Redis缓存频繁请求的API响应:

```python
import json
from fastapi import Depends, Request, Response
from functools import wraps
import redis.asyncio as redis

# 创建Redis连接池
redis_pool = redis.ConnectionPool.from_url("redis://localhost:6379/0")

async def get_redis_client():
    """获取Redis客户端"""
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close()

def cache_response(expire: int = 300):
    """API响应缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args, 
            request: Request, 
            response: Response, 
            redis_client: redis.Redis = Depends(get_redis_client),
            **kwargs
        ):
            # 生成缓存键
            cache_key = f"api:{request.url.path}:{request.query_params}"
            
            # 检查是否有缓存
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
                
            # 没有缓存，执行原函数
            result = await func(*args, request=request, response=response, **kwargs)
            
            # 缓存结果
            await redis_client.set(
                cache_key,
                json.dumps(result),
                ex=expire
            )
            
            return result
        return wrapper
    return decorator

# 使用缓存装饰器
@router.get("/api/v1/public-plans")
@cache_response(expire=600)  # 缓存10分钟
async def get_public_plans(
    request: Request,
    response: Response,
    page: int = 1,
    limit: int = 10
):
    # 查询公开计划的逻辑
    plans = await db.plans.find_many(
        {"is_public": True},
        skip=(page - 1) * limit,
        limit=limit
    )
    
    return {
        "page": page,
        "limit": limit,
        "total": await db.plans.count({"is_public": True}),
        "data": [plan.dict() for plan in plans]
    }
```

### 3.3 使用压缩减少传输大小

在FastAPI中启用响应压缩:

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# 添加Gzip压缩中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)  # 最小压缩大小1KB
```

## 4. 内存优化

### 4.1 使用生成器和流式处理

对于大量数据的处理，使用生成器避免一次性加载全部数据到内存:

```python
async def process_large_dataset():
    # 优化前 - 一次性加载所有数据
    all_items = await db.items.find_many({})
    for item in all_items:  # 可能导致内存问题
        process_item(item)
        
    # 优化后 - 使用流式处理
    async for item in db.items.stream({}):
        await process_item(item)
        # 处理完后释放内存
```

### 4.2 周期性释放内存

对于长时间运行的进程，定期执行内存回收:

```python
import gc
import time
import asyncio

async def memory_monitor(interval_seconds: int = 3600):
    """定期监控和释放内存的后台任务"""
    while True:
        # 等待指定时间
        await asyncio.sleep(interval_seconds)
        
        # 手动触发垃圾回收
        collected = gc.collect()
        logger.info(f"Garbage collector: collected {collected} objects")
        
# 在应用启动时启动监控
@app.on_event("startup")
async def startup_event():
    # 启动内存监控任务
    asyncio.create_task(memory_monitor())
```

## 5. 日志和监控优化

### 5.1 异步日志处理

使用异步日志处理器避免日志IO阻塞主线程:

```python
import logging
import asyncio
from logging.handlers import QueueHandler, QueueListener
import queue

class AsyncLogHandler:
    """异步日志处理器，避免日志IO阻塞主线程"""
    
    def __init__(self, logger_name='helios'):
        self.log_queue = queue.Queue(-1)  # 无限队列
        self.queue_handler = QueueHandler(self.log_queue)
        
        # 配置根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        file_handler = logging.FileHandler('helios.log')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # 创建队列监听器
        self.listener = QueueListener(
            self.log_queue, 
            file_handler,
            respect_handler_level=True
        )
        
        # 配置我们的应用日志记录器
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(self.queue_handler)
        self.logger.setLevel(logging.INFO)
        
    def start(self):
        """启动异步日志处理"""
        self.listener.start()
        
    def stop(self):
        """停止异步日志处理"""
        self.listener.stop()

# 使用
log_handler = AsyncLogHandler()

@app.on_event("startup")
async def startup_event():
    log_handler.start()

@app.on_event("shutdown")
async def shutdown_event():
    log_handler.stop()
```

### 5.2 实施性能指标收集

使用Prometheus和Grafana收集和可视化性能指标:

```python
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

# 定义自定义指标
llm_requests = Counter(
    "llm_api_requests_total", 
    "Total number of LLM API requests",
    ["model", "status"]
)

llm_response_time = Histogram(
    "llm_api_response_time_seconds", 
    "LLM API response time in seconds",
    ["model"]
)

# 使用上下文管理器记录LLM调用时间
@contextlib.asynccontextmanager
async def track_llm_call(model: str):
    start_time = time.time()
    try:
        yield
        # 成功调用
        llm_requests.labels(model=model, status="success").inc()
    except Exception as e:
        # 失败调用
        llm_requests.labels(model=model, status="error").inc()
        raise e
    finally:
        # 记录响应时间
        duration = time.time() - start_time
        llm_response_time.labels(model=model).observe(duration)

# 在LLM调用中使用
async def call_llm_api(model: str, messages: list, temperature: float):
    async with track_llm_call(model):
        # 实际的API调用...
        response = await actual_llm_call(model, messages, temperature)
        return response

# 在FastAPI应用中启用Prometheus指标收集
@app.on_event("startup")
async def startup_event():
    # 设置Prometheus监控
    Instrumentator().instrument(app).expose(app)
```

## 6. 性能测试工具

1. **locust**: 负载测试工具，可以模拟大量用户同时访问API
   ```bash
   pip install locust
   ```

2. **pytest-benchmark**: 用于Python代码性能基准测试
   ```bash
   pip install pytest-benchmark
   ```
   
   示例用法:
   ```python
   def test_plan_generation_performance(benchmark):
       # 这将多次运行函数并收集性能指标
       result = benchmark(generate_plan, "学习Python编程")
       assert "tasks" in result
   ```

3. **py-spy**: Python程序的采样分析器，可以不修改代码就能分析性能
   ```bash
   pip install py-spy
   
   # 使用方法
   py-spy record -o profile.svg -- python your_program.py
   ```

4. **memory-profiler**: 分析Python代码的内存使用
   ```bash
   pip install memory-profiler
   
   # 使用装饰器分析函数内存使用
   @profile
   def memory_heavy_function():
       # 代码...
   ``` 
 

本文档提供了针对Helios自适应规划系统后端的性能优化策略和最佳实践。

## 1. LLM调用优化

LLM (大语言模型) 调用是系统中最耗时也是最昂贵的操作，优化这部分能显著提升系统响应速度和降低成本。

### 1.1 实现LLM响应缓存

```python
import hashlib
import json
from functools import lru_cache
from typing import Dict, Any, Optional

class LLMCache:
    """LLM响应缓存，减少重复调用"""
    
    def __init__(self, max_size: int = 1000):
        self.get_response = lru_cache(maxsize=max_size)(self._get_response)
        
    def _get_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        # 这个方法被lru_cache装饰，实际上缓存逻辑由装饰器处理
        return None
        
    def get_cache_key(self, model: str, messages: list, temperature: float) -> str:
        """生成缓存键"""
        # 将请求参数序列化为字符串并计算哈希值
        data = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature
        }, sort_keys=True)
        return hashlib.md5(data.encode()).hexdigest()
        
    async def get_cached_response(
        self, 
        model: str, 
        messages: list, 
        temperature: float = 0.7
    ) -> Optional[Dict[str, Any]]:
        """尝试获取缓存的响应"""
        cache_key = self.get_cache_key(model, messages, temperature)
        return self.get_response(cache_key)
        
    def add_to_cache(
        self, 
        model: str, 
        messages: list, 
        temperature: float,
        response: Dict[str, Any]
    ) -> None:
        """添加响应到缓存"""
        cache_key = self.get_cache_key(model, messages, temperature)
        # 强制将结果添加到LRU缓存
        self.get_response.__wrapped__.__cache__[cache_key] = response
        
# 使用示例
llm_cache = LLMCache()

async def get_llm_response(model: str, messages: list, temperature: float = 0.7) -> Dict[str, Any]:
    # 首先尝试从缓存获取
    cached_response = await llm_cache.get_cached_response(model, messages, temperature)
    if cached_response:
        return cached_response
        
    # 缓存未命中，调用实际的LLM API
    response = await call_llm_api(model, messages, temperature)
    
    # 将结果添加到缓存
    llm_cache.add_to_cache(model, messages, temperature, response)
    
    return response
```

### 1.2 智能体并行调用

对于某些可以并行处理的任务，可以使用asyncio同时调用多个智能体:

```python
import asyncio
from typing import Dict, List

async def parallel_agent_processing(user_goal: str) -> Dict[str, Any]:
    """并行处理用户目标，同时调用多个智能体"""
    
    async def analyst_task():
        """分析师智能体任务"""
        return await analyst_agent.process_message(user_goal)
        
    async def researcher_task():
        """研究员智能体任务"""
        return await researcher_agent.generate_research_plan({"goal": user_goal})
    
    # 并行执行两个任务
    analyst_result, researcher_result = await asyncio.gather(
        analyst_task(),
        researcher_task()
    )
    
    # 合并结果
    return {
        "analysis": analyst_result,
        "research": researcher_result
    }
```

### 1.3 LLM Token优化

减少发送到LLM的Token数量可以降低成本并提高速度:

```python
def optimize_system_message(system_message: str) -> str:
    """优化系统消息以减少token数量"""
    # 移除不必要的空白和换行符
    system_message = " ".join(system_message.split())
    
    # 简化指令，保留核心内容
    # 这里可以根据具体系统消息内容进行更精细的优化
    
    return system_message

def truncate_conversation_history(messages: List[Dict[str, str]], max_tokens: int = 3000) -> List[Dict[str, str]]:
    """截断对话历史以适应token限制"""
    # 保留system message和最近的用户消息
    system_message = next((m for m in messages if m["role"] == "system"), None)
    recent_messages = messages[-5:]  # 最近5条消息
    
    truncated_messages = []
    if system_message:
        truncated_messages.append(system_message)
        
    # 添加最近的消息
    truncated_messages.extend(recent_messages)
    
    # 确保不重复添加system message
    return [m for i, m in enumerate(truncated_messages) 
            if i == 0 or truncated_messages[i] != truncated_messages[0]]
```

## 2. 数据库优化

### 2.1 索引优化

为频繁查询的字段添加索引:

```python
# SQLAlchemy模型优化示例
from sqlalchemy import Column, Index, String, Integer, DateTime

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    plan_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    
    # 添加复合索引，用于按用户ID和计划ID查询任务
    __table_args__ = (
        Index('idx_user_plan', user_id, plan_id),
        Index('idx_status_due', status, due_date),
    )
```

通过Alembic迁移脚本添加索引:

```python
# migrations/versions/xxxx_add_indexes.py
from alembic import op

def upgrade():
    # 为user表的email字段创建索引
    op.create_index('idx_user_email', 'users', ['email'], unique=True)
    
    # 为tasks表创建复合索引
    op.create_index('idx_task_user_status', 'tasks', ['user_id', 'status'])

def downgrade():
    op.drop_index('idx_user_email', table_name='users')
    op.drop_index('idx_task_user_status', table_name='tasks')
```

### 2.2 查询优化

优化数据库查询以减少IO操作:

```python
# 优化前 - 多次查询
async def get_user_plans(user_id: str):
    plans = await db.plans.find_many({"user_id": user_id})
    
    result = []
    for plan in plans:
        # 每个计划单独查询任务，导致N+1查询问题
        tasks = await db.tasks.find_many({"plan_id": plan.id})
        plan_data = plan.dict()
        plan_data["tasks"] = tasks
        result.append(plan_data)
        
    return result

# 优化后 - 使用联结或预加载
from sqlalchemy.orm import selectinload

async def get_user_plans(user_id: str):
    # 使用selectinload一次性加载所有相关任务
    query = (
        select(Plan)
        .where(Plan.user_id == user_id)
        .options(selectinload(Plan.tasks))
    )
    
    result = await db.execute(query)
    plans = result.scalars().all()
    
    return [plan.to_dict() for plan in plans]
```

### 2.3 连接池优化

配置合适的数据库连接池大小:

```python
# database/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 根据服务器CPU核心数和内存设置合适的连接池大小
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,           # 连接池中保持的连接数
    max_overflow=20,        # 允许超出pool_size的连接数量
    pool_timeout=30,        # 等待连接的超时时间（秒）
    pool_recycle=1800,      # 回收连接的时间（秒）
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
```

## 3. API响应时间优化

### 3.1 异步处理长时间运行的任务

使用后台任务处理耗时操作:

```python
from fastapi import BackgroundTasks
from uuid import uuid4

# tasks.py
async def generate_plan_task(goal: str, user_id: str, task_id: str):
    """后台生成计划的任务"""
    try:
        # 生成计划的耗时过程
        plan = await agent_team.generate_plan(goal)
        
        # 存储结果
        await db.plans.create(
            id=str(uuid4()),
            user_id=user_id,
            goal=goal,
            tasks=plan["tasks"]
        )
        
        # 更新任务状态
        await db.tasks.update_one(
            {"id": task_id},
            {"$set": {"status": "completed"}}
        )
        
        # 通过WebSocket通知前端
        await websocket_manager.send_to_user(
            user_id, 
            {"type": "PLAN_GENERATED", "taskId": task_id}
        )
    except Exception as e:
        logger.error(f"Plan generation failed: {e}")
        await db.tasks.update_one(
            {"id": task_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )

# API端点
@router.post("/api/v1/plans")
async def create_plan(
    request: PlanRequest, 
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id)
):
    # 创建任务记录
    task_id = str(uuid4())
    task = await db.tasks.create(
        id=task_id,
        type="plan_generation",
        status="pending",
        user_id=user_id
    )
    
    # 在后台运行耗时任务
    background_tasks.add_task(
        generate_plan_task, 
        request.goal, 
        user_id, 
        task_id
    )
    
    # 立即返回任务ID
    return {"taskId": task_id, "status": "pending"}
```

### 3.2 实现API响应缓存

使用Redis缓存频繁请求的API响应:

```python
import json
from fastapi import Depends, Request, Response
from functools import wraps
import redis.asyncio as redis

# 创建Redis连接池
redis_pool = redis.ConnectionPool.from_url("redis://localhost:6379/0")

async def get_redis_client():
    """获取Redis客户端"""
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close()

def cache_response(expire: int = 300):
    """API响应缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args, 
            request: Request, 
            response: Response, 
            redis_client: redis.Redis = Depends(get_redis_client),
            **kwargs
        ):
            # 生成缓存键
            cache_key = f"api:{request.url.path}:{request.query_params}"
            
            # 检查是否有缓存
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
                
            # 没有缓存，执行原函数
            result = await func(*args, request=request, response=response, **kwargs)
            
            # 缓存结果
            await redis_client.set(
                cache_key,
                json.dumps(result),
                ex=expire
            )
            
            return result
        return wrapper
    return decorator

# 使用缓存装饰器
@router.get("/api/v1/public-plans")
@cache_response(expire=600)  # 缓存10分钟
async def get_public_plans(
    request: Request,
    response: Response,
    page: int = 1,
    limit: int = 10
):
    # 查询公开计划的逻辑
    plans = await db.plans.find_many(
        {"is_public": True},
        skip=(page - 1) * limit,
        limit=limit
    )
    
    return {
        "page": page,
        "limit": limit,
        "total": await db.plans.count({"is_public": True}),
        "data": [plan.dict() for plan in plans]
    }
```

### 3.3 使用压缩减少传输大小

在FastAPI中启用响应压缩:

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# 添加Gzip压缩中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)  # 最小压缩大小1KB
```

## 4. 内存优化

### 4.1 使用生成器和流式处理

对于大量数据的处理，使用生成器避免一次性加载全部数据到内存:

```python
async def process_large_dataset():
    # 优化前 - 一次性加载所有数据
    all_items = await db.items.find_many({})
    for item in all_items:  # 可能导致内存问题
        process_item(item)
        
    # 优化后 - 使用流式处理
    async for item in db.items.stream({}):
        await process_item(item)
        # 处理完后释放内存
```

### 4.2 周期性释放内存

对于长时间运行的进程，定期执行内存回收:

```python
import gc
import time
import asyncio

async def memory_monitor(interval_seconds: int = 3600):
    """定期监控和释放内存的后台任务"""
    while True:
        # 等待指定时间
        await asyncio.sleep(interval_seconds)
        
        # 手动触发垃圾回收
        collected = gc.collect()
        logger.info(f"Garbage collector: collected {collected} objects")
        
# 在应用启动时启动监控
@app.on_event("startup")
async def startup_event():
    # 启动内存监控任务
    asyncio.create_task(memory_monitor())
```

## 5. 日志和监控优化

### 5.1 异步日志处理

使用异步日志处理器避免日志IO阻塞主线程:

```python
import logging
import asyncio
from logging.handlers import QueueHandler, QueueListener
import queue

class AsyncLogHandler:
    """异步日志处理器，避免日志IO阻塞主线程"""
    
    def __init__(self, logger_name='helios'):
        self.log_queue = queue.Queue(-1)  # 无限队列
        self.queue_handler = QueueHandler(self.log_queue)
        
        # 配置根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        file_handler = logging.FileHandler('helios.log')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # 创建队列监听器
        self.listener = QueueListener(
            self.log_queue, 
            file_handler,
            respect_handler_level=True
        )
        
        # 配置我们的应用日志记录器
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(self.queue_handler)
        self.logger.setLevel(logging.INFO)
        
    def start(self):
        """启动异步日志处理"""
        self.listener.start()
        
    def stop(self):
        """停止异步日志处理"""
        self.listener.stop()

# 使用
log_handler = AsyncLogHandler()

@app.on_event("startup")
async def startup_event():
    log_handler.start()

@app.on_event("shutdown")
async def shutdown_event():
    log_handler.stop()
```

### 5.2 实施性能指标收集

使用Prometheus和Grafana收集和可视化性能指标:

```python
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

# 定义自定义指标
llm_requests = Counter(
    "llm_api_requests_total", 
    "Total number of LLM API requests",
    ["model", "status"]
)

llm_response_time = Histogram(
    "llm_api_response_time_seconds", 
    "LLM API response time in seconds",
    ["model"]
)

# 使用上下文管理器记录LLM调用时间
@contextlib.asynccontextmanager
async def track_llm_call(model: str):
    start_time = time.time()
    try:
        yield
        # 成功调用
        llm_requests.labels(model=model, status="success").inc()
    except Exception as e:
        # 失败调用
        llm_requests.labels(model=model, status="error").inc()
        raise e
    finally:
        # 记录响应时间
        duration = time.time() - start_time
        llm_response_time.labels(model=model).observe(duration)

# 在LLM调用中使用
async def call_llm_api(model: str, messages: list, temperature: float):
    async with track_llm_call(model):
        # 实际的API调用...
        response = await actual_llm_call(model, messages, temperature)
        return response

# 在FastAPI应用中启用Prometheus指标收集
@app.on_event("startup")
async def startup_event():
    # 设置Prometheus监控
    Instrumentator().instrument(app).expose(app)
```

## 6. 性能测试工具

1. **locust**: 负载测试工具，可以模拟大量用户同时访问API
   ```bash
   pip install locust
   ```

2. **pytest-benchmark**: 用于Python代码性能基准测试
   ```bash
   pip install pytest-benchmark
   ```
   
   示例用法:
   ```python
   def test_plan_generation_performance(benchmark):
       # 这将多次运行函数并收集性能指标
       result = benchmark(generate_plan, "学习Python编程")
       assert "tasks" in result
   ```

3. **py-spy**: Python程序的采样分析器，可以不修改代码就能分析性能
   ```bash
   pip install py-spy
   
   # 使用方法
   py-spy record -o profile.svg -- python your_program.py
   ```

4. **memory-profiler**: 分析Python代码的内存使用
   ```bash
   pip install memory-profiler
   
   # 使用装饰器分析函数内存使用
   @profile
   def memory_heavy_function():
       # 代码...
   ``` 
 
 