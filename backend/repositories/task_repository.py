# helios/repositories/task_repository.py

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from helios.database.models import Task
from helios.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    """
    Task实体的仓储类，提供任务相关的数据访问方法
    """
    def __init__(self, db: Session):
        super().__init__(Task, db)
    
    def find_by_status(self, status: str) -> List[Task]:
        """
        通过状态查找任务
        
        参数:
            status: 任务状态
            
        返回:
            符合条件的任务对象列表
        """
        return self.find(status=status)
    
    def find_by_user_id(self, user_id: int) -> List[Task]:
        """
        查找用户的所有任务
        
        参数:
            user_id: 用户ID
            
        返回:
            用户的所有任务对象列表
        """
        return self.find(user_id=user_id)
    
    def find_by_priority(self, priority: int, limit: int = 10) -> List[Task]:
        """
        查找指定优先级的任务
        
        参数:
            priority: 任务优先级
            limit: 返回结果的最大数量
            
        返回:
            符合条件的任务对象列表
        """
        return self.db.query(self.model).filter(
            self.model.priority == priority
        ).limit(limit).all()
    
    def update_status(self, task_id: uuid.UUID, status: str) -> Optional[Task]:
        """
        更新任务状态
        
        参数:
            task_id: 任务ID
            status: 新状态
            
        返回:
            更新后的任务对象，如果任务不存在则返回None
        """
        return self.update(task_id, status=status)
    
    def update_result(self, task_id: uuid.UUID, result: dict) -> Optional[Task]:
        """
        更新任务结果
        
        参数:
            task_id: 任务ID
            result: 任务结果
            
        返回:
            更新后的任务对象，如果任务不存在则返回None
        """
        return self.update(task_id, result=result)
    
    def find_pending_tasks(self, limit: int = 10) -> List[Task]:
        """
        查找待处理的任务
        
        参数:
            limit: 返回结果的最大数量
            
        返回:
            待处理的任务对象列表
        """
        return self.db.query(self.model).filter(
            self.model.status == "PENDING"
        ).order_by(
            self.model.priority.desc(),
            self.model.created_at.asc()
        ).limit(limit).all() 