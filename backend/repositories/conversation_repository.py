# helios/repositories/conversation_repository.py

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from helios.database.models import ConversationMessage
from helios.repositories.base import BaseRepository

class ConversationRepository(BaseRepository[ConversationMessage]):
    """
    ConversationMessage实体的仓储类，提供对话消息相关的数据访问方法
    """
    def __init__(self, db: Session):
        super().__init__(ConversationMessage, db)
    
    def find_by_task_id(self, task_id: uuid.UUID) -> List[ConversationMessage]:
        """
        查找任务的所有对话消息
        
        参数:
            task_id: 任务ID
            
        返回:
            任务的所有对话消息对象列表，按sequence_order排序
        """
        return self.db.query(self.model).filter(
            self.model.task_id == task_id
        ).order_by(
            self.model.sequence_order
        ).all()
    
    def find_by_speaker(self, task_id: uuid.UUID, speaker: str) -> List[ConversationMessage]:
        """
        查找指定发言者在任务中的所有对话消息
        
        参数:
            task_id: 任务ID
            speaker: 发言者角色
            
        返回:
            符合条件的对话消息对象列表
        """
        return self.db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.speaker == speaker
        ).order_by(
            self.model.sequence_order
        ).all()
    
    def get_last_message(self, task_id: uuid.UUID) -> Optional[ConversationMessage]:
        """
        获取任务的最后一条对话消息
        
        参数:
            task_id: 任务ID
            
        返回:
            最后一条对话消息对象，如果不存在则返回None
        """
        return self.db.query(self.model).filter(
            self.model.task_id == task_id
        ).order_by(
            self.model.sequence_order.desc()
        ).first()
    
    def add_message(self, task_id: uuid.UUID, speaker: str, message: str) -> ConversationMessage:
        """
        添加新的对话消息
        
        参数:
            task_id: 任务ID
            speaker: 发言者角色
            message: 消息内容
            
        返回:
            创建的对话消息对象
        """
        # 获取当前最大的sequence_order
        last_message = self.get_last_message(task_id)
        sequence_order = (last_message.sequence_order + 1) if last_message else 0
        
        # 创建新消息
        return self.create(
            task_id=task_id,
            speaker=speaker,
            message=message,
            sequence_order=sequence_order
        ) 